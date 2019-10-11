#! /usr/bin/env python3
import datetime
import pathlib
import sys
from argparse import ArgumentParser

import exiftool

# the field to extract from photo files
EXIF_DATE1_FIELD = "DateTimeOriginal"
EXIF_DATE2_FIELD = "DateTime"
EXIF_DATE3_FIELD = "ModifyDate"  # Guessing from file date

# Terminal Color Codes
CRED = '\033[31m'
CGREEN = '\033[32m'
CORANGE = '\033[93m'
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
# Generates a String of the Year as passed by the user
def gen_year_dir(year, pattern):
    try:
        year_dir = pattern.replace("%Y", "{}")
        return year_dir.format(year)
    except:
        return pattern


# -------------------------------------------------------------------------------------------
#  Process one directory
def process_directory(directory, output, recursive, guess):
    dir_path = pathlib.Path(directory)
    output_path = pathlib.Path(output)

    if dir_path.is_dir():  # Must be a dir passed.
        for file_in_dir in dir_path.iterdir():
            if file_in_dir.is_dir() and recursive:  # item in list is directory, RECURSIVE ?
                print(f'Dir Found: {file_in_dir}. Recursive True, Processing ')
                process_directory(file_in_dir, output, recursive, guess)
            elif file_in_dir.is_file():  # Process file
                with exiftool.ExifTool() as metadata_tool:
                    date_of_photo = guess_date(file_in_dir, metadata_tool, guess)

                    if date_of_photo is not None:  # lets guess the date
                        photo_year = date_of_photo.year  # separate year
                        photo_month = date_of_photo.month  # separate month
                        photo_day = date_of_photo.day  # separate day

                        final_path = output_path / gen_year_dir(str(photo_year), args.yp)
                        if args.day or args.month:  # create full structure
                            final_path = final_path / str(photo_month)
                        if args.day:
                            final_path = final_path / str(photo_day)

                        photo_basename = file_in_dir.name
                        destination_file = final_path / photo_basename

                        if destination_file.exists():
                            print(f'File {destination_file} exists on {final_path}! {CORANGE}IGNORED{CEND}')
                        else:
                            # create Path
                            print(f'{CGREEN}Moving :{CEND} {photo_basename} -> {destination_file}')

                            final_path.mkdir(exist_ok=True, parents=True)
                            file_in_dir.replace(destination_file)
                    else:
                        print(f'File: {file_in_dir} does not have Date/Time information. {CRED}(IGNORED){CEND}')


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
def run(source, output_dir, recursive, guess):
    source_path = pathlib.Path(source)
    output_path = pathlib.Path(output_dir)

    process_directory(source_path, output_path, recursive, guess)
    sys.exit(1)


# -------------------------------------------------------------------------------------------
# Usage: ./organize_by_date.py [options] -s <source> [-o output_dir]
if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-yp', nargs='?', default='%Y',
                        help='Define a Pattern for the name of the year directory (use %Y to place the year. Ex.: %Y Albums)')
    parser.add_argument('-m', '--month', action='store_true', default=False,
                        help='Separate Photos by month, inside year.')
    parser.add_argument('-d', '--day', action='store_true', default=False, help='Separate Photos by day, inside month.')
    parser.add_argument('-g', '--guess', action='store_true', default=False, help='Activate guessing mode.')
    parser.add_argument('-s', '--source',
                        help='Source dir of the photos that will be processed')
    parser.add_argument('-o', '--output_dir', nargs='?', default='./',
                        help='Destination dir of the photos (will use current directory, if omitted)')
    parser.add_argument('-r', '--recursive', default=False, action='store_true', help='Process directory recursively.')
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = './'

    run(args.source, args.output_dir, args.recursive, args.guess)
