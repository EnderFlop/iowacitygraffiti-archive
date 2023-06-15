import json
import sys
import shutil
import os
import re

def get_image_name(img_path):
    img_path = img_path.split("\\")[-1]
    img_path = img_path.split(".")[0]
    return img_path

def get_location_name(img_path):
    img_path = img_path.split("\\")[-2]
    return img_path

def get_date(img_path):
    img_path = img_path.split("\\")[-3]
    img_path = img_path.replace(".", "/")
    return img_path

#files are organized ...../TEMP/{Location Name}/{Image Name}.jpg
def create_description():
    img_path = sys.argv[1]
    img_name = get_image_name(img_path)
    location = get_location_name(img_path)
    date = get_date(img_path)
    print(f"\nNAME: {img_name}\nLOCATION: {location}\nDATE: {date}\n")
    artist = input("Artist: ")
    notes = input("Notes: ")
    data = {
        "artist": artist,
        "date_photographed": date,
        "location": location,
        "img_name": img_name,
        "notes": notes
    }
    obj = json.dumps(data)

    #the following uses a regex to match "Streetart" with "Streetart (40)"
    folders = os.listdir("../photos/")
    regex = re.compile(r"\b" + re.escape(artist) + r"\b")
    try:
        valid_folder = list(filter(regex.match, folders))[0]
    except IndexError: #path does not exist
        os.makedirs(f"../photos/{artist}")
        valid_folder = artist

    artist_folder = f"../photos/{valid_folder}"
    #write json
    with open(f"{artist_folder}/{img_name}.json", "w") as outfile:
        outfile.write(obj)
    #move image
    shutil.move(img_path, artist_folder)

#update below values depending on when and were the photos were taken
create_description()
