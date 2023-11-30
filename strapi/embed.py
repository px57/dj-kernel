import requests 
import pprint

def join_path_url(url, path): 
    """
        @description: 
    """
    path = ''.join(path.split())
    if (path[0] == '/'):
        path = path[1:]

    return url + '/' + path

def put(path, data, request=None):
    """
        @description: 
    """
    url = join_path_url('http://127.0.0.1:1337/api', path)
    headers = {
        "Content-Type": "application/json"
    }

    if not request: 
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']

    req = requests.put(
        url, 
        json=data,
        headers=headers
    )
    
    if req.status_code == 200:
        return req.json()
    return None

def post(path, data, request=None):
    """
        @description: 
    """
    url = join_path_url('http://127.0.0.1:1337/api', path)
    headers = {
        "Content-Type": "application/json"
    }

    if not request: 
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']

    req = requests.post(
        url, 
        json=data,
        headers=headers
    )
    
    if req.status_code == 200:
        return req.json()
    return None
    


class StrapiObject:
    def __init__(self) -> None:
        """
            @description:
        """
        pass

class StrapiGetEmbed:
    def __init__(self, result, model, request) -> None:
        """
            @description:
        """
        self.result = result
        self.model = model
        self.request = request

    def exists(self):
        """
            @description:
        """
        if self.result is None:
            return False
        
        return len(self.result['data']) != 0

    def first(self):
        """
            @description:
        """
        if self.result is None:
            return None
        return self.result['data'][0]

    def serialize(self):
        """
            @description:
        """
        if self.result is None:
            return None
        return self.result['data']
    
    def create(self, **kwargs):
        """
            @description:
        """
        params = {
            'data': kwargs,
        }
        post('/' + self.model, params, self.request)

    def update(self, **kwargs):
        """
            @description:
        """
        for item in self.result['data']:
            params = {
                'data': kwargs,
            }
            put('/' + self.model + '/' + str(item['id']), params, self.request)

    def info(self):
        """
            @description:
        """
        pass

    def __str__(self):
        """
            @description:
        """
        return str(self.result)