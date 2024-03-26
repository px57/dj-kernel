# """Connect to the server for the test."""
#
# from django.conf import settings
# from django.utils import timezone
#
# from rest_framework.test import APIClient
#
# from .client import ConnectOauthApi
# from .manager import OauthManager
#
# from datetime import timedelta
# import requests, json, os
#
#
# class TestConnectOauthApi(ConnectOauthApi):
#     """
#         Client test pour oauth pour ce connecter au différents iserve.
#     """
#
#     def get_url(self, url):
#         """Format url."""
#         return os.path.join(self.iserve_url, url)
