#! /usr/bin/env python3

#  This script renames the Photos.app XMP generated file
# relative of the file passed to Digikam XMP filename
from argparse import ArgumentParser
from pathlib import Path

XMP_SUFFIX = ".xmp"

def rename_xmp_file(file):
    print(f'Processing file: {file}')
    file_path = Path(file).resolve()
    if file.is_file():
        file_basepath = file_path.parent
        file_filename = file_path.name

        file_xmpphoto = file_path.with_suffix(XMP_SUFFIX.upper())

        # let's find the correspondent XMP of the files
        file_xmpdigikam = file_basepath / (file_filename + XMP_SUFFIX)

        print(f'    Base: {file_basepath}')
        print(f'    Full: {file_filename}')
        print(f'    Photo: {file_xmpphoto}')
        print(f'    Digikam: {file_xmpdigikam}')


        if file_xmpphoto.is_file():
            print(f'Renaming: {file_xmpphoto} -> {file_xmpdigikam}')
            file_xmpphoto.replace(file_xmpdigikam)

def run(filedir):

    file_path = Path(filedir).resolve()

    if file_path.is_dir():
        for file in file_path.iterdir():
            if file.suffix.lower() !=  XMP_SUFFIX:
                rename_xmp_file(file)
    else:
        rename_xmp_file(file_path)



# -------------------------------------------------------------------------------------------
# Usage: ./organize_by_date.py [options] -s <source> [-o output_dir]
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filedir', help='Directory to process or File (original, not the XMP).')
    args = parser.parse_args()

    run(args.filedir)

