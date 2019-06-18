import os
import json

import requests


class ResourceHandler:
    def __init__(self):
        self.host = "https://openaws.appspot.com"
        self.endpoints = {
            "records": "records_v3",
            "people": "entities",
            "locations": "entities",
            "organisations": "entities",
            "events": "entities",
            "creators": "entities",
            "collectors": "entities",
            "objects": "objects",
            "collections": "collections",
        }

    def _api_request(self, path, method="get", params=None, data=None):
        # Always returns a dict with 'status_code' plus 'result' or 'status_msg'
        if method == "get":
            r = requests.get("/".join([self.host, path]), params=params)
        else:
            r = requests.post("/".join([self.host, path]), data=data)

        try:
            r_to_dict = json.loads(r.content)
            return r_to_dict
        except ValueError as e:
            return {"status_code": 5, "status_msg": str(e)}

    def get_resource(self, collection, resource):
        r = self._api_request("/".join([self.endpoints.get(collection), resource]))

        # Generate r
        if r.get("status_code") == 0:
            return r.get("result")

        elif r.get("status_code") == 1:
            return {
                "errors": [
                    {"code": 404, "msg": "Resourcen eksisterer ikke", "id": resource}
                ]
            }
        elif r.get("status_code") == 2:
            return {
                "errors": [{"code": 404, "msg": "Resourcen er slettet", "id": resource}]
            }
        else:
            return {
                "errors": [
                    {
                        "code": r.get("status_code"),
                        "msg": r.get("status_msg"),
                        "id": resource,
                    }
                ]
            }

    # 'batch_records' from ClientInterface reformatted
    def multi_get_records(self, id_list):
        data = {"view": "record", "oasid": json.dumps(id_list)}
        return _api_request(path="resolve_records_v2", method="post", data=data)

    def get_entity_labels(self, resource_list):
        # resource_list: [('collection', '4'), ('availability', '2')]
        r = self._api_request("resolve_params", params=resource_list)

        if r.get("status_code") == 0:
            output = []
            for key, value in r.get("resolved_params").items():
                for k, v in value.items():
                    d = {"resource": key, "id": k, "label": v.get("display_label")}
                    output.append(d)
            return {"result": output}
        else:
            return {
                "errors": [{"code": r.get("status_code"), "msg": r.get("status_msg")}]
            }
