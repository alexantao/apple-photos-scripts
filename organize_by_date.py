#! /usr/bin/env python3

import datetime
import pathlib
import shutil
from argparse import ArgumentParser

import exiftool

# the field to extract from photo files
EXIF_DATE1_FIELD = "DateTimeOriginal"
EXIF_DATE2_FIELD = "DateTime"
EXIF_DATE3_FIELD = "ModifyDate"  # Guessing from file date

# Terminal Color Codes
CRED = '\033[31m'
CGREEN = '\033[32m'
CEND = '\033[0m'


# Function to transform a string to Date
# in case the string is malformed, return None
def str_to_date(date_string):
    try:
        result = datetime.datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
    except:
        result = None

    return result


# -------------------------------------------------------------------------------------------
#     Tries to guess the date of the file using some methods (if guess is TRUE,
#  else only DateTimeOriginal is used)
def guess_date(file, metadata, guess):
    file_str_path = str(file.resolve())

    try:
        # Method 1: EXIF Field DateTimeOriginal
        result = str_to_date(metadata.get_tag(EXIF_DATE1_FIELD, file_str_path))

        # Method 2: Field DateTime
        if result is None and guess:
            result = str_to_date(metadata.get_tag(EXIF_DATE2_FIELD, file_str_path))

        # Method 3: Field FileModifiedDate
        if result is None and guess:
            result = str_to_date(metadata.get_tag(EXIF_DATE3_FIELD, file_str_path))
    except:
        result = None

    # Method 5: DateFinder. Try to discover from filename patterns
    # print("Arquivo: {0} - Data Encontrada: {1}".format(file_str_path, dateutil.parser.parse(file_str_path)))
    # search = datefinder.find_dates(file)
    # if search is not None:
    #    for date_result in search:
    #       print("Arquivo: ", file, " Data Encontrada: ", date_result)

    # Method 4: SO File Date and Time Created
    if result is None:
        if guess:
            return datetime.datetime.fromtimestamp(file.stat().st_ctime)
        else:
            return None

    return result


# -------------------------------------------------------------------------------------------
def run(source, output_dir, guess):
    for source_entry in source:
        source_path = pathlib.Path(source_entry)

        if source_path.is_dir():  # item in list is directory

            for original_photo in source_path.iterdir():

                # get Metadata from file
                with exiftool.ExifTool() as metadata_tool:
                    date_of_photo = guess_date(original_photo, metadata_tool, guess)

                if date_of_photo is not None:  # lets guess the date
                    photo_year = date_of_photo.year  # separate year
                    photo_month = date_of_photo.month  # separate month
                    photo_day = date_of_photo.day  # separate day

                    # lets create directory struct as ordered
                    final_path = pathlib.Path(output_dir) / str(photo_year)
                    if args.day or args.month:  # create full structure
                        final_path = final_path / str(photo_month)
                    if args.day:
                        final_path = final_path / str(photo_day)

                    photo_basename = original_photo.name
                    destination_file = final_path / photo_basename

                    # create Path
                    print(CGREEN, "{0}Moving :{1} {2} -> {3}".format(CGREEN, CEND, photo_basename, destination_file))

                    # os.makedirs(os.path.dirname(destination_file), exist_ok=True)  # Directory does nor exist, create
                    final_path.mkdir(exist_ok=True, parents=True)
                    shutil.move(original_photo, destination_file)
                else:
                    print(
                        'File: {0} " does not have Date/Time information. {1}(IGNORED){2}'.format(original_photo, CRED,
                                                                                                  CEND))
                    continue
        else:
            print("Source {0} is not a directory.".format(source_path))


# Usage: ./organize_by_date.py [options] -s <source> [-o output_dir]
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-m', '--month', action='store_true', default=False,
                        help='Separate Photos by month, inside year.')
    parser.add_argument('-d', '--day', action='store_true', default=False, help='Separate Photos by day, inside month.')
    parser.add_argument('-g', '--guess', action='store_true', default=False, help='Activate guessing mode.')

    parser.add_argument('-s', '--source', nargs='+',
                        help='Source dir of the photos that will be processed')
    parser.add_argument('-o', '--output_dir', nargs='?', default='./',
                        help='Destination dir of the photos (will use current directory, if omitted)')
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = './'

    run(args.source, args.output_dir, args.guess)
