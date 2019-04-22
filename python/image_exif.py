# =========================================================
# Dependencies

# pip install piexif
# =========================================================


import piexif
import os
from datetime  import datetime, timedelta


#TODO

# create list of pairs in log file (new name - old name - camera) in case names will need to be restored

# create class Pict with counter and all necessary data variables
# create file name from Pict vriables according to user requirement
# class Pict version 1 should have datetime model oldfilename counter


# =========================================================
# Definitions
# =========================================================

##### ----------------- printing all metadata from one file
def print_all_file_info(fpath):
    exif_dict = piexif.load(fpath)
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

##### ----------------- printing datetime and camera model from one file
def print_file_info(fpath):
    exif_dict = piexif.load(fpath)
    print (exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal])
    print (exif_dict["0th"][piexif.ImageIFD.Model])


##### ----------------- create and print new name for test
def create_file_name(fpath, num):
    exif_dict = piexif.load(fpath)
    print ("-------------------")
    datetime_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
    datetime_object = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
    print (datetime_object)
    fixed_datetime = datetime_object
    camera = exif_dict["0th"][piexif.ImageIFD.Model].decode("utf-8")
    print (camera)
    if camera == "NIKON D5500":
        model = "_D55"
        fixed_datetime = datetime_object + timedelta(seconds=24,hours=8)
    elif camera == "SM-N920W8":
        model = "_SNote"
        #fixed_datetime = datetime_object
    elif camera == "Canon PowerShot SX50 HS": 
        model = "_SX50"
        fixed_datetime = datetime_object + timedelta(minutes=9, hours=7) 
		#, minutes=9
    print(fixed_datetime)

    filename = fixed_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    #filename = (datetime_str.replace(":", "-")).replace(" ", "_")
    print (filename)
    filename += model
    filename += "_"
    filename += str(num)
    filename += ".jpg"
    return filename



# create list of files in folder


#picts = []
#for root, dirs, files in os.walk(r'F:\ninasla\python'):
#    for file in files:
#        if file.endswith('.jpg') or file.endswith('.jpeg'):
#            picts.append(file)




# =========================================================
# main
# =========================================================

## Step 1 List all files in current folder
path = os.getcwd()
print (path)
files = os.listdir(path)
print (files)

i = 1
for file in files:
    pict = os.path.join(path, file)
    print(pict)
    #newname = create_file_name(pict, i)
    #print ("new name " + newname)
    #i = i+1
    #print("####################### " + str(i))
    #os.rename(pict, os.path.join(path, newname))
    