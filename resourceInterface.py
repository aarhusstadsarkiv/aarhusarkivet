import os
import json

import requests
from six.moves.urllib.parse import urlencode

import searchInterface
import settings


class ResourceHandler():

    def __init__(self):
        self.url = "https://openaws.appspot.com"
        # self.facets = settings.FACETS
        self.filters = settings.QUERY_FILTERS
        self.searchAPI = searchInterface.SearchHandler()
        # self.service_url = 'https://openaws.appspot.com'
        self.resource_endpoints = {
            'records': 'records_v3',
            'people': 'entities',
            'locations': 'entities',
            'organisations': 'entities',
            'events': 'entities',
            'creators': 'entities',
            'collectors': 'entities',
            'objects': 'objects',
            'collections': 'collections'
        }

    def _api_request(self, url, params=None):
        # Always returns a dict with 'status_code' plus 'result' or 'error'
        response = requests.get(url, params=params)
        try:
            response_to_dict = json.loads(response.content)
            return response_to_dict
        except ValueError as e:
            return {'status_code': 5, 'error': e}

    def get_resource(self, collection, resource):

        def format_record(record):
            def _generate_hierarchical_structure(string_list):
                # Takes a list of strings with possible '/' as hierarchical seperators
                # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

                def addHierItem(key, hierStruct, hierList, parent):
                    if parent != "":
                        path = parent + "/" + key
                    else:
                        path = key

                    hierItem = {"label": key, "path": path}

                    childrenList = []
                    children = hierStruct.get(key)
                    for childKey in sorted(children):
                        addHierItem(childKey, children, childrenList, path)

                    if len(childrenList) > 0:
                        hierItem["children"] = childrenList

                    hierList.append(hierItem)

                hierList = []
                hierStruct = {}
                for item in sorted(string_list):
                    splitList = item.split("/")

                    curLevel = hierStruct
                    for key in splitList:
                        hierData = curLevel.get(key, {})
                        curLevel[key] = hierData
                        curLevel = hierData

                for key in sorted(hierStruct):
                    addHierItem(key, hierStruct, hierList, "")

                return hierList

            result = {}
            for key, value in record.items():
                # First handle all specialcases
                # If 'series' then treat uniquely
                if key == 'series':
                    output = []
                    currentLevel = []
                    urlpath = {}
                    collection = record.get('collection')

                    if collection:
                        urlpath['collection'] = collection.get('id')

                    for idx in value.split('/'):
                        currentLevel.append(idx)
                        urlpath['series'] = '/'.join(currentLevel)
                        level = {}
                        level['label'] = idx
                        level['new_link'] = urlencode(urlpath)
                        output.append(level)
                    result[key] = output

                # If key is list of strings
                elif key in ['admin_tags']:
                    output = []
                    for idx in value:
                        item = {}
                        item['label'] = idx
                        item['new_link'] = urlencode({key: _id})
                        output.append(item)
                    result[key] = output

                elif key in ['collection_tags']:
                    result[key] = _generate_hierarchical_structure(value)
                    
                elif key in ['resources']:
                    result[key] = value

                # If key is dict
                elif isinstance(value, dict) and key in self.filters:
                    # If id-dict
                    if value.get('id'):
                        _id = value.get('id')
                        label = value.get('label')
                        item = {}
                        item['label'] = label
                        item['id'] = _id
                        item['new_link'] = urlencode({key: _id})
                        result[key] = item
                    else:
                        result[key] = value

                # If key is list (of id-dicts)
                elif isinstance(value, list) and key in self.filters:
                    output = []

                    for _dict in value:

                        # hierarchical concept or entity
                        if isinstance(_dict.get('id'), list):
                            hierarchy = []
                            for i, v in enumerate(_dict.get('id')):
                                item = {}
                                item['id'] = v
                                item['label'] = _dict.get('label')[i]
                                item['new_link'] = '='.join([key, str(v)])
                                hierarchy.append(item)
                            output.append(hierarchy)

                        # flat concept or entity
                        else:
                            _id = _dict.get('id')
                            label = _dict.get('label')
                            item = {}
                            item['id'] = _id
                            item['label'] = label
                            item['new_link'] = urlencode({key: _id})
                            output.append(item)

                    result[key] = output

                else:
                    result[key] = value

            return result

        def format_collection(collection):
            def _list_collection_structures(collection_id):
                # Used to fetch series and collection_tags as facets (incl. count) when requesting a collection

                def _generate_hierarchical_structure(dict_list):
                    # Takes a list of strings with possible '/' as hierarchical seperators
                    # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

                    def addHierItem(key, hierStruct, hierList, parent):
                        if parent != "":
                            path = parent + "/" + key
                        else:
                            path = key

                        hierItem = {"label": key, "path": path}

                        childrenList = []
                        children = hierStruct.get(key)
                        for childKey in sorted(children):
                            addHierItem(childKey, children, childrenList, path)

                        if len(childrenList) > 0:
                            hierItem["children"] = childrenList

                        hierList.append(hierItem)

                    # hierarchical = False
                    hierList = []
                    hierStruct = {}
                    # Extra conversion (relative to the clientInterface-function), as amazon returns list of dicts,
                    # not just list of strings
                    string_list = [e.get("value") for e in dict_list]

                    for item in sorted(string_list):
                        splitList = item.split("/")
                        # if len(splitlist) > 1:
                        #     hierarchical = True

                        curLevel = hierStruct
                        for key in splitList:
                            hierData = curLevel.get(key, {})
                            curLevel[key] = hierData
                            curLevel = hierData

                    for key in sorted(hierStruct):
                        addHierItem(key, hierStruct, hierList, "")

                    return hierList

                collection_facets = self.searchAPI.get_collection_info(collection_id)
                
                # Convert to dicts with label, id and children keys, like the classic 'series'
                series = []
                if collection_facets.get("series"):
                    series_list = collection_facets["series"].get("buckets")
                    series = _generate_hierarchical_structure(series_list)

                collection_tags = []
                if collection_facets.get("collection_tags"):
                    collection_tags_list = collection_facets["collection_tags"].get("buckets")
                    collection_tags = _generate_hierarchical_structure(collection_tags_list)

                return series, collection_tags

            # Enhance with dynamically fetched structures from searchengine
            series, collection_tags = _list_collection_structures(collection.get('id'))
            collection['series'] = series
            collection['collection_tags'] = collection_tags

            # Pop 'structure'-key - at least for now. Reintroduce when we can work with descriptions on
            # individual series-levels
            collection.pop('structure', None)

            return collection

        response = self._api_request('/'.join([self.url,
                                               self.resource_endpoints.get(collection),
                                               resource]))

        if response.get('status_code') == 0:
            result = response.get('result')
            if collection == 'records':
                return format_record(result)
            elif collection == 'collections':
                return format_collection(result)
            else:
                return result

        elif response.get('status_code') == 1:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen eksisterer ikke',
                    'id': resource
                }
            }
        elif response.get('status_code') == 2:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen er slettet',
                    'id': resource
                }
            }
        else:
            return {
                'error': {
                    'code': response.get('status_code'),
                    'msg': response.get('status_msg'),
                    'id': resource
                }
            }

    def get_labels(self, resource_list):
        # resource_list: [{'resource': 'collection', 'id': 4}, {'resource': 'availability', 'id': 2}]
        r = self._api_request("/".join([self.url, "resolve_params"]), params=resource_list)

        if r.get("status_code") == 0:
            output = []
            for key, value in r.get("resolved_params").iteritems():
                for k, v in value.items():
                    d = {
                        "resource": key,
                        "id": k,
                        "label": v.get("display_label")
                    }
                    output.append(d)
            return {"status_code": 0, "result": output}
        else:
            return r
