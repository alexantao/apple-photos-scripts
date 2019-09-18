#! /usr/bin/env python3

import datetime
import glob
import os
from argparse import ArgumentParser
from shutil import move

import exiftool

# the field to extract from photo files
EXIF_DATE_FIELD = "DateTimeOriginal"
CRED = '\033[31m'
CGREEN = '\033[32m'
CEND = '\033[0m'


def run(source, output_dir):
    for dir_entry in source:
        if os.path.isdir(dir_entry):  # item in list is directory
            dir_entry = os.path.join(dir_entry, "*")

        file_list = glob.glob(dir_entry)  # generate a list of the source
        file_list.sort()  # lets just sort the list

        for original_photo in file_list:
            # print("----------------------\nTesting: ", original_photo)
            photo_basename = os.path.basename(original_photo)

            try:
                # get Metadata from file
                with exiftool.ExifTool() as metadata_tool:
                    original_date_str = metadata_tool.get_tag(EXIF_DATE_FIELD, original_photo)

                if original_date_str != None:

                    date_of_photo = datetime.datetime.strptime(original_date_str,
                                                               '%Y:%m:%d %H:%M:%S')  # transform to date obj
                    photo_year = date_of_photo.year  # separate year
                    photo_month = date_of_photo.month  # separate month
                    photo_day = date_of_photo.day  # separate day

                    # lets create directory struct as ordered
                    final_path = os.path.join(output_dir, str(photo_year))
                    if args.day or args.month:  # create full structure
                        final_path = os.path.join(final_path, str(photo_month))
                    if args.day:
                        final_path = os.path.join(final_path, str(photo_day))

                    destination_file = os.path.join(final_path, photo_basename)  # this is the final pathname
                    # create Path
                    print(CGREEN, "Moving : ", CEND, photo_basename, " -> ", destination_file)
                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)  # Directory does nor exist, create
                    move(original_photo, destination_file)
            except:  # photos whitout EXIF information or DateTimeOriginal are ignored
                print('File: "', original_photo, '" does not have Date/Time information. ', CRED, '(IGNORED)', CEND)
                continue


# Usage: ./exifdate_to_dir.py [options] <source> <output_dir>
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Prints all info about processing')
    parser.add_argument('-y', '--year', action='store_true', default=True,
                        help='Separate Photos by year (default True).')
    parser.add_argument('-m', '--month', action='store_true', default=False,
                        help='Separate Photos by month, inside year.')
    parser.add_argument('-d', '--day', action='store_true', default=False, help='Separate Photos by day, inside month.')

    parser.add_argument('source', nargs='*', help='Source files pattern or dir of the photos that will be processed')
    parser.add_argument('output_dir', nargs='?', default='./',
                        help='Destination dir of the photos (will use current directory, if omitted)')
    args = parser.parse_args()

    run(args.source, args.output_dir)
