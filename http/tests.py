
from kernel.http import Response
from django.test import TestCase

class TestResponseLoadSite(TestCase):
    """
        @description:   
    """
    
    def test_without_request(self):
        """
            @description:
        """
        res = Response(request=None)
        res.get_site()