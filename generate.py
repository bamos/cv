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

import requests
from bs4 import BeautifulSoup

import shelve

from scholarly import scholarly
import bibtexparser.customization as bc
from bibtexparser.bparser import BibTexParser
from datetime import date
from itertools import groupby
from jinja2 import Environment, FileSystemLoader

# TODO: Could really be cleaned up
def get_pub_md(context, config):
    def _get_author_str(immut_author_list):
        authors = copy.copy(immut_author_list)
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
        sep = ", " if len(authors) > 2 else " "
        authors = sep.join(authors)

        # Hacky fix for special characters.
        authors = authors.replace(r'\"o', '&ouml;')
        authors = authors.replace(r'\'o', '&oacute;')
        authors = authors.replace(r"\'\i", '&iacute;')

        return authors

    def _format_author_list(immut_author_list):
        formatted_authors = []
        for author in immut_author_list:
            new_auth = author.split(", ")
            assert len(new_auth) == 2
            new_auth = new_auth[1] + " " + new_auth[0]
            author_urls = config['author_urls']

            k = list(filter(lambda k: k in new_auth, author_urls.keys()))
            if len(k) == 0 and config['name'] not in new_auth:
                print(f"+ Author URL not found for {new_auth}")

            new_auth = new_auth.replace(' ', '&nbsp;')
            if len(k) > 0:
                assert len(k) == 1, k
                url = author_urls[k[0]]
                new_auth = f"<a href='{url}' target='_blank'>{new_auth}</a>"

            if config['name'] in new_auth:
                new_auth = "<strong>" + new_auth + "</strong>"

            # if 'zico' in author.lower():
            #     new_auth = 'J. Z. Kolter'
            #     if '*' in author:
            #         new_auth += '*'
            # else:
            #     new_auth = author.split(", ")
            #     new_auth = new_auth[1][0] + ". " + new_auth[0]
            #     if config['name'] in new_auth:
            #         new_auth = "<strong>" + new_auth + "</strong>"
            formatted_authors.append(new_auth)
        return formatted_authors

    def _get_pub_str(pub, prefix, gidx, include_image):
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
        year_venue = "{} {}".format(pub['_venue'], pub['year'])

        highlight = 'selected' in pub and pub['selected'].lower() == 'true'
        img_str = f'<img src="images/publications/{pub["ID"]}.png" onerror="this.style.display=\'none\'" class="publicationImg" />'
        links = []
        abstract = ''
        if 'abstract' in pub:
            links.append("""
[<a href='javascript:;'
    onclick=\'$(\"#abs_{}{}\").toggle()\'>abs</a>]""".format(pub['ID'], prefix))
            abstract = context.make_replacements(pub['abstract'])
        if 'link' in pub:
            img_str = "<a href=\'{}\' target='_blank'>{}</a> ".format(
                pub['link'], img_str)
            title = "<a href=\'{}\' target='_blank'>{}</a> ".format(
                pub['link'], title)

        for base in ['code', 'slides', 'talk']:
            key = base + 'url'
            if key in pub:
                links.append(
                    "[<a href=\'{}\' target='_blank'>{}</a>] ".format(
                        pub[key], base))
        links = ' '.join(links)

        if abstract:
            abstract = '''
<div id="abs_{}{}" style="text-align: justify; display: none" markdown="1">
{}
</div>
'''.format(pub['ID'], prefix, abstract)

        if '_note' in pub:
            note_str = f"({pub['_note']})"
        else:
            note_str = ''

        tr_style = 'style="background-color: #ffffd0"' if highlight else ''
        if include_image:
            return f'''
<tr id="tr-{pub['ID']}" {tr_style}>
<td align='right' style='padding-left:0;padding-right:0;'>
{prefix}{gidx}.
</td>
<td>
{img_str}
<em>{title}</em> {links}<br>
{author_str}<br>
{year_venue} {note_str} <br>
{abstract}
</td>
</tr>
'''
        else:
            return f'''
<tr id="tr-{pub['ID']}" {tr_style}>
<td align='right'>
{prefix}{gidx}.
</td>
<td>
    <em>{title}</em> {links}<br>
    {author_str}<br>
    {year_venue} {note_str} <br>
    {abstract}
</td>
</tr>
'''

    def load_and_replace(bibtex_file):
        with open(os.path.join('publications', bibtex_file), 'r') as f:
            p = BibTexParser(f.read(), bc.author).get_entry_list()
        for pub in p:
            for field in pub:
                if field != 'link':
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
    #                                     i + 1, include_image=False) + sep
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

        details = ''
        gidx = 1
        for year, year_pubs in groupby(pubs, lambda pub: pub['year_int']):
            print_year = year >= 2015

            if print_year:
                year_str = str(year)
                if year == 2015:
                    year_str = "2015 and earlier"
                details += f'<h2>{year_str}</h2>\n'
                details += '<table class="table table-hover">\n'

            for i, pub in enumerate(year_pubs):
                details += _get_pub_str(
                    pub, '', gidx,
                    include_image=include_image,
                ) + sep
                gidx += 1

            if print_year and year > 2015:
                details += '</table>\n'

        if not print_year:
            details += '</table>\n'

    else:
        details = '<table class="table table-hover">'
        for i, pub in enumerate(pubs):
            details += _get_pub_str(pub, '', i + 1,
                    include_image=include_image,
                ) + sep
        details += '</table>'
    contents['details'] = details
    contents['file'] = config['file']

    return contents


