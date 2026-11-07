import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class PushGuardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / 'cv'
        self.remote = self.root / 'remote.git'
        self.repo.mkdir()
        self.run_command('git', 'init', '--bare', str(self.remote))
        self.git('init', '--initial-branch=main')
        self.git('config', 'user.name', 'Guard Test')
        self.git('config', 'user.email', 'guard@example.com')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        shutil.copyfile(Path(__file__).resolve().parents[1] / 'Makefile',
                        self.repo / 'Makefile')
        (self.repo / 'templates').mkdir()
        (self.repo / 'templates' / 'example').touch()
        (self.repo / 'publications').mkdir()
        (self.repo / 'publications' / 'example.bib').touch()
        (self.repo / 'cv.yaml').write_text('name: Test\n')
        generator = self.repo / 'generate.py'
        generator.write_text('#!/bin/sh\ntouch stage-started\nexit 1\n')
        generator.chmod(0o755)
        self.git('add', '.')
        self.git('commit', '-m', 'Initial source')
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-u', 'origin', 'main')

    def run_command(self, *arguments, check=True):
        return subprocess.run(arguments, cwd=self.repo, check=check,
                              text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)

    def git(self, *arguments):
        return self.run_command('git', *arguments)

    def commit_change(self):
        (self.repo / 'cv.yaml').write_text('name: Changed\n')
        self.git('add', 'cv.yaml')
        self.git('commit', '-m', 'Change source')

    def assert_push_rejected(self, message):
        result = self.run_command('make', '-j8', 'push', check=False)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)
        self.assertFalse((self.repo / 'stage-started').exists(), result.stdout)

    def test_clean_pushed_commit_passes(self):
        self.run_command('make', 'check-pushed')

    def test_uncommitted_changes_block_before_building(self):
        (self.repo / 'cv.yaml').write_text('name: Changed\n')
        with self.subTest(state='unstaged'):
            self.assert_push_rejected('Commit all changes')
        self.git('add', 'cv.yaml')
        with self.subTest(state='staged'):
            self.assert_push_rejected('Commit all changes')
        self.git('reset', '--hard', 'HEAD')
        (self.repo / 'new-file').touch()
        self.git('config', 'status.showUntrackedFiles', 'no')
        with self.subTest(state='untracked'):
            self.assert_push_rejected('Commit all changes')

    def test_unpushed_commit_blocks_until_pushed(self):
        self.commit_change()
        self.assert_push_rejected('Push the current CV commit')
        self.git('push')
        self.run_command('make', 'check-pushed')

    def test_missing_upstream_blocks(self):
        self.git('branch', '--unset-upstream')
        self.assert_push_rejected('git push -u')

    def test_detached_head_blocks(self):
        self.git('checkout', '--detach')
        self.assert_push_rejected('git push -u')

    def test_local_upstream_does_not_count_as_pushed(self):
        self.git('branch', 'local-upstream')
        self.git('branch', '--set-upstream-to=local-upstream')
        self.assert_push_rejected('git push -u')

    def test_fetch_failure_blocks(self):
        self.git('remote', 'set-url', 'origin', str(self.root / 'missing.git'))
        self.assert_push_rejected('Could not read from remote repository')

    def test_stale_remote_tracking_branch_does_not_pass(self):
        original = self.git('rev-parse', 'HEAD').stdout.strip()
        self.commit_change()
        self.git('push')
        self.run_command('git', '--git-dir', str(self.remote),
                         'update-ref', 'refs/heads/main', original)
        self.assert_push_rejected('Push the current CV commit')


if __name__ == '__main__':
    unittest.main()
