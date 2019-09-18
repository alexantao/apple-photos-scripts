This repository contains some scripts useful to manipulate Apple Photos Library or work with photos files.
I used then to migrate my 800gb, 101.000 photos library from Apple Photos to digikam.

# photos-check

Not once, but several times, I tried to export a file in my Mac Photos App and got an error that the photo could not be copied. Later I discovered that the phisical file was missing, althrough it is referenced in Photos database, and even can be seen inside the App (possibly a low res version of it). 

I made this simple script that checks if the file is missing or not on the disk.
On my last check, I found out that I have 720 photos/videos missing, from a total of about 100.000. 
Tested on Photos version is 3.0.
   
For now, it just checks for the Master version, but future releases will include versions as well. 

Requires python 3, may work with python 2, but not tested.

USAGE: 
   ./check_photos_library.py directory_of_your_library 

# exifdate_to_dir

Reads EXIF data from files and move then to a directory structure like YEAR/MONTH/DAY.
You can choose the level to create. YEAR is mandatory. Will always be created.

Requires python 3 and PyExifTool, may work with python 2, but not tested.

**OPTIONS:**

    -m, --month: create MONTH directories. Result will be YEAR/MONTH
    -d, --day: create DAY directories. Result will be YEAR/MONTH/DAY
    -g, --guess: try to guess the date. Method sequence:
                   1) EXIF DateTimeOriginal
                   2) EXIF DateTime
                   3) EXIF ModifyDate
                   4) Date of creation of file from SO 

**USAGE:**
  
     ./exifdate_to_dir.py [options] <path_or_files> [output_dir]
   
   - path_or_files: if a Path, will scan all files inside and try to extract the EXIF data from then. those whose EXIF data could not be extract will be IGNORED
   - output_dir: where the files will be MOVED to. If ignored, defaults to current dir, './'

