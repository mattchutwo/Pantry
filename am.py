# Matthew Chu
# Methods for app data
import os
import datetime


# Void Method to seperate outputed text
def Abyss():
    print("-" * 25)  # prints "-" 25 times


# Boolean Method to validate the existence of the given file(path)
# Returns True if file exists; False if else
def CheckFileExists(path):
    # if(Path(path).is_file()):
    if os.path.isfile(path):
        return True
    else:
        return False
