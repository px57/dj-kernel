
from kernel.http.upload.convert.video import ffmpegConvert, getVideoConverterCommand
import os

def convert_video(modelObject, key):
    """
        @description: 
    """
    convert_field_key = key + '_converted'

    if not hasattr(modelObject, convert_field_key):
        raise Exception(modelObject.__class__.__name__ + ' does not have ' + convert_field_key)
    
    # # -> if the video is already converted, return None
    if getattr(modelObject, convert_field_key):
        return None
    
    # # -> observe if the video exists
    video = getattr(modelObject, key)
    if type(video) != str:
        try:
            path = video.path
        except:
            return None
    else:
        path = video

    if not os.path.exists(path):
        return None
    
    # -> is mp4 file extension
    if path.split('.')[-1] == 'mp4':
        setattr(modelObject, convert_field_key, True)
        modelObject.save()
        return None
    
    # -> convert the video
    cmd = getVideoConverterCommand(path)
    outputPath = ffmpegConvert(path, cmd, '-before-convert')

    setattr(modelObject, convert_field_key, True)
    setattr(modelObject, key, outputPath)
    modelObject.save()

