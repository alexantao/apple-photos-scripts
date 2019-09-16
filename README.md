# photos-check

Not once, but several times, I tried to export a file in my Mac Photos App and got an error that the photo could not be copied. Later I discovered that the phisical file was missing, althrough it is referenced in Photos database, and even can be seen inside the App (possibly a low res version of it). 

I made this simple script that checks if the file is missing or not on the disk.
On my last check, I found out that I have 720 photos/videos missing, from a total of about 100.000. 
Tested on Photos version is 3.0.
   
For now, it just checks for the Master version, but future releases will include versions as well. 

USAGE: 
   ./check_photos_library.py directory_of_your_library 
