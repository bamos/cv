import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml
from bs4 import BeautifulSoup

import generate


class HomepageGenerationTests(unittest.TestCase):
    def test_generation_preserves_homepage_controls_and_shared_bio(self):
        data = yaml.safe_load(Path('cv.yaml').read_text())
        context = generate.MARKDOWN_CONTEXT
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(context, 'BUILD_DIR', directory), \
                patch.object(context, '_output_file', str(Path(directory) / 'cv.md')), \
                patch.object(generate, 'add_repo_data', return_value='40k+'), \
                patch.object(generate, 'get_scholar_stats', return_value={'citations': '15k+', 'h_index': 47}), \
                contextlib.redirect_stdout(io.StringIO()):
            generate.process_resume(context, data, preview=False)
            homepage = (Path(directory) / 'cv.md').read_text()
            bio = (Path(directory) / 'bio.md').read_text()

        html = BeautifulSoup(homepage, 'html.parser')
        self.assertEqual([section['id'] for section in html.select('.home-section')],
                         ['publications', 'code', 'talks'])
        for name in ['publications', 'code', 'talks']:
            self.assertEqual(html.select_one(f'#tab-{name}')['href'], f'#{name}')
            self.assertIsNotNone(html.select_one(f'#{name} > h2[id="-{name}"]'))
        self.assertIsNotNone(html.select_one('#about-intro'))
        self.assertIsNotNone(html.select_one('#bio[hidden]'))
        self.assertIsNotNone(html.select_one('#last-updated'))
        self.assertIn('{% include_relative bio.md %}', homepage)
        self.assertEqual(bio.split('---', 2)[2].strip(), data['about_formal'].strip())
        self.assertIn('[here](https://github.com/bamos/presentations)', homepage)
        self.assertNotIn('padding-right:0', str(html.select_one('#talks tr td:nth-child(2)')))
        self.assertNotIn('<style>', homepage)
        self.assertNotIn('javascript:', homepage)
        self.assertTrue(html.select('.abstract-box'))
        for abstract in html.select('.abstract-box'):
            self.assertTrue(abstract.has_attr('data-nosnippet'))
            self.assertIsNotNone(html.select_one(f'button[aria-controls="{abstract["id"]}"][aria-expanded="false"]'))
        for image in html.select('.publicationImg'):
            self.assertTrue(image.get('alt'))


if __name__ == '__main__':
    unittest.main()