# TODO: Could really be cleaned up
def get_pub_latex(context, config):
    def _get_author_str(immut_author_list):
        authors = copy.copy(immut_author_list)
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
        sep = ", " if len(authors) > 2 else " "
        authors = sep.join(authors)

        return authors

    # [First Initial]. [Last Name]
    def _format_author_list(immut_author_list):
        formatted_authors = []
        for author in immut_author_list:
            new_auth = author.split(", ")
            assert len(new_auth) == 2
            new_auth = new_auth[1] + " " + new_auth[0]
            author_urls = config['author_urls']

            k = list(filter(lambda k: k in new_auth, author_urls.keys()))
            if len(k) > 0:
                assert len(k) == 1, k
                url = author_urls[k[0]]
                new_auth = f"\href{{{url}}}{{{new_auth}}}"

            if config['name'] in new_auth:
                new_auth = r"\textbf{" + new_auth + r"}"
            new_auth = new_auth.replace('. ', '.~')
            new_auth = '\mbox{' + new_auth + '}'
            formatted_authors.append(new_auth)
        return formatted_authors


    def _get_pub_str(pub, prefix, gidx):
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
        if 'link' in pub:
            title = r"\href{{{}}}{{{}}} ".format(pub['link'], title)

        assert('_venue' in pub and 'year' in pub)
        year_venue = "{} {}".format(pub['_venue'], pub['year'])

        links = []
        for base in ['code', 'slides', 'talk']:
            key = base + 'url'
            if key in pub:
                links.append(
                    r"[\href{{{}}}{{{}}}] ".format(pub[key], base))
        links = ' '.join(links)

        highlight = 'selected' in pub and pub['selected'].lower() == 'true'
        highlight_color = '\cellcolor{tab_highlight}' if highlight else ''
        if '_note' in pub:
            # note_str = r'{} && \textbf{{{}}} \\'.format(
            note_str = f"({pub['_note']})"
        else:
            note_str = ''

        return rf'''
\begin{{minipage}}{{\textwidth}}
\begin{{tabular}}[t]{{p{{8mm}}p{{1mm}}>{{\raggedright\arraybackslash}}p{{6.5in}}}}
{highlight_color} \hfill{prefix}{gidx}.\hspace*{{1mm}} && \textit{{{title}}} {links} \\
{highlight_color} && {author_str} \\
{highlight_color} && {year_venue} {note_str} \\
\end{{tabular}} \\[2mm]
\end{{minipage}}'''

    def load_and_replace(bibtex_file):
        with open(os.path.join('publications', bibtex_file), 'r') as f:
            p = BibTexParser(f.read(), bc.author).get_entry_list()
        for pub in p:
            for field in pub:
                if field != 'link':
                    pub[field] = context.make_replacements(pub[field])
            pub['author'] = _format_author_list(pub['author'])
        return p

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

        details = ''
        gidx = 1
        for year, year_pubs in groupby(pubs, lambda pub: pub['year_int']):
            print_year = year >= 2015
            if print_year:
                year_str = str(year)
                if year == 2015:
                    year_str = "2015 and earlier"
                details += rf'\subsection{{{year_str}}}' + '\n'

            for i, pub in enumerate(year_pubs):
                details += _get_pub_str(pub, '', gidx) + sep
                gidx += 1

    else:
        assert False
    contents['details'] = details
    contents['file'] = config['file']

    return contents


