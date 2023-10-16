
from kernel.http import Response
from django.test import TestCase
from kernel.http.classobjects import Url

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


class TestUrlObject(TestCase):
    """
        @description: Test the url class object
    """

    def test_compose_url_with_little_part(self):
        """
            @description: Creer une url complete avec peu de parametres
        """
        url = Url(
            # full_url='https://www.google.com.br',
            protocol='https',
            host='www.google.com.br',
            pathname='/',
            queryParams={
                'test': 1234,
                'ppup': 'oaeuaoeu'
            }
        )
        self.assertEqual(url.get_full_url(), 'https://www.google.com.br/?test=1234&ppup=oaeuaoeu')

    def test_passfullurl__get__fullurl(self):
        """
            @description: Passar uma url completa e pegar ela completa
        """
        url = Url(
            full_url='https://www.google.com.br',
        )
        self.assertEqual(url.get_full_url(), 'https://www.google.com.br')

    