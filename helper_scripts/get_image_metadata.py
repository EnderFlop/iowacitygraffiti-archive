from PIL import Image
import PIL.ExifTags

def get_lat_long(filepath):
    #heavily modified version of https://python.plainenglish.io/reading-a-photographs-exif-data-with-python-and-pillow-a29fceafb761
    image = Image.open(filepath)
    exif_data_PIL = image._getexif()
    exif_data = {}
    for k, v in PIL.ExifTags.TAGS.items():
        if k in exif_data_PIL:
            value = exif_data_PIL[k]
        else:
            value = None

        # if len(str(value)) > 64:
        #     value = str(value)[:65] + "..."

        exif_data[v] = {"tag": k, "raw": value}

    image.close()

    #GPS Tag Info found here: https://exiftool.org/TagNames/GPS.html
    gps = exif_data["GPSInfo"]["raw"]
    try:
        north = sanatizeCoords(gps[2]) 
        west = sanatizeCoords(gps[4])
    except TypeError: #sometimes doesn't have the GPSInfo, just send their ass to null island
        north = 00.00000
        west = 00.00000
    return (north, west)

def sanatizeCoords(coords):
    # (41.0 29.0 50.6) -> 41.39506
    return float(f"{int(coords[0])}.{int(coords[1])}{str(coords[2]).replace('.', '')}")