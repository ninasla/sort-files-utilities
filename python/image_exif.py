# =========================================================
# Dependencies

# Python 3.x https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html
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

class MyCam:
    def __init__(self, exifname, nickname, timediff):
        self.exifname = exifname
        self.nickname = nickname
        self.timediff = timediff

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

##### ----------------- print camera information for cams listed in cams array 
def print_mycams_info(cams):
    for cam in cams:
        print(cam.exifname + " : " + cam.nickname)
        print(cam.timediff)

##### ----------------- find cam in cams array by Exif name
def find_cam_by_exifname(cams, camname):
    for cam in cams:
        if camname == cam.exifname:
            return cam
    return None

##### ----------------- create and print new name for test
def create_file_name(fpath, num, cams):
    exif_dict = piexif.load(fpath)
    print ("-------------------")
    datetime_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
    datetime_object = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
    print (datetime_object)
    fixed_datetime = datetime_object
    model = "none"
    camera = exif_dict["0th"][piexif.ImageIFD.Model].decode("utf-8")
    print (camera)
    thecam = find_cam_by_exifname(cams, camera)
    if thecam is not None:
        model = thecam.nickname
        fixed_datetime = datetime_object + thecam.timediff
    #if camera == "NIKON D5500":
        #model = "_D55"
        #fixed_datetime = datetime_object + timedelta(seconds=24,hours=8)
    #elif camera == "SM-N920W8":
        #model = "_SNote"
        #fixed_datetime = datetime_object
    #elif camera == "Canon PowerShot SX50 HS": 
        #model = "_SX50"
        #fixed_datetime = datetime_object + timedelta(minutes=9, hours=7) 
		#, minutes=9
    print(fixed_datetime)

    filename = fixed_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    #filename = (datetime_str.replace(":", "-")).replace(" ", "_")
    print (filename)
    filename += "_"
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
# Configuration
# =========================================================

dirpath = os.getcwd()
filetypes = ['.jpg','.jpeg', '.tiff', '.JPG', '.JPEG', '.TIFF']

## Berlin 2016
#mycams = [MyCam("NIKON D5500", "D55", timedelta(seconds=24,hours=8)), MyCam("SM-N920W8","SNote", timedelta(0)), MyCam("Canon PowerShot SX50 HS", "SX50", timedelta(minutes=9, hours=7))]

## Paris 2013
mycams = [MyCam("Canon PowerShot SX160 IS", "SX160", timedelta(hours=21)), MyCam("Canon PowerShot SX200 IS", "SX200", timedelta(hours=9))]


# =========================================================
# main
# =========================================================

## print configuration data
print ("########## SETUP DATA ##########")
print (dirpath)
print_mycams_info(mycams)
print ("################################")
## Step 1 List all files in current folder


files = [ fn for fn in os.listdir(dirpath) if any(fn.endswith(ext) for ext in filetypes) ]
#print (files)

i = 1
for file in files:
    pict = os.path.join(dirpath, file)
    print(pict)
    print_file_info(pict)
    newname = create_file_name(pict, i, mycams)
    print ("------------- new name " + newname)
    i = i+1
    ####################### !!!!!! Next step will RENAME file
    os.rename(pict, os.path.join(dirpath, newname))


