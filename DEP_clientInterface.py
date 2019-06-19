import os
import json
from copy import deepcopy

import requests
from six.moves.urllib.parse import urlencode

import serviceInterface
import settings


class Client:
    def __init__(self):
        self.facets = settings.FACETS
        # self.filters = settings.QUERY_FILTERS
        self.filters = settings.QUERY_PARAMS
        self.service = serviceInterface.Service()
        self.service_url = "https://openaws.appspot.com"
        self.resources = {
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

    # def batch_records(self, id_list):
    #     if id_list:
    #         url = "https://openaws.appspot.com/resolve_records_v2"
    #         data = {"view": "record", "oasid": json.dumps(id_list)}
    #         response = requests.post(url, data=data)
    #         try:
    #             payload = json.loads(response.content)
    #             if payload.get("status_code") == 0:
    #                 return payload.get("result")
    #         except ValueError as e:
    #             return {"status_code": 5, "status_msg": e}
    #     else:
    #         return []

    # def _get_request(self, url, params=None):
    #     response = requests.get(url, params=params)
    #     try:
    #         response_to_dict = json.loads(response.content)
    #         return response_to_dict
    #     except ValueError as e:
    #         return {"status_code": 5, "error": e}

    # def list_facets_v2(self):
    #     def encode(key, val):
    #         utf8_param = [(key, val)]
    #         return urlencode(utf8_param)

    #     facets = self.service.list_facets()
    #     result = {}

    #     for facet in facets:
    #         out = {}
    #         for b in facets[facet].get("buckets"):
    #             b["add_link"] = encode(facet, b.get("value"))
    #             out[b.get("value")] = b
    #         result[facet] = out
    #     return {"total_facets": self.facets, "active_facets": result}

    # def _generate_new_link(self, key, value=None):
    #     """Takes one dict of key(s) and value(s) OR two strings"""
    #     if value:
    #         # value = str(value) if isinstance(value, int) else value
    #         return self._urlencode_old({key: value})
    #     else:
    #         return self._urlencode_old(key)

    # def _urlencode_old(self, params, decode=True):
    #     path = {}
    #     if type(params) == dict:
    #         iterable = params.items()
    #     else:
    #         iterable = params
    #     for key, value in iterable:

    #         if key in path:
    #             # path[key] += ';' + unicode(value).encode('utf-8')
    #             path[key] += ";" + value
    #         else:
    #             # path[key] = unicode(value).encode('utf-8')
    #             path[key] = value

    #     return urlencode(path)

    # def list_resources(self, query_params=None):
    #     def _generate_views(params, view):
    #         output = []
    #         views = [
    #             {
    #                 "label": "Listevisning",
    #                 "value": "list",
    #                 "icon": "fas fa-list",  # 'view_list'
    #             },
    #             {
    #                 "label": "Galleri-visning",
    #                 "value": "gallery",
    #                 "icon": "fas fa-th",  # 'view_module'
    #             },
    #         ]

    #         if params:
    #             stripped_params = [(t[0], t[1]) for t in params if t[0] != "view"]
    #         else:
    #             stripped_params = []

    #         for option in views:
    #             current = {}
    #             current["label"] = option.get("label")
    #             current["icon"] = option.get("icon")
    #             if option.get("value") == view:
    #                 current["selected"] = True
    #             else:
    #                 current["link"] = _urlencode(
    #                     stripped_params + [("view", option.get("value"))]
    #                 )
    #             output.append(current)
    #         return output

    #     def _generate_sorts(params, sort, direction):
    #         sorts = [
    #             {
    #                 "label": "Ældste dato først",
    #                 "sort": "date_from",
    #                 "icon": "fas fa-long-arrow-alt-up",  # 'arrow_upward'
    #                 "direction": "asc",
    #             },
    #             {
    #                 "label": "Nyeste dato først",
    #                 "sort": "date_to",
    #                 "icon": "fas fa-long-arrow-alt-down",  # 'arrow_downward'
    #                 "direction": "desc",
    #             },
    #             {"label": "Relevans", "sort": "_score", "direction": "desc"},
    #         ]
    #         output = []

    #         if params:
    #             stripped_params = [
    #                 (t[0], t[1])
    #                 for t in params
    #                 if t[0] not in ["sort", "direction", "start"]
    #             ]
    #         else:
    #             stripped_params = []

    #         for option in sorts:
    #             current = {}
    #             current["icon"] = option.get("icon")
    #             current["label"] = option.get("label")
    #             if option.get("sort") == sort and option.get("direction") == direction:
    #                 current["selected"] = True
    #             else:
    #                 current["link"] = _urlencode(
    #                     stripped_params
    #                     + [
    #                         ("sort", option.get("sort")),
    #                         ("direction", option.get("direction")),
    #                     ]
    #                 )
    #             output.append(current)
    #         return output

    #     def _generate_sizes(params, size):
    #         sizes = [20, 50, 100]
    #         output = []

    #         if params:
    #             stripped_params = [(t[0], t[1]) for t in params if t[0] != "size"]
    #         else:
    #             stripped_params = []

    #         for option in sizes:
    #             current = {}
    #             current["label"] = option
    #             if option == size:
    #                 current["selected"] = True
    #             else:
    #                 current["link"] = _urlencode(stripped_params + [("size", option)])
    #             output.append(current)
    #         return output

    #     def _generate_filters_v2(filters, params):
    #         # Takes filters-array of filters and adds view- and remove-links
    #         for f in filters:
    #             # If resolve_params has a display_label equal to "ID Missing"
    #             if f.get("error"):
    #                 continue

    #             key = f.get("key")
    #             value = f.get("value")
    #             negated = f.get("negated")

    #             # View_link
    #             # 'label' indicates an id-based filter, which has
    #             # an id and has been resolved
    #             if f.get("label"):
    #                 if key == "collection":
    #                     f["view_link"] = "/".join(["collections", value])
    #                 else:
    #                     f["view_link"] = "/".join([key, value])

    #             # Remove_link
    #             # If positive collection, also remove series
    #             # negative collection-params works like normal param
    #             if key == "collection" and not negated:
    #                 new_params = [
    #                     (k, v)
    #                     for k, v in params
    #                     if k not in ["collection", "series", "start"]
    #                 ]
    #                 f["remove_link"] = _urlencode(new_params)
    #             else:
    #                 new_params = [(k, v) for k, v in params if k not in ["start"]]
    #                 original_key = "-" + key if negated else key
    #                 f["remove_link"] = _urlencode(
    #                     new_params, remove=(original_key, value)
    #                 )

    #             # Inverse_link
    #             # If negated, replace with positive, vice versa
    #             # exception: if positive collection, remove series-param, as
    #             # it follows the positive collection
    #             if negated:
    #                 new_params = [(k, v) for k, v in params if k not in ["start"]]
    #                 f["invert_link"] = _urlencode(
    #                     new_params, insert=(key, value), remove=("-" + key, value)
    #                 )
    #             else:
    #                 if key == "collection":
    #                     new_params = [
    #                         (k, v)
    #                         for k, v in params
    #                         if k not in ["collection", "series"]
    #                     ]
    #                     f["invert_link"] = _urlencode(
    #                         new_params, insert=("-" + key, value)
    #                     )
    #                 else:
    #                     new_params = [(k, v) for k, v in params if k not in ["start"]]
    #                     f["invert_link"] = _urlencode(
    #                         new_params, insert=("-" + key, value), remove=(key, value)
    #                     )

    #             if key in ["people", "organisations"]:
    #                 response = self._get_request(
    #                     "https://openaws.appspot.com/entities/" + value
    #                 )
    #                 if response.get("status_code") == 0:
    #                     entity = response.get("result")

    #                     if entity.get("is_creative_creator"):
    #                         f["creator_link"] = "creators=" + value
    #                     if entity.get("is_creator"):
    #                         f["creator_link"] = "collectors=" + value

    #         return filters

    #     # def _generate_facets_v2(facets, params=None):

    #     #     def _generate_facet(name, active_facets, params):

    #     #         def _recursive(name, total_facets, active_facets, params):

    #     #             for d in total_facets:
    #     #                 _id = d.get('id')

    #     #                 if _id in active_facets.keys():
    #     #                     d['count'] = active_facets.get(_id)

    #     #                     current = (name, _id)
    #     #                     if params and (current in params):
    #     #                         rm_params = [x for x in params if x != current]
    #     #                         d['remove_link'] = _urlencode_v2(rm_params)
    #     #                         # i['remove_link'] = _urlencode(params,
    #     #                         #                               remove=current)
    #     #                     elif params:
    #     #                         add_params = params + [current]
    #     #                         d['add_link'] = _urlencode_v2(add_params)
    #     #                         # i['add_link'] = _urlencode(params,
    #     #                         #                            insert=current)
    #     #                     else:
    #     #                         d['add_link'] = _urlencode_v2([current])

    #     #                     if d.get('children'):
    #     #                         _recursive(name, d.get('children'),
    #     #                                    active_facets, params)

    #     #             return total_facets

    #     #         facet_label = self.facets[name].get('label')
    #     #         total_facets = deepcopy(self.facets[name].get('content'))
    #     #         linked_tree = _recursive(name, total_facets, active_facets, params)

    #     #         return {"label": facet_label, 'content': linked_tree}

    #     #     output = {}
    #     #     for facet_name in facets:
    #     #         # extract id and count from aws-output
    #     #         buckets = facets[facet_name].get('buckets')
    #     #         active_facets = {b.get('value'): b.get('count') for b in buckets}
    #     #         # generate links recursively
    #     #         output[facet_name] = _generate_facet(facet_name,
    #     #                                              active_facets,
    #     #                                              params)

    #     #     return output

    #     def _generate_facets_v3(facets, params=None):
    #         result = {}
    #         for facet in facets:
    #             out = {}
    #             for b in facets[facet].get("buckets"):
    #                 active = (facet, b.get("value"))
    #                 if params and (active in params):
    #                     rm_params = [x for x in params if x != active]
    #                     b["remove_link"] = _urlencode_v2(rm_params)
    #                 elif params:
    #                     b["add_link"] = _urlencode_v2(params + [active])
    #                 else:
    #                     b["add_link"] = _urlencode_v2([active])
    #                 out[b.get("value")] = b
    #             result[facet] = out
    #         return result

    #     def _urlencode_v2(params):
    #         # params must be a list of tuple(s)
    #         if not params:
    #             return "root"
    #         else:
    #             # utf8_params = [(t[0], unicode(t[1]).encode('utf-8')) for t in params]
    #             utf8_params = [(t[0], t[1]) for t in params]
    #             return urlencode(utf8_params)

    #     def _urlencode(params=None, remove=None, insert=None):
    #         # Like original _urlencode, but added utf8-encoding before
    #         # returning urlencoded params
    #         temp_params = deepcopy(params) if params else []
    #         if remove and not insert:
    #             if remove in temp_params:
    #                 temp_params.remove(remove)
    #         elif remove and insert:
    #             if remove in temp_params:
    #                 loc = temp_params.index(remove)
    #                 temp_params[loc] = insert
    #             else:
    #                 temp_params.append(insert)
    #         elif insert:
    #             temp_params.append(insert)

    #         # utf8_params = [(t[0], unicode(t[1]).encode('utf-8')) for t in temp_params]
    #         utf8_params = [(t[0], t[1]) for t in temp_params]
    #         return urlencode(utf8_params)

    #     # If requesting af list of collections
    #     if query_params.get("resource", "") == "collections":
    #         response = self._get_request("https://openaws.appspot.com/collections")
    #         if response.get("status_code") == 0:
    #             return response.result
    #         else:
    #             return {
    #                 "error": response.get("status_code"),
    #                 "msg": response.get("status_msg"),
    #             }

    #     # If SAM-request (view=ids) or fmt=json, return without adding further keys
    #     # if query_params.get('view', '') == 'ids':
    #     if "ids" in query_params.getlist("view"):
    #         return self.service.list_resources(query_params)

    #     # Else return fullblown response
    #     resp = self.service.list_resources(query_params)

    #     # Convert Immutable MultiDict to mutable list of tuples
    #     # http://werkzeug.pocoo.org/docs/0.13/datastructures/#werkzeug.datastructures.MultiDict
    #     # processed_params = [tup for tup in query_params.iteritems(multi=True)]
    #     processed_params = [tup for tup in query_params.items(multi=True)]

    #     # Keys used for generating searchviews and facets
    #     resp["params"] = processed_params

    #     resp["collection_search"] = query_params.get("collection", False)

    #     resp["filters"] = _generate_filters_v2(resp["server_filters"], processed_params)
    #     resp["active_facets"] = _generate_facets_v3(
    #         resp["server_facets"], processed_params
    #     )

    #     # 'non_query_params' is used to generate a remove_link for the q-param
    #     # which is not processed in _generate_filter()
    #     query = query_params.get("q")
    #     if query:
    #         other_params = [i for i in processed_params if i != ("q", query)]
    #         resp["non_query_params"] = _urlencode_v2(other_params)

    #     # Just testing - remove?
    #     resp["total_facets"] = self.facets

    #     # Client-params dependent on valid response
    #     if resp.get("status_code") == 0:

    #         total = resp["total"]
    #         start = resp["start"]
    #         size = resp["size"]

    #         # Append to service-response
    #         resp["size_list"] = _generate_sizes(processed_params, size)
    #         resp["sort_list"] = _generate_sorts(
    #             processed_params, resp["sort"], resp["direction"]
    #         )
    #         resp["view_list"] = _generate_views(
    #             processed_params, query_params.get("view", "list")
    #         )
    #         resp["view"] = query_params.get("view", "list")

    #         if resp.get("result"):
    #             rm_tup = ("start", str(start))
    #             if start > 0:
    #                 resp["first"] = _urlencode(processed_params, remove=rm_tup)
    #                 resp["previous"] = _urlencode(
    #                     processed_params, remove=rm_tup, insert=("start", start - size)
    #                 )

    #             if total <= 10000 and (start + size < total):
    #                 last_start = total // size * size
    #                 if last_start == total:
    #                     last_start = total - size
    #                 resp["last"] = _urlencode(
    #                     processed_params, remove=rm_tup, insert=("start", last_start)
    #                 )

    #             if (start + size < total) and (start + size <= 10000):
    #                 resp["next"] = _urlencode(
    #                     processed_params, remove=rm_tup, insert=("start", start + size)
    #                 )

    #     else:
    #         resp["message"] = "Something went wrong..."

    #     return resp

    # def get_resource(self, collection, resource, fmt=None):

    #     def _generate_hierarchical_structure(string_list):
    #         # Takes a list of strings with possible '/' as hierarchical seperators
    #         # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

    #         def addHierItem(key, hierStruct, hierList, parent):
    #             if parent != "":
    #                 path = parent + "/" + key
    #             else:
    #                 path = key

    #             hierItem = {"label": key, "path": path}

    #             childrenList = []
    #             children = hierStruct.get(key)
    #             for childKey in sorted(children):
    #                 addHierItem(childKey, children, childrenList, path)

    #             if len(childrenList) > 0:
    #                 hierItem["children"] = childrenList

    #             hierList.append(hierItem)

    #         hierList = []
    #         hierStruct = {}
    #         for item in sorted(string_list):
    #             splitList = item.split("/")

    #             curLevel = hierStruct
    #             for key in splitList:
    #                 hierData = curLevel.get(key, {})
    #                 curLevel[key] = hierData
    #                 curLevel = hierData

    #         for key in sorted(hierStruct):
    #             addHierItem(key, hierStruct, hierList, "")

    #         return hierList

    #     def format_record(record):
    #         result = {}
    #         for key, value in record.items():
    #             # First handle all specialcases
    #             # If 'series' then treat uniquely
    #             if key == 'series':
    #                 output = []
    #                 currentLevel = []
    #                 urlpath = {}
    #                 collection = record.get('collection')

    #                 if collection:
    #                     urlpath['collection'] = collection.get('id')

    #                 for idx in value.split('/'):
    #                     currentLevel.append(idx)
    #                     urlpath['series'] = '/'.join(currentLevel)
    #                     level = {}
    #                     level['label'] = idx
    #                     level['new_link'] = self._generate_new_link(urlpath)
    #                     output.append(level)
    #                 result[key] = output

    #             # If key is list of strings
    #             elif key in ['admin_tags']:
    #                 output = []
    #                 for idx in value:
    #                     item = {}
    #                     item['label'] = idx
    #                     item['new_link'] = self._generate_new_link(key, idx)
    #                     output.append(item)
    #                 result[key] = output

    #             elif key in ['collection_tags']:
    #                 result[key] = _generate_hierarchical_structure(value)

    #             elif key in ['resources']:
    #                 result[key] = value

    #             # If key is dict
    #             elif isinstance(value, dict) and key in self.filters:
    #                 # If id-dict
    #                 if value.get('id'):
    #                     _id = value.get('id')
    #                     label = value.get('label')
    #                     item = {}
    #                     item['label'] = label
    #                     item['id'] = _id
    #                     item['new_link'] = self._generate_new_link(key, _id)
    #                     result[key] = item
    #                 else:
    #                     result[key] = value

    #             # If key is list (of id-dicts)
    #             elif isinstance(value, list) and key in self.filters:
    #                 output = []

    #                 for _dict in value:

    #                     # hierarchical concept or entity
    #                     if isinstance(_dict.get('id'), list):
    #                         hierarchy = []
    #                         for i, v in enumerate(_dict.get('id')):
    #                             item = {}
    #                             item['id'] = v
    #                             item['label'] = _dict.get('label')[i]
    #                             item['new_link'] = '='.join([key, str(v)])
    #                             hierarchy.append(item)
    #                         output.append(hierarchy)

    #                     # flat concept or entity
    #                     else:
    #                         _id = _dict.get('id')
    #                         label = _dict.get('label')
    #                         item = {}
    #                         item['id'] = _id
    #                         item['label'] = label
    #                         item['new_link'] = self._generate_new_link(key, _id)
    #                         output.append(item)

    #                 result[key] = output

    #             else:
    #                 result[key] = value

    #         return result

    #     def format_collection(collection):

    #         # Enhance with dynamically fetched structures from searchengine
    #         series, collection_tags = self.service.list_collection_structures(collection.get('id'))
    #         collection['series'] = series
    #         collection['collection_tags'] = collection_tags

    #         # Pop 'structure'-key - at least for now. Reintroduce when we can work with descriptions on
    #         # individual series-levels
    #         collection.pop('structure', None)

    #         return collection

    #     response = self._get_request('/'.join([self.service_url,
    #                                            self.resources.get(collection),
    #                                            resource]))

    #     if response.get('status_code') == 0:
    #         res = response.get('result')
    #         if collection == 'records':
    #             if fmt == 'json':
    #                 return res
    #             else:
    #                 return format_record(res)
    #         elif collection == 'collections':
    #             return format_collection(res)
    #         else:
    #             return res

    #     elif response.get('status_code') == 1:
    #         return {
    #             'error': {
    #                 'code': 404,
    #                 'msg': 'Resourcen eksisterende ikke',
    #                 'id': resource
    #             }
    #         }
    #     elif response.get('status_code') == 2:
    #         return {
    #             'error': {
    #                 'code': 404,
    #                 'msg': 'Resourcen er slettet',
    #                 'id': resource
    #             }
    #         }
    #     else:
    #         return {
    #             'error': {
    #                 'code': response.get('status_code'),
    #                 'msg': response.get('status_msg'),
    #                 'id': resource
    #             }
    #         }


