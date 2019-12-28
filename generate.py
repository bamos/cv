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
from itertools import groupby
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
        sep = ", " if len(authors) > 2 else " "
        authors = sep.join(authors)

        # Hacky fix for special characters.
        authors = authors.replace('\\"o', '&ouml;')

        return authors

    # [First Initial]. [Last Name]
    def _format_author_list(immut_author_list):
        formatted_authors = []
        for author in immut_author_list:
            if 'zico' in author.lower():
                new_auth = 'J. Z. Kolter'
                if '*' in author:
                    new_auth += '*'
            else:
                new_auth = author.split(", ")
                new_auth = new_auth[1][0] + ". " + new_auth[0]
                if config['name'] in new_auth:
                    new_auth = "<strong>" + new_auth + "</strong>"
            formatted_authors.append(new_auth)
        return formatted_authors

    def _get_pub_str(pub, prefix, gidx, includeImage):
        author_str = _get_author_str(pub['author'])
        # prefix = category['prefix']
        title = pub['title']
        # if title[-1] not in ("?", ".", "!"):
        #    title += ","
        # title = '"{}"'.format(title)
        # if 'link' in pub:
        #     title = "<a href=\'{}\'>{}</a>".format(
        #         pub['link'], title)
        title = title.replace("\n", " ")

        assert('_venue' in pub and 'year' in pub)
        yearVenue = "{} {}".format(pub['_venue'], pub['year'])

        imgStr = '<img src="images/publications/{}.png"/>'.format(pub['ID'])
        links = ['[{}{}]'.format(prefix, gidx)]
        abstract = ''
        if 'abstract' in pub:
            links.append("""
[<a href='javascript:;'
    onclick=\'$(\"#abs_{}{}\").toggle()\'>abs</a>]""".format(pub['ID'], prefix))
            abstract = context.make_replacements(pub['abstract'])
        if 'link' in pub:
            imgStr = "<a href=\'{}\' target='_blank'>{}</a> ".format(
                pub['link'], imgStr)
            links.append(
                "[<a href=\'{}\' target='_blank'>pdf</a>] ".format(pub['link']))
        if 'codeurl' in pub:
            links.append(
                "[<a href=\'{}\' target='_blank'>code</a>] ".format(pub['codeurl']))
        links = ' '.join(links)

        if abstract:
            abstract = '''
<div id="abs_{}{}" style="text-align: justify; display: none" markdown="1">
{}
</div>
'''.format(pub['ID'], prefix, abstract)

        if '_note' in pub:
            note_str = '<strong>{}</strong><br>'.format(pub['_note'])
        else:
            note_str = ''

        if includeImage:
            return '''
<tr>
<td class="col-md-3">{}</td>
<td>
    <strong>{}</strong><br>
    {}<br>
    {}<br>
    {}
    {}<br>
    {}
</td>
</tr>
'''.format(imgStr, title, author_str, yearVenue, note_str, links, abstract)
        else:
            return '''
<tr>
<td>
    <strong>{}</strong><br>
    {}<br>
    {}<br>
    {}
    {}<br>
    {}
</td>
</tr>
'''.format(title, author_str, yearVenue, note_str, links, abstract)

    def load_and_replace(bibtex_file):
        with open(os.path.join('publications', bibtex_file), 'r') as f:
            p = BibTexParser(f.read(), bc.author).get_entry_list()
        for pub in p:
            for field in pub:
                pub[field] = context.make_replacements(pub[field])
            pub['author'] = _format_author_list(pub['author'])
        return p

    # if 'categories' in config:
    #     contents = []
    #     for category in config['categories']:
    #         type_content = {}
    #         type_content['title'] = category['heading']

    #         pubs = load_and_replace(category['file'])

    #         details = ""
    #         # sep = "<br><br>\n"
    #         sep = "\n"
    #         for i, pub in enumerate(pubs):
    #             details += _get_pub_str(pub, category['prefix'],
    #                                     i + 1, includeImage=False) + sep
    #         type_content['details'] = details
    #         type_content['file'] = category['file']
    #         contents.append(type_content)
    # else:

    include_image = config['include_image']
    sort_bib = config['sort_bib']
    group_by_year = config['group_by_year']

    contents = {}
    pubs = load_and_replace(config['file'])
    sep = "\n"

    if sort_bib:
        pubs = sorted(pubs, key=lambda pub: int(pub['year']), reverse=True)

    if group_by_year:
        for pub in pubs:
            m = re.search('(\d{4})', pub['year'])
            assert m is not None
            pub['year_int'] = int(m.group(1))
            pub['ID'] += f"_{config['file'].replace('.', '_')}"

        details = ''
        for year, year_pubs in groupby(pubs, lambda pub: pub['year_int']):
            details += f'<h2>{year}</h2>\n'
            details += '<table class="table table-hover">\n'
            for i, pub in enumerate(year_pubs):
                details += _get_pub_str(pub, '', i + 1, includeImage=include_image) + sep
            details += '</table>\n'
    else:
        details = '<table class="table table-hover">'
        for i, pub in enumerate(pubs):
            details += _get_pub_str(pub, '', i + 1, includeImage=include_image) + sep
        details += '</table>'
    contents['details'] = details
    contents['file'] = config['file']

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
            if section_tag == 'about':
                if self._file_ending == '.tex':
                    continue
                section_template_name = "section" + self._file_ending
                section_data['data'] = section_content
            elif section_tag == 'news':
                if self._file_ending == '.tex':
                    continue
                section_template_name = os.path.join(self.SECTIONS_DIR, 'news.md')
                section_data['items'] = section_content
            elif section_tag == 'service':
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, 'skills' + self._file_ending)
            elif section_tag in ['coursework', 'education', 'honors',
                                 'industry', 'research', 'skills', 'teaching']:
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif 'publications' in section_tag:
                if self._file_ending == ".tex":
                    section_data['content'] = section_content
                elif self._file_ending == ".md":
                    section_data['content'] = get_pub_md(self, section_content)
                section_data['scholar_id'] = yaml_data['social']['google_scholar']
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
        (r'\\\\\[[^\]]*]', '\n'),  # newlines
        (r'\\ ', ' '),  # spaces
        (r'\\&', '&'),  # unescape &
        (r'\\\$', '\$'),  # unescape $
        (r'\\%', '%'),  # unescape %
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
        (r'\\href{([^}]*)}{([^}]*)}', r'[\2](\1)'),  # urls
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
