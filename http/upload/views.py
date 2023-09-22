from django.shortcuts import render
from kernel.http import Response
from .models import UploadedImage, SeecuboxFile
from .convert.video import VideoConverter
from django.conf import settings
import PIL
import os
import uuid

def compressAvatar(request, dbUploaded, image):
    """
        @description: Compresser avatar pour qu'il soit
        x. il faudrait compresser cette images pour qu'elle fasse une taille idéal de 100x100
        x. Il faut aussi veuillez à ce que le redimensionnements soit bien calculer.
    """
    # -> D'abord je commence par récupérer qu'elle est la taille de cette éléments
    path = settings.MEDIA_ROOT + dbUploaded.src.name
    image = PIL.Image.open(path)
    width, height = image.size
    image.close()

    # cmd = """
    #     convert -define jpeg:size={{IMG_WIDTH}}x{{IMG_HEIGHT}} {{img_src}}  -thumbnail 150x150^ \
    #             -gravity center -extent 150x150 {{img_src}}
    # """
    cmd = """
        convert -define jpeg:size={{IMG_WIDTH}}x{{IMG_HEIGHT}} {{img_src}}  -thumbnail 428x428^ \
                -gravity center -extent 428x428 {{img_src}}
    """
    cmd = cmd.replace('{{IMG_WIDTH}}', str(width))
    cmd = cmd.replace('{{IMG_HEIGHT}}', str(height))
    cmd = cmd.replace('{{img_src}}', path)
    os.system(cmd)

def avatar(request):
    """
        @description: Avatar modifier
    """
    res = Response()
    image = request.FILES.get('file', None)
    real_name = image.name
    extension = image.name.split('.')[-1]

    image.name = f'{uuid.uuid4().hex}.{extension}'

    dbUploaded = UploadedImage(
        src=image,
        real_name=real_name
    )
    dbUploaded.save()
    compressAvatar(request, dbUploaded, image)

    res.status = 'done'
    res.url = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.thumbUrl = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.name = image.name
    for key in request.GET:
        setattr(res, key, request.GET.get(key))
    return res.success()

def video(request):
    """
        @description: Il s'agit ici d'uploader la video en questions.
    """

    res = Response()
    image = request.FILES.get('file', None)
    real_name = image.name
    extension = image.name.split('.')[-1]
    image.name = f'{uuid.uuid4().hex}.{extension}'
    dbUploaded = UploadedImage(
        src=image,
        real_name=real_name
    )
    dbUploaded.save()

    res.status = 'done'
    res.url = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.thumbUrl = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.name = image.name
    for key in request.GET:
        setattr(res, key, request.GET.get(key))

    for_edit_video(dbUploaded)
    return res.success()

def for_edit_video(dbUploaded):
    """
        @description: Transformers
    """
    path = os.path.join(settings.MEDIA_ROOT, dbUploaded.src.name)
    if not os.path.exists(path):
        return

    splittedPath = path.split('.')
    base64Path = '.'.join(splittedPath[0:-1]) + '.html'
    gifPath = '.'.join(splittedPath[0:-1]) + '.gif'
    littleVideoPath = '.'.join(splittedPath[0:-1]) + '-little.' + splittedPath[-1]

    cmd = ' '.join([
        'ffmpeg -ss 00:00:00.0 -i',
        path,
        '-c copy -t 00:00:05.0',
        littleVideoPath
    ])
    os.system(cmd)

    cmd = ' '.join([
        'ffmpeg -i',
        littleVideoPath,
        '-vf "fps=1,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe -',
        '| convert -delay 10 - -loop 0',
        gifPath
    ])
    os.system(cmd)

    cmd = 'cat ' + gifPath + ' | base64 > ' + base64Path
    os.system(cmd)

    # VideoConverter(path, dbUploaded)

def for_order(request):
    """Add the file video to order."""
    res = Response()
    image = request.FILES.get('file', None)
    real_name = image.name
    extension = image.name.split('.')[-1]
    image.name = f'{uuid.uuid4().hex}.{extension}'
    dbUploaded = SeecuboxFile(
        src=image,
        real_name=real_name
    )
    dbUploaded.save()
    res.status = 'done'
    res.url = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.thumbUrl = settings.ADRESS_HOST + settings.MEDIA_URL + dbUploaded.src.name
    res.name = image.name
    res.real_name = real_name
    for key in request.GET:
        setattr(res, key, request.GET.get(key))
    return res.success()