"""Unit tests for utils module."""

import argparse
import ftplib
import unittest
import utils
from collections import Counter
from unittest.mock import patch


class TestPackageStatisticsMethods(unittest.TestCase):

    def test_create_ftp_mirror(self):
        """Tests creating an FTP mirror string."""
        mirror = utils.create_ftp_mirror('uk')
        self.assertEqual(mirror, 'ftp.uk.debian.org')

    def test_create_base_dir(self):
        """Tests creating base_dir."""
        base_dir = utils.create_base_dir('stable', 'main')
        self.assertEqual(base_dir, 'debian/dists/stable/main/')

    def test_create_contents_filename(self):
        """Tests creating the contents file, Contents-xxx.gz."""
        contents_filename = utils.create_contents_filename(
            'amd64')
        self.assertEqual(contents_filename, 'Contents-amd64.gz')

    @patch('ftplib.FTP', autospec=True)
    def test_create_ftp_connection(self, mock_ftp_constructor):
        """Tests creating a mock FTP connection."""
        mock_ftp = mock_ftp_constructor.return_value
        mirror = utils.create_ftp_mirror('uk')
        base_dir = utils.create_base_dir('stable', 'main')
        utils.create_ftp_connection(mirror, base_dir)
        mock_ftp_constructor.assert_called_with(mirror)
        self.assertTrue(mock_ftp.login.called)
        mock_ftp.cwd.assert_called_with(base_dir)

    @patch('ftplib.FTP', autospec=True)
    def test_destroy_ftp_connection(self, mock_ftp_constructor):
        """Tests destructing a mock FTP connection."""
        mock_ftp = mock_ftp_constructor.return_value
        mirror = utils.create_ftp_mirror('uk')
        base_dir = utils.create_base_dir('stable', 'main')
        utils.create_ftp_connection(mirror, base_dir)
        utils.destroy_ftp_connection(mock_ftp)
        self.assertTrue(mock_ftp.quit.called)

    @patch('ftplib.FTP', autospec=True)
    def test_download_contents(self, mock_ftp_constructor):
        """Tests downloading .gz file through mock FTP connection."""
        mock_ftp = mock_ftp_constructor.return_value
        mirror = utils.create_ftp_mirror('uk')
        base_dir = utils.create_base_dir('stable', 'main')
        contents_filename = utils.create_contents_filename('amd64')
        utils.download_contents(mock_ftp, contents_filename)
        self.assertTrue(mock_ftp.retrbinary.called)

    @patch('gzip.open', autospec=True)
    def test_gunzip_file(self, mock_gzip_open):
        """Tests unpacking .gz file, gzip.open method is being mocked."""
        contents_filename = utils.create_contents_filename(
            'amd64')
        utils.gunzip_file(contents_filename)
        mock_gzip_open.assert_called_with(contents_filename, 'rt')

    def test_get_top_packages(self):
        """Tests getting top N packages."""
        N = 3
        package_file_count = Counter(
            {'package1': 1, 'package2': 3, 'package3': 4, 'package4': 2})
        result = utils.get_top_packages(3, package_file_count)
        self.assertEqual(
            result, [('package3', 4), ('package2', 3), ('package4', 2)])

    def test_get_packages(self):
        line = 'bin/busybox             utils/busybox,shells/busybox-static'
        packages = utils.get_packages(line)
        self.assertEqual(packages, ['utils/busybox', 'shells/busybox-static'])

    def test_add_package_to_entries(self):
        package1 = 'package1'
        package2 = 'package2'
        entries = {}

        utils.add_package_to_entries(package1, entries)
        self.assertEqual(entries, {'package1': 1})

        utils.add_package_to_entries(package2, entries)
        self.assertEqual(entries, {'package1': 1, 'package2': 1})

        utils.add_package_to_entries(package1, entries)
        self.assertEqual(entries, {'package1': 2, 'package2': 1})

    def test_parse_line_and_update_entries(self):
        line = 'bin/busybox             utils/busybox,shells/busybox-static'
        entries = {}

        utils.parse_line_and_update_entries(line, entries)
        self.assertEqual(
            entries, {'utils/busybox': 1, 'shells/busybox-static': 1})

    def test_create_arg_parser(self):
        parser = utils.create_arg_parser()

        self.assertEqual(type(parser), argparse.ArgumentParser)


if __name__ == '__main__':
    unittest.main()
