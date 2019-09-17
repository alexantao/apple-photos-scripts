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

Requires python 3, may work with python 2, but not tested.

USAGE: 
   ./exifdate_to_dir.py [options] <path or files> <output_dir>


TODO: Work with RAW files.
