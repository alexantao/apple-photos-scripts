#! /usr/bin/env python3
#
#  This script checks you Photos App Library, printing
# all files that are on database but not phisically on HD.
#
#  I got this situation a lot of times, when trying to export
# some photo and got an export error, finding out later that
# the problem was that the file was not found on system file.]
#  Photos lost it. 
#
#   The Progress bar indicates number of rows processed.

import ntpath
import os
import sqlite3
import sys
from argparse import ArgumentParser

import progressbar

CRED = '\033[31m'
CGREEN = '\033[32m'
CEND = '\033[0m'


def vprint(verbose, message):
    if verbose:
        print(message)


#  Main Function
def check(verbose, exclude_versions, lib_dir, output_file):
    db_path = os.path.join(lib_dir, 'database')
    photos_db_path = os.path.join(db_path, 'photos.db')

    try:
        photos_db = sqlite3.connect(photos_db_path)
        photos_db.row_factory = sqlite3.Row
    except sqlite3.Error as erro:
        print("Problem connecting to Database: ", photos_db_path)
        print(" Error: ", erro)
        sys.exit(1)

    try:
        version_cursor = photos_db.cursor()
        master_cursor = photos_db.cursor()
        version_cursor.execute('SELECT COUNT(*) from RKVersion')
        (number_of_rows,) = version_cursor.fetchone()
        version_cursor.execute('SELECT * FROM RKVersion')
    except sqlite3.Error as erro:
        print("Problem on Database: ", photos_db_path)
        print(" Error: ", erro)
        sys.exit(1)

    vprint(verbose, "Number of items to check: " + str(number_of_rows) + "\n")
    bar = progressbar.ProgressBar(maxval=number_of_rows)

    # Processing each item of DB VERSION
    with open('%s' % output_file, 'w') as output:  # Open output File
        print("versionuuid,masterUuid,imagePath", file=output)

        for version_item in bar(iter(version_cursor.fetchone, None)):
            version_uuid = version_item['uuid']
            master_uuid = version_item['masterUuid']

            try:
                query = 'SELECT imagePath FROM RKMaster WHERE uuid="' +  master_uuid +'"'
                master_cursor.execute(query)
                imagePath = master_cursor.fetchone()[0]

            except sqlite3.Error as erro:
                print("Problem on Master Select: ", photos_db_path)
                print(" Error: ", erro)
                sys.exit(1)

            # get path from master
            full_path = os.path.join(lib_dir, 'Masters', imagePath)

            # Check if Master Version of the file exists.
            if not os.path.exists(full_path):
                vprint(verbose, "Image " + ntpath.normpath(imagePath) + CRED + " NOK " + CEND)
                # print("Master :\t UUID=", uuid, "\tArquivo: ", path, file=log_file)
                print(version_uuid + "," + master_uuid + "," + imagePath, file=output)
            else:
                vprint(verbose, "Image " + ntpath.normpath(imagePath) + CGREEN + " OK " + CEND)

        photos_db.close()


if __name__ == '__main__':
    # Options parsed from command line
    parser = ArgumentParser()
    parser.add_argument('--ev', action="store_true", default=True,
                        help='Exclude check of Version Files (Edited Photos). Scan only Master Files')
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Print All Check Files on Screen')
    parser.add_argument('library_dir', help='Path of Photos App Library to check')
    parser.add_argument('output_file', help='Output file with UUIDs found.')
    args = parser.parse_args()

    print("Checking Library: ", args.library_dir)
    check(args.verbose, True, args.library_dir, args.output_file)
