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
    main_db_path = os.path.join(db_path, 'photos.db')
    proxy_db_path = os.path.join(db_path, 'photos.db')

    try:
        main_db = sqlite3.connect(main_db_path)
        main_db.row_factory = sqlite3.Row
        proxy_db = sqlite3.connect(proxy_db_path)
        proxy_db.row_factory = sqlite3.Row
    except sqlite3.Error as erro:
        print("Problem connecting to Database: ", main_db_path)
        print(" Error: ", erro)
        sys.exit(1)

    try:
        dbcursor = main_db.cursor()
        dbcursor.execute('SELECT COUNT(*) from RKMaster')
        (number_of_rows,) = dbcursor.fetchone()
        dbcursor.execute('SELECT * FROM RKMaster')
    except sqlite3.Error as erro:
        print("Problem on Database: ", main_db_path)
        print(" Error: ", erro)
        sys.exit(1)

    vprint(verbose, "Number of items to check: " + str(number_of_rows) + "\n")
    bar = progressbar.ProgressBar(maxval=number_of_rows)

    # Processing each item of DB
    with open('%s' % output_file, 'w') as output:  # Open output File
        for masteritem in bar(iter(dbcursor.fetchone, None)):
            uuid = masteritem['uuid']
            path = os.path.join(lib_dir, 'Masters', masteritem['imagePath'])

            # Check if Master Version of the file exists.
            if not os.path.exists(path):
                vprint(verbose, "Check Master" + ntpath.normpath(masteritem['imagePath']) + CRED + " NOK " + CEND)
                # print("Master :\t UUID=", uuid, "\tArquivo: ", path, file=log_file)
                print(uuid, file=output)
            else:
                vprint(verbose, "Check Master " + ntpath.normpath(masteritem['imagePath']) + CGREEN + " OK " + CEND)

            # if not exclude_versions:
            #     # Let's Verify if there are versions left and if they exists
            #     version_cursor = main_db.cursor()
            #     version_cursor.execute('SELECT * FROM RKVersion WHERE masterUuid=?', [uuid])
            #
            #     edited_paths = []
            #     unadjusted_count = 0
            #
            #     # Finding edited photo Verions
            #     for version in iter(version_cursor.fetchone, None):
            #         edited_path = []
            #
            #         # ---- PHASE 1  ------
            #         # Find out if there are edited versions of the photo
            #         if version['adjustmentUuid'] != 'UNADJUSTEDNONRAW':
            #             version_uuid = version['adjustmentUuid']
            #
            #             adjust_cursor = proxy_db.cursor()
            #             adjust_cursor.execute('SELECT * FROM RKModelResource WHERE resourceTag=?',
            #                                   [version['adjustmentUuid']])
            #             for resource in iter(adjust_cursor.fetchone, None):
            #                 if resource['attachedModelType'] == 2 and resource['resourceType'] == 4:
            #                     res_filename = version['filename']
            #
            #                     # Check if Master Version of the file exists.
            #                     full_file = ntpath.join(ntpath.dirname(masteritem['imagePath']), res_filename)
            #                     if res_filename != None and not os.path.exists(full_file):
            #                         vprint(verbose, "     Check Version : " + full_file + CRED + " NOK " + CEND)
            #                         print(version_uuid, file=output)

        main_db.close()
        proxy_db.close()


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
