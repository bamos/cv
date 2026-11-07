import tempfile
import unittest
from pathlib import Path

import generate


class PublicationVenueTests(unittest.TestCase):
    def test_venue_and_year_are_formatted_once(self):
        for venue, expected in [('NeurIPS', 'NeurIPS 2026'), ('', '2026')]:
            with self.subTest(venue=venue):
                self.assertEqual(generate.format_publication_venue({
                    'ID': 'example', '_venue': venue, 'year': '2026',
                }), expected)

    def test_duplicate_year_identifies_the_publication(self):
        for venue in ['NeurIPS 2026', 'NeurIPS (2026)', 'NeurIPS2026']:
            with self.subTest(venue=venue):
                with self.assertRaisesRegex(ValueError, "example.*2026.*_venue"):
                    generate.format_publication_venue({
                        'ID': 'example', '_venue': venue, 'year': '2026',
                    })

    def test_both_renderers_reject_a_duplicate_year(self):
        with tempfile.TemporaryDirectory() as directory:
            bibfile = Path(directory) / 'publications.bib'
            bibfile.write_text('''@misc{example,
  title={Publication year regression},
  author={Brandon Amos},
  abstract={A valid abstract.},
  year={2026},
  _venue={NeurIPS 2026}
}
''')
            config = {
                'file': str(bibfile),
                'name': 'Amos',
                'author_urls': {},
                'error_without_author_url': True,
                'sort_bib': True,
                'group_by_year': True,
                'include_image': False,
            }
            for renderer, context in [
                (generate.get_pub_md, generate.MARKDOWN_CONTEXT),
                (generate.get_pub_latex, generate.LATEX_CONTEXT),
            ]:
                with self.subTest(renderer=renderer.__name__):
                    with self.assertRaisesRegex(ValueError, "example.*2026.*_venue"):
                        renderer(context, config)


class PublicationAbstractTests(unittest.TestCase):
    renderers = [
        (generate.get_pub_md, generate.MARKDOWN_CONTEXT),
        (generate.get_pub_latex, generate.LATEX_CONTEXT),
    ]

    def render_publication(self, renderer, context, abstract):
        with tempfile.TemporaryDirectory() as directory:
            bibfile = Path(directory) / 'publications.bib'
            abstract_field = '' if abstract is None else f'  abstract={{{abstract}}},\n'
            bibfile.write_text('''@misc{example,
  title={Publication abstract regression},
  author={Brandon Amos},
  year={2026},
  _venue={NeurIPS},
''' + abstract_field + '}\n')
            return renderer(context, {
                'file': str(bibfile),
                'name': 'Amos',
                'author_urls': {},
                'error_without_author_url': True,
                'sort_bib': True,
                'group_by_year': True,
                'include_image': False,
            })

    def test_both_renderers_reject_missing_or_blank_abstracts(self):
        for renderer, context in self.renderers:
            for abstract in [None, '', ' \n\t ']:
                with self.subTest(renderer=renderer.__name__, abstract=abstract):
                    with self.assertRaisesRegex(ValueError, 'example.*abstract'):
                        self.render_publication(renderer, context, abstract)

    def test_both_renderers_accept_nonempty_abstracts(self):
        for renderer, context in self.renderers:
            with self.subTest(renderer=renderer.__name__):
                result = self.render_publication(renderer, context, 'A valid abstract.')
                self.assertIn('Publication abstract regression', result['details'])
                if context is generate.MARKDOWN_CONTEXT:
                    self.assertIn('A valid abstract.', result['details'])


if __name__ == '__main__':
    unittest.main()
