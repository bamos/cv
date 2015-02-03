#!/usr/bin/env python3

"""Generates LaTeX, markdown, and plaintext copies of my cv."""

__author__ = [
    'Brandon Amos <http://bamos.github.io>',
    'Ellis Michael <http://ellismichael.com>',
]

import argparse
import copy
import os
import re
import sys
import yaml

from bibtexparser.customization import *
from bibtexparser.bparser import BibTexParser
from datetime import date
from jinja2 import Environment, FileSystemLoader

def _get_bibtex_md(p, pub_types):
    def get_author_str(authors):
        a_len = len(authors)
        if a_len == 1:
            author_str = authors[0]
        elif a_len == 2:
            author_str = authors[0] + " and " + authors[1]
        else:
            author_str = ""
            for i in range(a_len):
                author_str += authors[i]
                if i < a_len-1: author_str += ", "
                if i == a_len-2: author_str += "and "
        return author_str

    for item in p:
        new_auth_list = []
        for auth in item['author']:
            new_auth = auth.split(", ")
            new_auth = new_auth[1][0] + ". " + new_auth[0]
            if new_auth == "B. Amos":
                new_auth = "**" + new_auth + "**"
            new_auth_list.append(new_auth)
        item['author'] = new_auth_list

    contents = []
    for t in pub_types:
        gidx = 1
        type_content = {}
        type_content['title'] = t[3]
        filtered = list(filter(lambda x: x['type'] == t[0], p))
        if t[1]:
            for x in filtered:
                if 'keyword' not in x or \
                        (x['keyword'] != 'journal' and x['keyword'] != 'magazine'):
                    print("Error: Bibliography 'article' items must define a "+
                      "keyword 'journal' or 'magazine'.")
                    sys.exit(-1)
            filtered = list(filter(lambda x: x['keyword'] == t[1], filtered))
        details = ""
        for item in filtered:
            author_str = get_author_str(item['author'])
            if item['title'][-1] not in ("?", ".", "!"): punc = ","
            else: punc = ""
            titlePunctuation = ","
            if t[0] == "inproceedings":
                details += "[" + t[2] + str(gidx) + "] " + \
                    author_str + ", \"" + item['title'] + punc + "\""
                if item['booktitle']:
                    details += " in <em>" + item['booktitle'] + "</em>,"
                details += " " + item['year'] + "<br><br>\n"
            elif t[0] == "article":
                details += "[" + t[2] + str(gidx) + "] " + \
                    author_str + ", \"" + item['title'] + punc + "\""
                if item['journal']:
                    details += " <em>" + item['journal'] + "</em>,"
                details += " " + item['year'] + "<br><br>\n"
            else:
                print(t)
                raise Exception()
            gidx += 1
        type_content['details'] = details
        contents.append(type_content)

    return contents

# def generate(ext):
    # print("Generating for extension: {}".format(ext))
    # body = ""
    # for section_tag,section_title in yaml_contents['order']:
    #     print("  + Section: {}".format(section_tag))
    #     section_contents = yaml_contents[section_tag]
    #     section_title = section_title.title()
    #     if ext == "md":
    #         section_contents = latexToMd(section_contents)
    #         section_title = latexToMd(section_title)

    #     if section_tag == 'publications' and ext == "md":
    #         with open(contents, 'r') as f:
    #             p = BibTexParser(f.read(), author).get_entry_list()
    #             pub_types = [
    #                 ('inproceedings', '', 'C', 'Conference Proceedings'),
    #                 ('article', 'journal', 'J', 'Journal Articles'),
    #                 ('article', 'magazine', 'M', 'Magazine Articles'),
    #             ]
    #             contents = get_bibtex_md(p, pub_types)

