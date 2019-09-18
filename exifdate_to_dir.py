#! /usr/bin/env python3

import datetime
import glob
import os
from argparse import ArgumentParser
from shutil import move

import exiftool

# the field to extract from photo files
EXIF_DATE1_FIELD = "DateTimeOriginal"
EXIF_DATE2_FIELD = "DateTime"
EXIF_DATE3_FIELD = "ModifyDate"  # Guessing from file date

# Terminal Color Codes
CRED = '\033[31m'
CGREEN = '\033[32m'
CEND = '\033[0m'


# -------------------------------------------------------------------------------------------
#     Tries to guess the date of the file using some methods (if guess is TRUE,
#  else only DateTimeOriginal is used)
#         original_date_str = metadata_tool.get_tag(EXIF_DATE1_FIELD, original_photo)
def guess_date(file, metadata, guess):
    # print("Guessing Date/Time:", file, guess)
    # Method 1: EXIF Field DateTimeOriginal
    original_date_str = metadata.get_tag(EXIF_DATE1_FIELD, file)

    # Method 2: Field DateTime
    if original_date_str is None and guess:
        original_date_str = metadata.get_tag(EXIF_DATE2_FIELD, file)

    # Method 3: Field FileModifiedDate
    if original_date_str is None and guess:
        original_date_str = metadata.get_tag(EXIF_DATE3_FIELD, file)

    # Method 4: File Date and Time Created
    if original_date_str is None:
        if guess:
            return datetime.datetime.fromtimestamp(os.stat(file).st_ctime)
        else:
            return None

    return datetime.datetime.strptime(original_date_str, '%Y:%m:%d %H:%M:%S')


# -------------------------------------------------------------------------------------------


def run(source, output_dir, guess):
    for dir_entry in source:
        if os.path.isdir(dir_entry):  # item in list is directory
            dir_entry = os.path.join(dir_entry, "*")

        file_list = glob.glob(dir_entry)  # generate a list of the source
        file_list.sort()  # lets just sort the list

        for original_photo in file_list:

            # get Metadata from file
            with exiftool.ExifTool() as metadata_tool:
                date_of_photo = guess_date(original_photo, metadata_tool, guess)

            if date_of_photo is not None:  # lets guess the date
                photo_year = date_of_photo.year  # separate year
                photo_month = date_of_photo.month  # separate month
                photo_day = date_of_photo.day  # separate day

                # lets create directory struct as ordered
                final_path = os.path.join(output_dir, str(photo_year))
                if args.day or args.month:  # create full structure
                    final_path = os.path.join(final_path, str(photo_month))
                if args.day:
                    final_path = os.path.join(final_path, str(photo_day))

                photo_basename = os.path.basename(original_photo)
                destination_file = os.path.join(final_path, photo_basename)  # this is the final pathname
                # create Path
                print(CGREEN, "Moving : ", CEND, photo_basename, " -> ", destination_file)
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)  # Directory does nor exist, create
                move(original_photo, destination_file)
            else:
                print('File: "', original_photo, '" does not have Date/Time information. ', CRED, '(IGNORED)', CEND)
                continue


# Usage: ./exifdate_to_dir.py [options] <source> <output_dir>
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-m', '--month', action='store_true', default=False,
                        help='Separate Photos by month, inside year.')
    parser.add_argument('-d', '--day', action='store_true', default=False, help='Separate Photos by day, inside month.')
    parser.add_argument('-g', '--guess', action='store_true', default=False, help='Activate guessing mode.')

    parser.add_argument('source', nargs='*', help='Source files pattern or dir of the photos that will be processed')
    parser.add_argument('output_dir', nargs='?', default='./',
                        help='Destination dir of the photos (will use current directory, if omitted)')
    args = parser.parse_args()

    run(args.source, args.output_dir, args.guess)
