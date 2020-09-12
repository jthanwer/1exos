import os
import sys
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_file(file, instance_id, enonce_id=None):
    basename = 'Correction' if enonce_id else 'Exercice'
    old_filename = file.name
    extension = old_filename.split('.')[-1].lower()
    fileid = instance_id
    if extension != 'pdf':
        image = Image.open(file)

        # -- Retrieve the good orientation of the photo
        img_exif = image.getexif()
        if img_exif:
            key_orientation = None
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    key_orientation = orientation
                    break
            try:
                exif_items = dict(img_exif.items())
                if key_orientation:
                    if exif_items[key_orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif_items[key_orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif_items[key_orientation] == 8:
                        image = image.rotate(90, expand=True)
            except:
                pass

        output = BytesIO()
        format_file = 'JPEG' if extension.lower() == 'jpg' else extension.upper()

        try:
            image.save(output, format=format_file, quality=40)
        except OSError:
            image = image.convert("RGB")
            image.save(output, format=format_file, quality=40)
        output.seek(0)

        if enonce_id:
            filename = '{}_{}_{}.'.format(basename, enonce_id, fileid) + extension
        else:
            filename = '{}_{}.'.format(basename, fileid) + extension
        file = InMemoryUploadedFile(output, 'ImageField', filename,
                                    'image/{}'.format(format_file.lower()),
                                    sys.getsizeof(output), None)
    else:
        if enonce_id:
            file.name = '{}_{}_{}.'.format(basename, enonce_id, fileid) + extension
        else:
            file.name = '{}_{}.'.format(basename, fileid) + extension

    return file
