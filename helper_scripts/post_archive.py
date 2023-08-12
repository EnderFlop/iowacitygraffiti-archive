import os
import json
from PIL import Image, ImageOps

# A bunch of utilities to run before each commit to generate metadata, thumbnails, and everything else.

def rename_preview():
    print("Renaming Preview Images")
    for dir_name in os.listdir(".\photos"):
        path = os.path.join(".\photos", dir_name)
        photos = os.listdir(path)
        if "PREVIEW.jpg" in photos:
            continue
        old_filename = photos[0].split(".")[0]
        os.rename(path + f"\{old_filename}.jpg", path + f"\PREVIEW.jpg")
        os.rename(path + f"\{old_filename}.json", path + f"\PREVIEW.json")

def get_rid_of_JPGs():
    print("Ridding the World of .JPGs")
    for dir_name in os.listdir(".\photos"):
        path = os.path.join(".\photos", dir_name)
        photos = os.listdir(path)
        offenders = [photo for photo in photos if photo[-4:] == ".JPG"]
        if len(offenders) == 0:
            continue
        for photo in offenders:
            old_filename = photo.split(".")[0]
            os.rename(path + f"\{old_filename}.JPG", path + f"\{old_filename}.jpg")

def renameArtist(oldName, newName):
    os.rename(f".\photos\{oldName}", f".\photos\{newName}")
    jsons = [file for file in os.listdir(f".\photos\{newName}") if file[-5:] == ".json"]
    for j in jsons:
        with open(f".\photos\{newName}\{j}", "r") as file:
            data = json.load(file)
        data["artist"] = newName
        print(data)
        with open(f".\photos\{newName}\{j}", "w") as file:
            file.write(json.dumps(data))
        

#renameArtist("Iris", "IRIS")

def generate_thumbnails():
    print("Generating Thumbnails")
    for dir_name in os.listdir(".\photos"):
        path = os.path.join(".\photos", dir_name)
        photos = os.listdir(path)
        for img_file in photos:
            image_name = img_file.split(".")[0]
            #skip jsons...................thumbnails.................images with thumbnails already................and the favorite artist images
            if (("json" in img_file) or ("thumbnail" in img_file) or (f"{image_name}_thumbnail.jpeg" in photos) or image_name == dir_name):
                continue
            new_path = os.path.join(path, img_file)
            image = Image.open(new_path)
            image = ImageOps.exif_transpose(image) #needed to keep vertical photos vertical
            image.thumbnail((500, 500))
            image.save(f".\photos\{dir_name}\{image_name}_thumbnail.jpeg", "jpeg", optimize=True, quality=10)

def delete_thumbnails():
    print("Deleting Thumbnails!")
    for dir_name in os.listdir(".\photos"):
        path = os.path.join(".\photos", dir_name)
        photos = os.listdir(path)
        for img_file in photos:
            if "thumbnail" in img_file:
                os.remove(f".\photos\{dir_name}\{img_file}")

def generate_metadata():
    print("Generating Metadata File")
    all_artists_dict = {}
    for folder in os.listdir(".\photos"):
        artist_dict = {}
        artist_dict["name"] = folder
        artist_dict["favorite"] = folder in IMPORTANT_ARTIST_LIST #if the artist gets their own page art and description. list is hardcoded below.

        photo_count = 0
        artist_dict["photos"] = {}
        for file in os.listdir(f".\photos\{folder}"):
            if ".jpg" not in file:
                continue
            photo_count += 1
            name = file[:-4] #remove ".jpg"

            #add location information
            with open(f"./photos/{folder}/{name}.json") as meta:
                data = json.load(meta)
                location = data["location"]
                if location not in artist_dict["photos"].keys():
                    artist_dict["photos"][location] = []
            artist_dict["photos"][location].append(name)

        artist_dict["count"] = photo_count
        all_artists_dict[folder] = artist_dict
    obj = json.dumps(all_artists_dict)
    with open(".\\artist_meta.json", "w") as outfile:
        outfile.write(obj)

def generate_location_json():
    print("Generating Location File")
    count_dict = {}
    with open(".\location_coords.json", "r") as file:
        coords = json.load(file)
        for location in coords.keys():
            count_dict[location] = 0

        for folder in os.listdir(".\photos"):
            for file in os.listdir(f".\photos\{folder}"):
                if ".json" not in file:
                    continue
                with open(f".\photos\{folder}\{file}") as meta:
                    data = json.load(meta)
                    location = data["location"]
                    if location not in coords.keys():
                        coords[location] = {}
                        coords[location]["lat_long"] = ""
                    count_dict[location] += 1
                    # if location == "S Dubuque St":
                    #     print(data)

                #LOCATION CHANGER
                # with open(f".\photos\{folder}\{file}", "w") as meta:
                #     if data["location"] == "Pentacrest Sidewalk down N Clinton St":
                #         data["location"] = "Pentacrest Sidewalk down Clinton St"
                #         print(data)
                #     meta.write(json.dumps(data))
        
    for location, count in count_dict.items():
        coords[location]["count"] = count

    with open(".\location_coords.json", "w") as file:
        file.write(json.dumps(coords))

#for when i'm archiving a ton but not organizing them. I want to record the location coords while I know them.
def generate_new_location_from_temp(filepath):
    with open(".\location_coords.json", "r") as file:
        processed_locations = json.load(file)

    for folder in os.listdir(filepath):
        for location in os.listdir(filepath + "/" + folder):
            if location not in processed_locations:
                    processed_locations[location] = {}
                    processed_locations[location]["lat_long"] = ""
                    processed_locations[location]["count"] = 0

    with open(".\location_coords.json", "w") as file:
        file.write(json.dumps(processed_locations))

def generate_favorite_artist_json():
    print("Generating Favorite Artist File")
    with open("./favorites.json") as file:
        data = json.load(file)

    for artist in IMPORTANT_ARTIST_LIST:
        if artist not in data.keys():
            data[artist] = {}
            data[artist]["description"] = ""
            data[artist]["tags_with"] = ""
            data[artist]["groups"] = ""
    
    with open("./favorites.json", "w") as file:
        file.write(json.dumps(data))

#to make a new "favorite" artist: add them to below list and run post-archive. then, type in their bio in favorites.json. Then add a cut out tag of theirs in their folder as {ARITST}.png
IMPORTANT_ARTIST_LIST = [""]

#generate_new_location_from_temp("c:/Users/EnderFlop/Desktop/temp graffiti storage")

def rename_all_photos():
    #for each folder
        #for each photo (.jpg or .JPG)
            #rename to be "whatever.a"

    for folder in os.listdir(".\photos"):
        print(folder)
        for file in os.listdir(f".\photos\{folder}"):
            if ".a" in file:
                img_name = file[:-2]
                os.rename(f".\photos\{folder}\{file}", f".\photos\{folder}\{img_name}.jpg")
        
    
    #dont need to update jsons because we're switching to .jpg back right after

#rename_all_photos()

def main():
    rename_preview()
    get_rid_of_JPGs()
    #files are renamed BEFORE anything else is generated, keep this order.
    generate_thumbnails()
    generate_metadata()
    generate_location_json()
    generate_favorite_artist_json()
    pass

if __name__ == "__main__":
    pass
    main()


#TODO:
    #change all names to be in order: 1.jpg, 2.jpg, etc. do whatever to fix github .JPG
    #look thru Unknown and sort out all of those into categories. 
    # Then, go thru any 1 tag artists and move to Unknown if applicable.