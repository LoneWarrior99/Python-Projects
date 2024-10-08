"""
Followed along with guide online, cited in README.md.
Figuring out what else I can add to this base code other than more metadata fields.
This is a work in progress as I try to incorporate new techniques during my journey.
Only modification so far is a banner. Looking into more meta fields.

"""


from argparse import ArgumentParser
import pikepdf
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from moviepy.editor import VideoFileClip
import pyfiglet

##Dependancies needed
## pip install Pillow
## pip install Pikepdf
## pip install moviepy

parser = ArgumentParser(
  prog='metadata extractor',
  description='This program pulls metadata from files of multiple types',
  epilog='Thanks for looking!'
)

# Set up the arguments
parser.add_argument('-e', "--extension", help="Use the syntax -e to specify the file extension")
parser.add_argument('-f', "--file", help="Use the syntax -f to specify the file to extract metadata from")

# Parsing command line arguments
args = parser.parse_args()

ascii_banner = pyfiglet.figlet_format("METADATA EXTRACTOR")
print(ascii_banner)



def get_pdf_metadata(pdf_file):
    pdf = pikepdf.Pdf.open(pdf_file)
    return dict(pdf.docinfo)


def get_image_metadata(image_file):
    image = Image.open(image_file)
    # Get metadata
    info_dict = {
        "Filename": image.filename,
        "Size": image.size,
        "Height": image.height,
        "Width": image.width,
        "Format": image.format,
        "Image Mode": image.mode,
        "Animation": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
   
        
    }
    # Extract EXIF data
    exifdata = image.getexif()
    if exifdata is not None:
        for tag_id, value in exifdata.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'GPSInfo':
                gps_data = {}
                for key in value.keys():
                    gps_tag = GPSTAGS.get(key, key)
                    gps_data[gps_tag] = value[key]
                info_dict['GPSData'] = gps_data
            else:
                try:
                    # Decode bytes
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    info_dict[tag] = value
                except UnicodeDecodeError:
                    # Skip metadata that cannot be decoded
                    continue
    return info_dict

def get_available_metadata_fields(file):
    clip = VideoFileClip(file)
    metadata = clip.reader.infos
    clip.reader.close()
    return list(metadata.keys())


def get_media_metadata(media_file):
    clip = VideoFileClip(media_file)
    metadata = {
        "Duration": clip.duration,
        "Size": clip.size,
        "FPS": clip.fps,
        "Frame Count": clip.reader.nframes,
        "Creation Date": clip.reader.infos.get('creation_time'),
        "Bitrate": clip.reader.infos.get('bit_rate'),
        "Channels": clip.reader.infos.get('channels'),
        "Sample Rate": clip.reader.infos.get('sample_rate'),
        "Title": clip.reader.infos.get('title'),
        "Author": clip.reader.infos.get('author'),
        "Album": clip.reader.infos.get('album'),
        "Year": clip.reader.infos.get('year'),
        "Artist": clip.reader.infos.get("artist"),
        "Creator": clip.reader.infos.get("creator"),
        "Owner": clip.reader.infos.get("owner"),
        "Producer": clip.reader.infos.get("producer"),
        "Company": clip.reader.infos.get("company"),
        "Copyright": clip.reader.infos.get("copyright"),
        "License": clip.reader.infos.get("license"),
        # Add any other desired metadata fields here
    }
    
    clip.close()
    return metadata




def main():
    if args.extension == "pdf":
        metadata = get_pdf_metadata(args.file)
        print(metadata)
    elif args.extension.lower() in ["jpeg", "jpg", "png"]:
        metadata = get_image_metadata(args.file)
        print(metadata)
    else:
        # Try extracting metadata using other methods
        if os.path.isfile(args.file):
            file_extension = os.path.splitext(args.file)[1].lower()[1:]
            if file_extension not in ["pdf", "jpeg", "jpg", "png"]:
                metadata = get_media_metadata(args.file)
                print(metadata)
            else:
                print("Unrecognized file extension.")
        else:
            print("Invalid file path.")


if __name__ == "__main__":
    main()
