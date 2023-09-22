
from .models import UploadedImage
from django.conf import settings
from PIL import Image
import os
import json
import subprocess

def getUploadedImage(ico):
    if ico is None:
        return None

    if type(ico) == str:
        url = ico
    else:
        url = ico.get('url')

    url = url[len(settings.ADRESS_HOST) + len(settings.MEDIA_URL): ]
    return url


response_error_get_image = {'x': 0, 'y': 0, 'duration': 5, 'mime': 'image/png'};
def get_image_size(src):
    try:
        im = Image.open(src)
        size = im.size # width, height
    except:
        return response_error_get_image
    return {'x': size[0], 'y': size[1], 'duration': 5}

def get_video_information(src):
    # -> Récupérer la valeur excact de chaque vidéo pour pouvoir aller de l'avant ou de l'arrieres.
    video = subprocess.getoutput('ffprobe -v error -show_entries format=duration  -show_entries stream=width,height  -print_format json ' + src)
    video = json.loads(video)
    return {
        'x': video['streams'][0]['width'],
        'y': video['streams'][0]['height'],
        'duration': video['format']['duration']
    }

MEDIA_GET_SIZE = [
    {
        'mime_list': ['image/png', 'image/jpeg', 'image/gif', 'image/x-icon', 'image/tiff', 'image/webp'],
        'function': get_image_size
    },
    {
        'mime_list': ['video/x-msvideo', 'video/mpeg', 'video/ogg', 'video/webm', 'video/3gpp', 'video/3gpp2'],
        'function': get_video_information
    }
]
def get_media_size(ico):
    """Calculer la taille des media cette éléments pour pouvoir ainsi l'adapter."""
    src = '.' + settings.MEDIA_URL + ico
    if not os.path.exists(src):
        return response_error_get_image

    # "file --mime-type -b " + src
    mime = subprocess.getoutput("file --mime-type -b " + src)
    for MEDIA in MEDIA_GET_SIZE:
        if mime in MEDIA['mime_list']:
            meta = MEDIA['function'](src)
            meta['mime'] = mime
            return meta

    # TODO -> Communiquer une erreur pour pouvoir prendre en charge ce format
    return response_error_get_image
