
from django.conf import settings

from redis import Redis 

class Redis(Redis):
    """

    """

    def __init__(self, cache_name='default'):
        """

        """
        CACHE = settings.CACHES[cache_name]
        super_redis_params = {
            'host': 'redis',
            'port': int(CACHE['LOCATION'].split('//')[1].split(':')[1].split('/')[0]),
            'db': int(CACHE['LOCATION'].split('//')[1].split(':')[1].split('/')[1]),
        }
        super(Redis, self).__init__(**super_redis_params)

    def geoadd(self, key, *args, **kwargs):
        """
        Add a point to the geospatial index represented by the key.

        Args:
            key (str): The key of the geospatial index.
            *args (tuple): The points to add to the geospatial index.
        """
        return super(Redis, self).geoadd(key, *args, **kwargs)
    
    def geo_nearest_points(self,
        key, 
        coords, 
        radius=1000, 
        unit='m', 
        withdist=True
    ):
        """
        Find the nearest points in the radius.

        Args:
            coords (tuple): The coordinates of the reference point.
            radius (int): The radius around the reference point.
            unit (str): The unit of distance.
        """
        points = self.georadius(
            key,
            coords[0], coords[1],
            radius, 
            unit=unit, 
            withdist=withdist
        )

        if not points:
            return None

        distances = []
        objects = {}

        # -> find the nearest points, and their distances
        for point in points:
            distances.append(point[1])
            objects[point[1]] = point

        print (len(points))
        # -> sort the distances
        distances.sort()
        return {
            'id': objects[distances[0]][0],
            'distance': objects[distances[0]][1],
            'unit': unit
        }