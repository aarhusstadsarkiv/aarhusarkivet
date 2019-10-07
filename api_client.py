# from six.moves.urllib.parse import urlencode
from urllib.parse import urlencode

import searchInterface
import resourceInterface
import autosuggestInterface
import settings


class ApiHandler:
    def __init__(self):
        self.searchAPI = searchInterface.SearchHandler()
        self.resourceAPI = resourceInterface.ResourceHandler()
        self.autosuggestAPI = autosuggestInterface.AutosuggestHandler()
        self.params = settings.QUERY_PARAMS
        self.facets = settings.FACETS

    def autosuggest(self, term, limit=10, domain=None):
        return self.autosuggestAPI.suggest(term, limit, domain)

    def search_records(self, query_params):
        def _validate_query_params(query_params):
            errors = []
            stripped_keys = []

            for key in query_params:
                negated = key[0] == "-"
                stripped_key = key[1:] if negated else key

                if stripped_key not in self.params:
                    errors.append({"param": key, "msg": "Invalid query-param"})
                    continue  # no further tests needed

                if negated and not self.params[stripped_key].get("negatable"):
                    errors.append({"param": key, "msg": "Param not negatable"})

                # Check if non-repeatable stripped_key already exists
                # eg. when using "-usability" and "usability"
                if stripped_key in stripped_keys and not self.params[stripped_key].get(
                    "repeatable"
                ):
                    errors.append({"param": key, "msg": "Param not repeatable"})

                stripped_keys.append(stripped_key)

            # When all stripped_keys are iterated, test for series without collections.
            if "series" in stripped_keys and "collection" not in stripped_keys:
                errors.append(
                    {
                        "param": "series",
                        "msg": "'Series'-key requires a 'collection'-key",
                    }
                )

            return {"errors": errors}

        def _urlencode(params=None, remove=None, insert=None):

            temp_params = params[:] if params else []
            if insert:
                temp_params.append(insert)
            if remove and temp_params and (remove in temp_params):
                temp_params.remove(remove)
            return urlencode(temp_params)

        def _generate_filters(filters, params):
            # Adds links and creator-bools to filters
            out = []

            for f in filters:
                el = {}
                key = f.get("key")
                value = f.get("value")
                negated = f.get("negated")

                # get label if unresolved
                if f.get("unresolved"):
                    r = self.resourceAPI.get_entity_labels([(key, value)])
                    if not r.get("errors"):
                        el["label"] = r["result"][0].get("label")

                # View-link
                # 'label' indicates an id-based filter which can be viewed
                if el.get("label"):
                    if key == "collection":
                        el["view_link"] = "/".join(["collections", value])
                    else:
                        el["view_link"] = "/".join([key, value])

                # Remove_link
                # If positive collection, also remove series
                # negative collection-params works like normal param
                if key == "collection" and not negated:
                    new_params = [
                        (k, v)
                        for k, v in params
                        if k not in ["collection", "series", "start"]
                    ]
                    el["remove_link"] = urlencode(new_params)
                else:
                    new_params = [(k, v) for k, v in params if k not in ["start"]]
                    org_key = "-" + key if negated else key
                    el["remove_link"] = _urlencode(new_params, remove=(org_key, value))

                # Inverse_link
                # If negated, replace with positive, vice versa
                # exception: if positive collection, remove series-param, as
                # it follows the collection
                if negated:
                    new_params = [(k, v) for k, v in params if k not in ["start"]]
                    el["invert_link"] = _urlencode(
                        new_params, remove=("-" + key, value), insert=(key, value)
                    )
                else:
                    if key == "collection":
                        new_params = [
                            (k, v)
                            for k, v in params
                            if k not in ["collection", "series", "start"]
                        ]
                        el["invert_link"] = _urlencode(
                            new_params, insert=("-" + key, value)
                        )
                    else:
                        new_params = [(k, v) for k, v in params if k not in ["start"]]
                        el["invert_link"] = _urlencode(
                            new_params, insert=("-" + key, value), remove=(key, value)
                        )
                # Creator and collector links and bools
                if key in ["people", "organisations"]:
                    api_resp = self.resourceAPI.get_resource(key, value)
                    if not api_resp.get("error"):
                        if api_resp.get("is_creative_creator"):
                            el["creator_link"] = "creators=" + value
                            el["creator"] = True
                        if api_resp.get("is_creator"):
                            el["creator_link"] = "collectors=" + value
                            el["collector"] = True

                el["negated"] = negated
                el["key"] = key
                el["value"] = value
                out.append(el)

            return out

        def _generate_facets(facets, params=None):
            # TODO: Does not work when excisting negative filter is set
            # and you click a positive facet: '-usability=4' is set, you click 'usability=2'
            result = {}
            params = [x for x in params if x[0] != "start"]  # remove 'start'-param from facet-links
            for facet in facets:
                out = {}
                for b in facets[facet].get("buckets"):
                    active = (facet, b.get("value"))
                    if params and (active in params):
                        stripped_params = [x for x in params if x != active]
                        b["remove_link"] = urlencode(stripped_params)
                    elif params:
                        b["add_link"] = urlencode(params + [active])
                    else:
                        b["add_link"] = urlencode([active])
                    out[b.get("value")] = b
                result[facet] = out
            return result

        def _generate_views(params, view):
            output = []
            views = [
                {
                    "label": "Listevisning",
                    "value": "list",
                    "icon": "fas fa-list",  # 'view_list'
                },
                {
                    "label": "Galleri-visning",
                    "value": "gallery",
                    "icon": "fas fa-th",  # 'view_module'
                },
            ]

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != "view"]
            else:
                stripped_params = []

            for option in views:
                current = {}
                current["label"] = option.get("label")
                current["icon"] = option.get("icon")
                if option.get("value") == view:
                    current["selected"] = True
                else:
                    current["link"] = urlencode(
                        stripped_params + [("view", option.get("value"))]
                    )
                output.append(current)
            return output

        def _generate_sorts(params, sort, direction):
            sorts = [
                {
                    "label": "Ældste dato først",
                    "sort": "date_from",
                    "icon": "fas fa-long-arrow-alt-up",  # 'arrow_upward'
                    "direction": "asc",
                },
                {
                    "label": "Nyeste dato først",
                    "sort": "date_to",
                    "icon": "fas fa-long-arrow-alt-down",  # 'arrow_downward'
                    "direction": "desc",
                },
                {"label": "Relevans", "sort": "_score", "direction": "desc"},
            ]
            output = []

            if params:
                stripped_params = [
                    (t[0], t[1])
                    for t in params
                    if t[0] not in ["sort", "direction", "start"]
                ]
            else:
                stripped_params = []

            for option in sorts:
                current = {}
                current["icon"] = option.get("icon")
                current["label"] = option.get("label")
                if option.get("sort") == sort and option.get("direction") == direction:
                    current["selected"] = True
                else:
                    current["link"] = urlencode(
                        stripped_params
                        + [
                            ("sort", option.get("sort")),
                            ("direction", option.get("direction")),
                        ]
                    )
                output.append(current)
            return output

        def _generate_sizes(params, size):
            sizes = [20, 50, 100]
            output = []

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != "size"]
            else:
                stripped_params = []

            for option in sizes:
                current = {}
                current["label"] = option
                if option == size:
                    current["selected"] = True
                else:
                    current["link"] = urlencode(stripped_params + [("size", option)])
                output.append(current)
            return output

        # Validate params
        if query_params:
            validated_request = _validate_query_params(query_params)
            if validated_request.get("errors"):
                return validated_request

        # Make api-call
        api_resp = self.searchAPI.search_records(query_params)

        # If api-error
        if api_resp.get("errors"):
            return api_resp

        # If SAM-request, no need for further processing
        # api_resp on request with "view=ids"-param includes three keys: status_code, result, next_cursor (optional)
        if "ids" in query_params.getlist("view"):
            return api_resp

        # Else process and convert response
        # api_resp on normal request includes: sort, direction, size, date_from,
        # date_to, _query_string, total, start, server_facets, filters, query, result,
        # view_list, sort_list, size_list, view, non_query_params
        resp = {}

        # convert multidict to list of tuples
        params = [tup for tup in query_params.items(multi=True)]

        # Keys used for generating searchviews and facets
        resp["params"] = params
        resp["query"] = api_resp.get("query", None)
        
        # Hint for GUI
        resp["collection_search"] = query_params.get("collection", False)

        # If filters, generate links and possibly labels
        if api_resp.get("filters"):
            resp["filters"] = _generate_filters(api_resp["filters"], params)

        # if facets, generate links
        if api_resp.get("facets"):
            resp["active_facets"] = _generate_facets(api_resp["facets"], params)

        # 'non_query_params' is used to generate a remove_link for the q-param
        # on the zero-hits page
        if not api_resp.get("result") and api_resp.get("query"):
            other_params = [i for i in params if i != ("q", api_resp.get("query"))]
            resp["non_query_params"] = urlencode(other_params)

        # Commented out. Probably not in use
        # resp["total_facets"] = self.facets

        # Pagination
        if api_resp.get("result"):
            total = api_resp["total"]
            start = api_resp["start"]
            size = api_resp["size"]
            rm_tup = ("start", str(start))
            if start > 0:
                resp["first"] = _urlencode(params, remove=rm_tup)
                resp["previous"] = _urlencode(
                    params, remove=rm_tup, insert=("start", start - size)
                )

            if total <= 10000 and (start + size < total):
                last_start = total // size * size
                if last_start == total:
                    last_start = total - size
                resp["last"] = _urlencode(
                    params, remove=rm_tup, insert=("start", last_start)
                )

            if (start + size < total) and (start + size <= 10000):
                resp["next"] = _urlencode(
                    params, remove=rm_tup, insert=("start", start + size)
                )

        # Proces size, sort, direction and view
        resp["size_list"] = _generate_sizes(params, api_resp["size"])
        resp["sort_list"] = _generate_sorts(
            params, api_resp["sort"], api_resp["direction"]
        )
        resp["view_list"] = _generate_views(params, query_params.get("view", "list"))
        resp["view"] = query_params.get("view", "list")
        resp["total"] = api_resp.get("total")
        resp["start"] = api_resp.get("start")
        resp["size"] = api_resp.get("size")
        resp["sort"] = api_resp.get("sort")
        resp["result"] = api_resp.get("result")
        # Commented out. Probably not in use
        # resp["_query_string"] = api_resp.get("_query_string")

        return resp

    def list_facets(self):
        facets = self.searchAPI.list_facets()
        result = {}
        for facet in facets:
            out = {}
            for b in facets[facet].get("buckets"):
                b["add_link"] = urlencode([(facet, b.get("value"))])
                out[b.get("value")] = b
            result[facet] = out
        return {"total_facets": self.facets, "active_facets": result}

    def get_multi_records(self, id_list=None):
        return self.resourceAPI.multi_get_records(id_list)

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
        api_resp = self.resourceAPI.get_resource(collection, resource)

        # If api-error
        if api_resp.get("errors"):
            return api_resp

        # Format and return response
        if collection == "records":
            return format_record(api_resp)
        elif collection == "collections":
            return format_collection(api_resp)
        else:
            return api_resp
