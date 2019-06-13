import json

import requests


class AutocompleteHandler():

    def __init__(self):
        self.url = "https://aarhusiana.appspot.com/autocomplete_v3"
        self.domains = ['events', 'people', 'organisations', 'locations', 'collections']
    
    def get(self, term, limit, domain=""):

        params = [('t', term), ('limit', limit)]
        if domain in self.domains:
            params.append(('domain', domain))
        response = requests.get(self.url, params=params)

        try:
            payload = json.loads(response.content)
            return payload.get('result')
        except ValueError as e:
            return {'status_code': 5, 'status_msg': e}