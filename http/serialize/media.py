
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile


def serialize_image_fields(request, picture):
    """Serializer l'images en questions pour que tout fonctionne."""
    if not hasattr(picture, 'name'):
        return None;

    if picture.name[0:7] == '/assets':
        return picture.name
    return settings.ADRESS_HOST + settings.MEDIA_URL  + picture.name

def serialize_file_fields(request, file):
    """Serializer l'images en questions pour que tout fonctionne."""
    file_type = type(file)
    
    if file.name is None:
        return None
    
    return settings.ADRESS_HOST + settings.MEDIA_URL  + file.name
    
def serialize_phone_number(request, phone_number):
    """Serialize aussi le numéro de téléphones."""
    if type(phone_number) is str:
        return {'country_code': None, 'number': None}

    if phone_number is None:
        return {'country_code': None, 'number': None}

    return {
        'country_code': phone_number.country_code,
        'number': phone_number.national_number
    };

def serialize_size_video(request, file):
    """Récupérer la tailles de cette éléments."""
    return {'x': 0, 'y': 0}
