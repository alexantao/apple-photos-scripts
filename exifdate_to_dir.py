#! /usr/bin/env python3

import glob

from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import os
import datetime
from argparse import ArgumentParser
from shutil import move

#     This program analyses the EXIF data from a photo file,
#   takes the date it was shot and moves the file to a subdirectory
#   structure like: YEAR/MONTH/DAY, acording to the options passed
#
#     It is good to structure your photo library that programs like
#   Digikam is watching.

#-------------------------------------------------------------------
# Function to extract aoo EXIF information from a file.
# Returns en EMPTY dictionary if none found
def get_exif_data(path):
    tags = {}
    if os.path.isfile(path):
        image = Image.open(path)
        try:
            image_info = image._getexif()
            for tag, value in image_info.items():
                key = TAGS.get(tag, tag)
                tags[key] = value
        finally:
            return tags
    else:
        return tags
#-------------------------------------------------------------------
# Main program function
def run(source, output_dir):

# 1. Gera a lista dos arquivos passados
# 2. Para cada arquivo:
#   2.1 - Lê as informações no EXIF do arquivo
#   2.2 - Recupera a data
#   2.3 - Cria diretório do ano/mes/dia
#   2.4 - Move o arquivo para o diretório (verificar se já existe lá !)

    if os.path.isdir(source):
        source += '/*'

    file_list = glob.glob(source)
    file_list.sort()                                    # lets just sort the list
    #print("List to test:", file_list)

    for original_photo in file_list:
        print("----------------------\nTesting: ", original_photo)
        photo_basename = os.path.basename(original_photo)
        tags = get_exif_data(original_photo)
        if len(tags) > 0:
            try: # first, separate year, month and date from EXIT
                original_date_str = tags['DateTimeOriginal']                                        # get original EXIF date
                date_of_photo = datetime.datetime.strptime(original_date_str, '%Y:%m:%d %H:%M:%S')  # transform to date obj
                photo_year = date_of_photo.year                                                     # separate year
                photo_month = date_of_photo.month                                                   # separate month
                photo_day = date_of_photo.day                                                       # separate day

                # lets create directory struct as ordered
                final_path = os.path.join(output_dir, str(photo_year))
                if args.day or args.month:       # create full structure
                    final_path = os.path.join(final_path, str(photo_month))
                if args.day:
                    final_path = os.path.join(final_path, str(photo_day))

                destination_file = os.path.join(final_path, photo_basename)             # this is the final pathname
                # create Path
                print("Moving : ", photo_basename, " -> ", destination_file)
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)           # Directory does nor exist, create
                #move(original_photo, destination_file)

            except:  #photos whitout EXIF information or DateTimeOriginal are ignored
                print('File: "', original_photo, '" does not have Date/Time information.')
                continue



# Usage: ./exifdate_to_dir.py [options] <source> <output_dir>
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Prints all info about processing')
    parser.add_argument('-y', '--year', action='store_true', default=True, help='Separate Photos by year (default True).')
    parser.add_argument('-m', '--month', action='store_true', default=False, help='Separate Photos by month, inside year.')
    parser.add_argument('-d', '--day', action='store_true', default=False, help='Separate Photos by day, inside month.')

    parser.add_argument('source', help='Source files pattern or dir of the photos that will be processed')
    parser.add_argument('output_dir', help='Destination dir of the photos')
    args = parser.parse_args()

    run(args.source, args.output_dir)
