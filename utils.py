"""Utils module.

This module contains methods needed for downloading
and parsing "Contents" indices file from Debian mirror.
"""

import argparse
import ftplib
import gzip
from collections import Counter


class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def create_ftp_mirror(country: str) -> str:
    return f'ftp.{country}.debian.org'


def create_base_dir(dist: str, comp: str) -> str:
    return f'debian/dists/{dist}/{comp}/'


def create_contents_filename(architecture: str) -> str:
    return f'Contents-{architecture}.gz'


def create_ftp_connection(mirror: str, base_dir: str) -> ftplib.FTP:
    ftp = ftplib.FTP(mirror)  # Create FTP connection for given mirror
    ftp.login()  # Anonymous login
    ftp.cwd(base_dir)  # Point to right directory
    return ftp


def destroy_ftp_connection(ftp: ftplib.FTP):
    try:
        ftp.quit()
    except ftplib.error_reply:  # pragma: no cover
        ftp.close()


def download_contents(ftp: ftplib.FTP, filename: str) -> str:
    with open(filename, 'wb') as local_file:
        ftp.retrbinary(f'RETR {filename}', local_file.write)


def gunzip_file(filename: str):
    return gzip.open(f'{filename}', 'rt')


def get_top_packages(top: int, data: Counter) -> Counter:
    return data.most_common(top)


def get_packages(line: str) -> list:
    line = line.split()
    # we don't need to store filename, presence of package is enough
    packages = line[1].split(',')
    return packages


def parse_line_and_update_entries(line: str, entries: dict):
    packages = get_packages(line)
    for package in packages:
        add_package_to_entries(package, entries)


def add_package_to_entries(package: str, entries: dict):
    if package in entries:
        entries[package] += 1
    else:
        entries[package] = 1


def print_stats(data: dict):  # pragma: no cover
    print('{}{:<4}{:<40} {:<10}{}'.format(Colors.HEADER,
          '', 'Package name', 'Number of files', Colors.ENDC))
    row_index = 0
    for package, num_of_files in data:
        row_index += 1
        print('{:<3} {}{:<40}{} {}{:<10}{}'.format(row_index, Colors.CYAN,
              package, Colors.ENDC, Colors.GREEN, num_of_files, Colors.ENDC))


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='package_statistics', description='Package Statistics')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1')
    parser.add_argument('architecture', metavar='A',
                        type=str, help='selected architecture')
    parser.add_argument('--top', type=int, default=10,
                        help='top number of packages')
    parser.add_argument('--country', type=str, default='uk',
                        help='nearest country, defaults to UK')
    parser.add_argument('--dist', type=str, default='stable',
                        help='distribution, defaults to "stable"')
    parser.add_argument('--comp', type=str, default='main',
                        help='component, defaults to "main"')
    return parser