class RenderContext(object):
    BUILD_DIR = 'build'
    TEMPLATES_DIR = 'templates'
    SECTIONS_DIR = 'sections'
    DEFAULT_SECTION = 'items'
    BASE_FILE_NAME = 'cv'

    def __init__(self, context_name, file_ending, jinja_options, replacements):
        self._file_ending = file_ending
        self._replacements = replacements

        context_templates_dir = os.path.join(self.TEMPLATES_DIR, context_name)

        self._output_file = os.path.join(
            self.BUILD_DIR, self.BASE_FILE_NAME + self._file_ending)
        self._base_template = self.BASE_FILE_NAME + self._file_ending

        self._context_type_name = context_name + 'type'

        self._jinja_options = jinja_options.copy()
        self._jinja_options['loader'] = FileSystemLoader(
            searchpath=context_templates_dir)
        self._jinja_env = Environment(**self._jinja_options)

    def make_replacements(self, yaml_data):
        # Make a copy of the yaml_data so that this function is idempotent
        yaml_data = copy.copy(yaml_data)

        if isinstance(yaml_data, str):
            for o, r in self._replacements:
                yaml_data = re.sub(o, r, yaml_data)

        elif isinstance(yaml_data, dict):
            for k, v in yaml_data.items():
                yaml_data[k] = self.make_replacements(v)

        elif isinstance(yaml_data, list):
            for idx, item in enumerate(yaml_data):
                yaml_data[idx] = self.make_replacements(item)

        return yaml_data

    def _render_template(self, template_name, yaml_data):
        return self._jinja_env.get_template(template_name).render(yaml_data)

    @staticmethod
    def _make_double_list(items):
        groups = []
        items_temp = list(items)
        while len(items_temp):
            group = {}
            group['first'] = items_temp.pop(0)
            if len(items_temp):
                group['second'] = items_temp.pop(0)
            groups.append(group)
        return groups

    def render_resume(self, yaml_data):
        # Make the replacements first on the yaml_data
        yaml_data = self.make_replacements(yaml_data)

        body = ''
        for section_tag,section_title in yaml_data['order']:
            print("  + Processing section: {}".format(section_tag))

            section_data = {'name': section_title}
            section_content = yaml_data[section_tag]
            if section_tag == 'interests':
                section_template_name = "section"+self._file_ending
                section_data['data'] = section_content
            elif section_tag in ['education','honors',
                                 'industry','research',
                                 'skills','teaching']:
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif section_tag == 'publications':
                if self._file_ending == ".tex":
                    section_data['items'] = section_content
                elif self._file_ending == ".md":
                    with open(section_content, 'r') as f:
                        p = BibTexParser(f.read(), author).get_entry_list()
                        pub_types = [
                            ('inproceedings', '', 'C', 'Conference Proceedings'),
                            ('article', 'journal', 'J', 'Journal Articles'),
                            ('article', 'magazine', 'M', 'Magazine Articles'),
                        ]
                        section_data['items'] = _get_bibtex_md(p,pub_types)
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            else:
                print("Error: Unrecognized section tag: {}".format(section_tag))
                # sys.exit(-1) TODO
                continue

            rendered_section = self._render_template(
                section_template_name, section_data)
            body += rendered_section.rstrip() + '\n\n\n'

        yaml_data['body'] = body
        yaml_data['today'] = date.today().strftime("%B %d, %Y")
        return self._render_template(
            self._base_template, yaml_data).rstrip() + '\n'

    def write_to_outfile(self, output_data):
        with open(self._output_file, 'w') as out:
            out.write(output_data)



LATEX_CONTEXT = RenderContext(
    'latex',
    '.tex',
    dict(
        block_start_string='~<',
        block_end_string='>~',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
        trim_blocks=True,
        lstrip_blocks=True
    ),
    []
)

MARKDOWN_CONTEXT = RenderContext(
    'markdown',
    '.md',
    dict(
        trim_blocks=True,
        lstrip_blocks=True
    ),
    [
        (r'\\ ', ' '), # spaces
        (r'\\&', '&'), # unescape &
        (r'\\textbf{([^}]*)}', r'**\1**'), # bold text
        (r'\\textit{([^}]*)}', r'*\1*'), # italic text
        (r'\{ *\\it *([^}]*)\}', r'*\1*'),
        (r'\\LaTeX', 'LaTeX'), # \LaTeX to boring old LaTeX
        (r'\\TeX', 'TeX'), # \TeX to boring old TeX
        ('---', '-'), # em dash
        ('--', '-'), # en dash
        (r'``([^\']*)\'\'', r'"\1"'), # quotes
    ]
)

def process_resume(context, yaml_data, preview):
    rendered_resume = context.render_resume(yaml_data)
    if preview:
        print(rendered_resume)
    else:
        context.write_to_outfile(rendered_resume)

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description=
        'Generates HTML, LaTeX, and Markdown resumes from data in YAML files.')
    parser.add_argument('yamls', metavar='YAML_FILE', nargs='+',
        help='the YAML files that contain the resume/cv details, in order of '
             'increasing precedence')
    parser.add_argument('-p', '--preview', action='store_true',
        help='prints generated content to stdout instead of writing to file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--latex', action='store_true',
        help='only generate LaTeX resume/cv')
    group.add_argument('-m', '--markdown', action='store_true',
        help='only generate Markdown resume/cv')
    args = parser.parse_args()

    yaml_data = {}
    for yaml_file in args.yamls:
        with open(yaml_file) as f:
            yaml_data.update(yaml.load(f))

    if args.latex or args.markdown:
        if args.latex:
            process_resume(LATEX_CONTEXT, yaml_data, args.preview)
        elif args.markdown:
            process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview)
    else:
        process_resume(LATEX_CONTEXT, yaml_data, args.preview)
        process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview)


if __name__ == "__main__":
    main()
