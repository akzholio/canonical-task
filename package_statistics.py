#! /usr/bin/python
"""Package Statistics CLI tool."""

import sys
import time
import utils
from collections import Counter
from multiprocessing import Process, Manager
from utils import Colors as colors


def main():
    # Prepare args
    parser = utils.create_arg_parser()
    args = parser.parse_args()

    ok = '{}OK{}'.format(colors.GREEN, colors.ENDC)

    # Create mirror, base_dir and contents_filename.
    print('Initial setup ... ', end='')
    mirror = utils.create_ftp_mirror(args.country)
    base_dir = utils.create_base_dir(args.dist, args.comp)
    contents_filename = utils.create_contents_filename(args.architecture)
    print(ok)

    # Establish ftp connection.
    print('Establishing FTP connection ... ', end='')
    ftp = utils.create_ftp_connection(mirror, base_dir)
    print(ok)

    # Download Contents-xxx.gz file.
    print('Downloading {}{}{} ... '.format(colors.WARNING,
          contents_filename, colors.ENDC), end='')
    utils.download_contents(ftp, contents_filename)
    print(ok)

    # Destroy ftp connection as we no longer need it.
    print('Closing FTP connection ... ', end='')
    utils.destroy_ftp_connection(ftp)
    print(ok)

    # Create a Counter object to store statistics.
    package_entries = Counter()

    # Begin parsing.
    print('Parsing ... ', end='')
    with utils.gunzip_file(contents_filename) as contents_file:
        for line in contents_file.readlines():
            utils.parse_line_and_update_entries(line, package_entries)
    print(ok)

    # Get Top N packages by number of associated files.
    print('Analyzing data ... ', end='')
    top_packages = utils.get_top_packages(args.top, package_entries)
    print(ok)

    # Print stats.
    utils.print_stats(top_packages)


if __name__ == '__main__':
    main()
