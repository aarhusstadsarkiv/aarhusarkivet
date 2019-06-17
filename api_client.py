from six.moves.urllib.parse import urlencode

import searchInterface
import resourceInterface
import autosuggestInterface
import settings


class ApiHandler:
    def __init__(self):
        self.searchAPI = searchInterface.SearchHandler()
        self.resourceAPI = resourceInterface.ResourceHandler()
        self.autosuggestAPI = autosuggestInterface.AutosuggestHandler()
        self.params = settings.SEARCH_FILTERS

    def autosuggest(self, term, limit=10, domain=""):
        return self.autosuggestAPI.get(term, limit, domain)

    def search_records(self, query_params):
        # Validate query-params
        errors = []
        for key in query_params:
            stripped_key = key[1:] if key[0] == "-" else key
            if stripped_key not in self.params:
                errors.append({"param": key, "msg": "Invalid param"})

            if key[0] == "-" and not self.params[stripped_key].get("negatable"):
                errors.append({"param": key, "msg": "Param not negatable"})

            # 'query_params' is a Immutable MultiDict
            if len(query_params.getlist(key)) > 1 and not self.params[stripped_key].get(
                "repeatable"
            ):
                errors.append({"param": key, "msg": "Param not repeatable"})
        if errors:
            return {"errors": errors}

        # Make api-call
        api_response = self.searchAPI.search_records(query_params)

        # If any id-filters need related labels
        if api_response.get("filters_to_resolve"):
            resp = self.resourceAPI.get_labels(filters_to_resolve)

            if resp.get("status_code") == 0:
                for _dict in resp.get("result"):
                    negated = True if (key, k) in negated_filters else False
                    filters_to_output.append(
                        {
                            "key": _dict.get("resource"),
                            "value": _dict.get("id"),
                            "label": _dict.get("label"),
                            "negated": negated,
                        }
                    )

        out["server_filters"] = filters_to_output
        # out['negated_filters'] = negated_filters

        return out

    def get_resource(self, collection, resource):
        # Formater record-dict
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
                if key == "series":
                    output = []
                    currentLevel = []
                    urlpath = {}
                    collection = record.get("collection")

                    if collection:
                        urlpath["collection"] = collection.get("id")

                    for idx in value.split("/"):
                        currentLevel.append(idx)
                        urlpath["series"] = "/".join(currentLevel)
                        level = {}
                        level["label"] = idx
                        level["new_link"] = urlencode(urlpath)
                        output.append(level)
                    result[key] = output

                # If key is list of strings
                elif key in ["admin_tags"]:
                    output = []
                    for idx in value:
                        item = {}
                        item["label"] = idx
                        item["new_link"] = urlencode({key: _id})
                        output.append(item)
                    result[key] = output

                elif key in ["collection_tags"]:
                    result[key] = _generate_hierarchical_structure(value)

                elif key in ["resources"]:
                    result[key] = value

                # If key is dict
                elif isinstance(value, dict) and key in self.params:
                    # If id-dict
                    if value.get("id"):
                        _id = value.get("id")
                        label = value.get("label")
                        item = {}
                        item["label"] = label
                        item["id"] = _id
                        item["new_link"] = urlencode({key: _id})
                        result[key] = item
                    else:
                        result[key] = value

                # If key is list (of id-dicts)
                elif isinstance(value, list) and key in self.params:
                    output = []

                    for _dict in value:

                        # hierarchical concept or entity
                        if isinstance(_dict.get("id"), list):
                            hierarchy = []
                            for i, v in enumerate(_dict.get("id")):
                                item = {}
                                item["id"] = v
                                item["label"] = _dict.get("label")[i]
                                item["new_link"] = "=".join([key, str(v)])
                                hierarchy.append(item)
                            output.append(hierarchy)

                        # flat concept or entity
                        else:
                            _id = _dict.get("id")
                            label = _dict.get("label")
                            item = {}
                            item["id"] = _id
                            item["label"] = label
                            item["new_link"] = urlencode({key: _id})
                            output.append(item)

                    result[key] = output

                else:
                    result[key] = value

            return result

        # Formater samlings-dict
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

                collection_facets = self.searchAPI.list_collection_facets(collection_id)

                # Convert to dicts with label, id and children keys, like the classic 'series'
                series = []
                if collection_facets.get("series"):
                    series_list = collection_facets["series"].get("buckets")
                    series = _generate_hierarchical_structure(series_list)

                collection_tags = []
                if collection_facets.get("collection_tags"):
                    collection_tags_list = collection_facets["collection_tags"].get(
                        "buckets"
                    )
                    collection_tags = _generate_hierarchical_structure(
                        collection_tags_list
                    )

                return series, collection_tags

            # Enhance with dynamically fetched structures from searchengine
            series, collection_tags = _list_collection_structures(collection.get("id"))
            collection["series"] = series
            collection["collection_tags"] = collection_tags

            # Pop 'structure'-key - at least for now. Reintroduce when we can work with descriptions on
            # individual series-levels
            collection.pop("structure", None)

            return collection

        # Make api-call
        api_response = self.resourceAPI.get_resource(collection, resource)

        # If api-error
        if api_response.get("errors"):
            return api_response

        # Format response
        if collection == "records":
            return format_record(api_response)
        elif collection == "collections":
            return format_collection(api_response)
        else:
            return api_response

