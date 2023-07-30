import random
import shutil
import json
import sys
import os

#takes in three files: the main photo (.jpg), the metadata (.json), and *optionally* the thumbnail (.jpeg)
#changes the artist name in the metadata, then moves all the files.

def rename_artist():
    #get file paths
    photo = ""
    metadata = ""
    thumbnail = ""
    for arg in sys.argv:
        file_ending = arg[-4:]
        if file_ending == "jpeg":
            thumbnail = arg
        elif file_ending == "json":
            metadata = arg
        elif file_ending == ".jpg":
            photo = arg

    print("\n\n" + photo)

    if not (photo and metadata):
        input("Needs a .jpg and and a .json!~")
        return
    
    #ask for new artist, check existence
    new_name = input("New Artist Name: ")
    new_artist_folder = f"..\photos\{new_name}"
    if not (os.path.exists(new_artist_folder)):
        input("That artist doesn't exist!~")
        return

    #write new artist to metadata
    with open(metadata, "r") as file:
        data = json.load(file)
    old_name = data["artist"]
    data["artist"] = new_name
    with open(metadata, "w") as file:
        file.write(json.dumps(data))

    #handle if file is named PREVIEW
    photo_name = photo.split("\\")[-1].replace(".jpg", "")
    if photo_name == "PREVIEW":
        rand_new_name = f"MOVED_{random.randint(0, 999)}"

        #rename photo
        new_photo = photo.replace("PREVIEW", rand_new_name)
        os.rename(photo, new_photo)
        photo = new_photo

        #rename metadata and write new photo name
        new_meta = metadata.replace("PREVIEW", rand_new_name)
        os.rename(metadata, new_meta)
        metadata = new_meta
        with open(metadata, "r") as file:
            data = json.load(file)
        data["img_name"] = rand_new_name
        with open(metadata, "w") as file:
            file.write(json.dumps(data))

        #rename thumbnail
        if (thumbnail):
          new_thumbnail = thumbnail.replace("PREVIEW", rand_new_name)
          os.rename(thumbnail, new_thumbnail)
          thumbnail = new_thumbnail

    #move files
    shutil.move(photo, new_artist_folder)
    shutil.move(metadata, new_artist_folder)
    if (thumbnail):
        shutil.move(thumbnail, new_artist_folder)
    
    #delete old folder if empty
    if len(os.listdir(f"..\photos\{old_name}")) == 0:
        os.rmdir(f"..\photos\{old_name}")

rename_artist()