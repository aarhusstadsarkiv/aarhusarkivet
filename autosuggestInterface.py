import json

import requests


class AutosuggestHandler:
    def __init__(self):
        self.url = "https://aarhusiana.appspot.com/autocomplete_v3"
        self.domains = ["events", "people", "organisations", "locations", "collections"]

    def suggest(self, term, limit, domain=""):

        params = [("t", term), ("limit", limit)]
        if domain in self.domains:
            params.append(("domain", domain))
        response = requests.get(self.url, params=params)

        try:
            resp = json.loads(response.content)
            if resp.get("errors"):
                return {
                    "errors": [{"code": resp.get("status_code"), "msg": resp.get("status_msg")}]
                }
            return resp.get("result")
        except ValueError as e:
            return {"errors": [{"code": 5, "msg": e}]}
