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
import yaml

import bibtexparser.customization as bc
from bibtexparser.bparser import BibTexParser
from datetime import date
from jinja2 import Environment, FileSystemLoader


def get_pub_md(context, config):
    """Given the bibtexparser's representation and configuration,
    return a markdown string similar to BibTeX's output
    of a markdown file.
    See `publications.bib` for an example BibTeX file.

    ### Conference Proceedings
    [C1] Names. "Paper A," in <em>IEEE</em>, 2015.<br><br>
    [C2] Names. "Paper B," in <em>IEEE</em>, 2015.<br><br>

    ### Journal Articles
    [J1] Names. "Paper C," in <em>IEEE</em>, 2015.<br><br>
"""

    def _get_author_str(immut_author_list):
        authors = copy.copy(immut_author_list)
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
        return ", ".join(authors)

    # [First Initial]. [Last Name]
    def _format_author_list(immut_author_list):
        formatted_authors = []
        for author in immut_author_list:
            new_auth = author.split(", ")
            new_auth = new_auth[1][0] + ". " + new_auth[0]
            if new_auth == config['name']:
                new_auth = "**" + new_auth + "**"
            formatted_authors.append(new_auth)
        return formatted_authors

    def _get_pub_str(pub, prefix, gidx):
        author_str = _get_author_str(pub['author'])
        prefix = category['prefix']
        title = pub['title']
        if title[-1] not in ("?", ".", "!"):
            title += ","
        title = '"{}"'.format(title)
        if 'link' in pub:
            title = "<a href=\'{}\'>{}</a>".format(
                pub['link'], title)

        if pub['ENTRYTYPE'] == "inproceedings":
            if pub['booktitle']:
                title += ' in <em>{}</em>,'.format(pub['booktitle'])
        elif pub['ENTRYTYPE'] == "article":
            if pub['journal']:
                title += ' <em>{}</em>,'.format(pub['journal'])

        return '+ [{}{}] {}, {} {}.'.format(
            prefix, gidx, author_str, title, pub['year'])

    def load_and_replace(bibtex_file):
        with open(os.path.join('publications', bibtex_file), 'r') as f:
            p = BibTexParser(f.read(), bc.author).get_entry_list()
        for pub in p:
            for field in pub:
                pub[field] = context.make_replacements(pub[field])
            pub['author'] = _format_author_list(pub['author'])
        return p

    contents = []
    for category in config['categories']:
        type_content = {}
        type_content['title'] = category['heading']

        pubs = load_and_replace(category['file'])

        details = ""
        # sep = "<br><br>\n"
        sep = "\n"
        for i, pub in enumerate(pubs):
            details += _get_pub_str(pub, category['prefix'], i + 1) + sep
        type_content['details'] = details
        contents.append(type_content)

    return contents


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
        template_name = template_name.replace(os.path.sep, '/')  # Fixes #11.
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
        for section_tag, section_title in yaml_data['order']:
            print("  + Processing section: {}".format(section_tag))

            section_data = {'name': section_title}
            section_content = None if section_tag == "NEWPAGE" else yaml_data[section_tag]
            if section_tag == 'interests':
                section_template_name = "section" + self._file_ending
                section_data['data'] = section_content
            elif section_tag in ['coursework', 'education', 'honors',
                                 'industry', 'research',
                                 'skills', 'teaching']:
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif section_tag == 'publications':
                if self._file_ending == ".tex":
                    section_data['items'] = section_content
                elif self._file_ending == ".md":
                    section_data['items'] = get_pub_md(self, section_content)
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif section_tag == 'NEWPAGE':
                pass
            else:
                print("Error: Unrecognized section tag: {}".format(section_tag))
                # sys.exit(-1) TODO
                continue

            if section_tag == 'NEWPAGE':
                if self._file_ending == ".tex":
                    body += "\n\n\\newpage\n"
                elif self._file_ending == ".md":
                    pass
            else:
                rendered_section = self._render_template(
                    section_template_name, section_data)
                body += rendered_section.rstrip() + '\n\n\n'

        yaml_data['body'] = body
        yaml_data['today'] = date.today().strftime("%B %d, %Y")
        return self._render_template(
            self._base_template, yaml_data).rstrip() + '\n'

    def write_to_outfile(self, output_data):
        with open(self._output_file, 'wb') as out:
            output_data = output_data.encode('utf-8')
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
        (r'\\ ', ' '),  # spaces
        (r'\\&', '&'),  # unescape &
        (r'\\textbf{([^}]*)}', r'**\1**'),  # bold text
        (r'\{ *\\bf *([^}]*)\}', r'**\1**'),
        (r'\\textit{([^}]*)}', r'*\1*'),  # italic text
        (r'\{ *\\it *([^}]*)\}', r'*\1*'),
        (r'\\LaTeX', 'LaTeX'),  # \LaTeX to boring old LaTeX
        (r'\\TeX', 'TeX'),  # \TeX to boring old TeX
        ('---', '-'),  # em dash
        ('--', '-'),  # en dash
        (r'``([^\']*)\'\'', r'"\1"'),  # quotes
        (r'\\url{([^}]*)}', r'[\1](\1)'),  # urls
        (r'\{([^}]*)\}', r'\1'),  # Brackets.
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
    parser = argparse.ArgumentParser(description='Generates HTML, LaTeX, and Markdown resumes from data in YAML files.')
    parser.add_argument('yamls', metavar='YAML_FILE', nargs='+',
                        help='The YAML files that contain the resume/cv'
                        'details, in order of increasing precedence')
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