def add_repo_data(context, config):
    repo_htmls = shelve.open('repo_htmls.shelf')

    for item in config:
        assert 'repo_url' in item
        assert 'year' in item
        assert 'github' in item['repo_url']

        short_name = re.search('.*github\.com/(.*)', item['repo_url'])[1]
        if 'name' not in item:
            item['name'] = short_name

        # Scrape the repo HTML instead of using the GitHub API
        # to avoid being rate-limited (sorry), and be nice by
        # caching to disk.
        if short_name not in repo_htmls:
            r = requests.get(item['repo_url'])
            repo_htmls[short_name] = r.content
        soup = BeautifulSoup(repo_htmls[short_name], 'html.parser')

        item['stars'] = soup.find(class_="js-social-count").text.strip()

        if 'desc' not in item:
            item['desc'] = soup.find('p', class_='f4 mt-3').text.strip()


def get_scholar_stats(scholar_id):
    scholar_stats = shelve.open('scholar_stats.shelf')
    if 'h_index' not in scholar_stats:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=['indices'])
        scholar_stats['h_index'] = author['hindex']
        scholar_stats['citations'] = '{:.1f}k'.format(author['citedby'] / 1000)
    return scholar_stats


class RenderContext(object):
    BUILD_DIR = 'build'
    TEMPLATES_DIR = 'templates'
    SECTIONS_DIR = 'sections'
    DEFAULT_SECTION = 'items'
    BASE_FILE_NAME = 'cv'

    def __init__(self, context_name, file_ending, jinja_options, replacements):
        self._context_name = context_name
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
            if not yaml_data.startswith('http'):
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
            print("Processing section: {}".format(section_tag))

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
            elif section_tag == 'repos':
                add_repo_data(self, section_content)
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif section_tag in ['current_position']:
                if self._context_name == 'markdown':
                    continue
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, 'positions' + self._file_ending)
            elif section_tag in ['coursework', 'education', 'honors',
                                 'positions', 'research', 'skills', 'service',
                                 'teaching', 'talks', 'advising']:
                section_data['items'] = section_content
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif 'publications' in section_tag:
                if self._file_ending == ".tex":
                    # section_data['content'] = section_content
                    section_data['content'] = get_pub_latex(self, section_content)
                elif self._file_ending == ".md":
                    section_data['content'] = get_pub_md(self, section_content)
                section_data['scholar_id'] = yaml_data['social']['google_scholar']
                section_data['scholar_stats'] = get_scholar_stats(yaml_data['social']['google_scholar'])
                section_template_name = os.path.join(
                    self.SECTIONS_DIR, section_tag + self._file_ending)
            elif section_tag == 'NEWPAGE':
                pass
            else:
                print("Error: Unrecognized section tag: {}".format(section_tag))
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
        # (r'~', ' '),  # spaces
        (r'\.~', '. '),  # spaces
        (r'\\ ', ' '),  # spaces
        (r'\\&', '&'),  # unescape &
        (r'\\\$', '\$'),  # unescape $
        (r'\\%', '%'),  # unescape %
        (r'\\textbf{(.*)}', r'**\1**'),  # bold text
        (r'\{ *\\bf *(.*)\}', r'**\1**'),
        (r'\\textit{(.*)}', r'*\1*'),  # italic text
        (r'\{ *\\it *(.*)\}', r'*\1*'),
        (r'\\LaTeX', 'LaTeX'),  # \LaTeX to boring old LaTeX
        (r'\\TeX', 'TeX'),  # \TeX to boring old TeX
        (' --- ', '&nbsp;-&nbsp;'),  # em dash
        (' -- ', '&nbsp;-&nbsp;'),  # en dash
        ('---', '-'),  # em dash
        ('--', '-'),  # en dash
        (r'``([^\']*)\'\'', r'"\1"'),  # quotes
        (r'\\url{([^}]*)}', r'[\1](\1)'),  # urls
        # (r'\\href{([^}]*)}{([^}]*)}', r'[\2](\1)'),  # urls
        (r'\\href{([^}]*)}{([^}]*)}', r'<a href="\1" target="_blank">\2</a>'),  # urls
        (r'\{([^}]*)\}', r'\1'),  # Brackets.
        (r'\$\\varheart\$', r'<i class="fa fas fa-heart"></i>'),  # Heart.
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
            yaml_data.update(yaml.safe_load(f))

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
