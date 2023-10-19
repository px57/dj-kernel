"""
    @description:
"""

from base64 import b64decode
from .embed import StrapiGetEmbed
import requests
import os
import json
import jwt

STRAPI_JWT_DECODED = {};

def join_path_url(url, path): 
    """
        @description: 
    """
    path = ''.join(path.split())
    if (path[0] == '/'):
        path = path[1:]

    return url + '/' + path

def strapi_post(path, data, request=None):
    """
        @description: 
    """
    url = join_path_url('http://127.0.0.1:1337/api', path)
    headers = {
        "Content-Type": "application/json"
    }

    if request is not None:
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']

    req = requests.post(
        url, 
        json=data,
        headers=headers
    )
    
    if req.status_code == 200:
        return req.json()
    return None

def strapi_get(model, filter, request=None):
    """
        @description: 
    """
    url = join_path_url('http://127.0.0.1:1337/api', model)
    headers = {
        "Content-Type": "application/json"
    }
    if request is not None:
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']

    queryParams =''
    for key in filter:
        queryParams += key + '=' + str(filter[key]) + '&'
    url += '?' + queryParams
    req = requests.get(url, headers=headers)

    if req.status_code == 200:
        embed = StrapiGetEmbed(req.json(), model, request)
    else:
        embed = StrapiGetEmbed(None, model, request)
    StrapiGetEmbed.url = url
    StrapiGetEmbed.headers = headers
    return embed

def strapi_exists(path, request=None):
    """
        @description: 
    """
    

def strapi_userId(request):
    """
        @description: 
    """
    return strapi_user(request).get('id', None)

def strapi_user(request):
    """
        @description: 
    """
    jwtToken = request.META['HTTP_AUTHORIZATION'].split(' ')[1]

    if jwtToken in STRAPI_JWT_DECODED:
        return STRAPI_JWT_DECODED[jwtToken]
    
    resp = os.popen('node ./node/jwt-decode.js ' + jwtToken)

    try:
        jwtDecoded = json.loads(resp.read())
    except:
        return None
    
    STRAPI_JWT_DECODED[jwtToken] = jwtDecoded
    return jwtDecoded



if __name__ == "__main__":
    content = strapi_post('/auth/forgot-password', {
        'email': 'projeta618@gmail.com',
    })
    

