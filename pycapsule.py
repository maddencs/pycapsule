import requests


class PyCapsule():
    xml_headers = {'Content-Type': 'application/xml',
                'Accept': 'text/xml'
    def __init__(self, **kwargs):
        self.base_url = kwargs.pop("base_url", None)
        self.api_key = kwargs.pop("api_key", None)

    def add(self, *args, **kwargs):
        """Add a new object to capsule"""
        end_point = self.base_url + '/api/' + args[0]
        r = requests.post(end_point, headers=self.headers)

