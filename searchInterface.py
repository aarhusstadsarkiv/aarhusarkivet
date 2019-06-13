import os
import json

import requests
import boto3

import settings
import resourceInterface


class SearchHandler():
    def __init__(self):
        # self.OAWS_API_KEY = os.environ.get('OAWS_API_KEY')
        # self.OAWS_BASE_URL = "https://openaws.appspot.com"
        # self.resourceAPI = resourceInterface.ResourceHandler()
        self.FILTERS = settings.SEARCH_FILTERS
        self.search_engine = boto3.client(
            "cloudsearchdomain",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION_NAME"),
            endpoint_url=os.environ.get("AWS_CLOUDSEARCH_ENDPOINT"),
        )

    def list_collection_facets(collection_id):
        facet_options = {
            "collection_tags": {"sort": "count", "size": 7000},
            "series": {"sort": "count", "size": 2000}
        }

        key_args = {}
        key_args["query"] = "matchall"
        key_args["facet"] = json.dumps(facet_options)
        key_args["returnFields"] = "_no_fields"
        key_args["size"] = 1
        key_args["queryParser"] = "structured"
        key_args["query"] = "matchall"
        key_args["filterQuery"] = "collection:'" + str(collection_id) + "'"

        api_response = self.search_engine.search(**key_args)
        return api_response.get("facets")

    def search_records(self, query_params):
        # 'query_params' is a Immutable MultiDict
        # http://werkzeug.pocoo.org/docs/0.13/datastructures/#werkzeug.datastructures.MultiDict

        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/search-api.html#structured-search-syntax
        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/searching-compound-queries.html

        ############
        # BASELINE #
        ############
        # Kwargs to send to all bobo3-cloudsearch-calls.
        key_args = {}
        key_args["queryParser"] = "structured"
        key_args["queryOptions"] = json.dumps(
            {"fields": ["label^4", "summary^2", "description"]}
        )

        date_from = query_params.get("date_from")
        date_to = query_params.get("date_to")
        q = query_params.get("q")
        sort = query_params.get("sort", "date_from")
        direction = query_params.get("direction", "asc")

        ####################
        # SORT + DIRECTION #
        ####################
        # Extra sorting-tests, if no explicit sort is selected.
        if not query_params.get("sort"):
            # If fulltext-search, then rank by relevance
            if q:
                sort = "_score"
                direction = "desc"
            # If date_to is set, override relevance-sorting
            if date_to:
                sort = "date_to"
                direction = "desc"
            # If date_from is set, overrides relevance and date_to
            if date_from:
                sort = "date_from"
                direction = "asc"

        key_args["sort"] = " ".join([sort, direction])  # aws-convention

        ###########
        # Q-PARAM #
        ###########
        # Fulltext query - wrap value in single-quotes or if empty use
        # "matchall" to enable filtered searches without a q-param
        if q and q.strip():
            # tokens = q.strip().split(' ')
            tokens = q.split(" ")
            if tokens:
                strs = []
                phrase = None
                phrase_strs = []

                for s in tokens:
                    # no need to bother
                    if len(s) < 2:
                        continue

                    # If single-word phrase
                    if not phrase and s.startswith('"') and s.endswith('"'):
                        strs.append("'" + s[1:-1] + "'")

                    # Elif single-word negative phrase
                    elif not phrase and s.startswith('-"') and s.endswith('"'):
                        strs.append("'" + s[2:-1] + "'")

                    # Elif a phrase is active, add token if not the ending
                    elif phrase and not (s.endswith('"') or s.startswith('"')):
                        phrase_strs.append(s)

                    elif s.startswith('-"') and not phrase:
                        # start a new phrase and append string
                        phrase = "negated"
                        # s = re.sub('*', '', s)
                        phrase_strs.append(s[2:])

                    elif s.startswith('"') and not phrase:
                        # start a new phrase and append string
                        phrase = "positive"
                        phrase_strs.append(s[1:])

                    elif s.endswith('"') and phrase:
                        # append string and close phrase
                        phrase_strs.append(s[:-1])
                        if phrase == "positive":
                            strs.append("(phrase '" + " ".join(phrase_strs) + "')")
                        else:
                            strs.append(
                                "(not (phrase '" + " ".join(phrase_strs) + "'))"
                            )
                        # Ready for new phrase
                        phrase = None
                        phrase_strs = []

                    elif s.startswith("-"):
                        if s.endswith("*"):
                            strs.append("(not (prefix '" + s[:-1] + "'))")
                        else:
                            strs.append("(not '" + s[1:] + "')")

                    elif s.endswith("*"):
                        strs.append("(prefix '" + s[:-1] + "')")

                    else:
                        strs.append("'" + s + "'")

            if len(tokens) > 1:
                key_args["query"] = "(and " + " ".join(strs) + ")"
            else:
                # key_args['query'] = "'" + strs[0] + "'"
                key_args["query"] = strs[0]

        else:
            key_args["query"] = "matchall"

        ############
        # FQ-PARAM #
        ############
        filters_to_query = []
        # If using id_based filters (collections or entities)
        # call resourceInterface.get_labels to fetch labels for each id
        filters_to_resolve = []
        filters_to_output = []
        negated_filters = []

        # Build filterQuery. TODO: hairy stuff that needs documentation
        for key in query_params.keys():

            # If key is negated, but not allowed to, skip it
            if (
                key.startswith("-")
                and key[1:] in self.FILTERS
                and not self.FILTERS[key[1:]].get("negatable")
            ):
                continue
            # remove any negation before using self.FILTERS
            stripped_key = key[1:] if key.startswith("-") else key

            if stripped_key in self.FILTERS:
                filter_type = self.FILTERS[stripped_key].get("type")

                # Go back to using the full key-label before iterating query
                for value in query_params.getlist(key):

                    if filter_type == "object":
                        filter_str = ":".join([stripped_key, "'" + value + "'"])
                        # if negation, update filter_str and add to negated[]
                        if stripped_key != key:
                            negated_filters.append((stripped_key, value))
                            filter_str = "(not " + filter_str + ")"
                        filters_to_query.append(filter_str)
                        filters_to_resolve.append({"resource": stripped_key, "id": int(value)})

                    elif filter_type in ["string", "integer"]:
                        filter_str = ":".join([stripped_key, "'" + value + "'"])
                        # if negation, update filter_str
                        if stripped_key != key:
                            negated_filters.append((stripped_key, value))
                            filter_str = "(not " + filter_str + ")"
                        filters_to_query.append(filter_str)
                        filters_to_output.append({"key": key, "value": value})

                    elif key == "date_from":
                        filters_to_query.append("date_from:[" + value + ",}")
                        filters_to_output.append({"key": key, "value": value})

                    elif key == "date_to":
                        filters_to_query.append("date_to:{," + value + "]")
                        filters_to_output.append({"key": key, "value": value})

        if filters_to_query:
            key_args["filterQuery"] = "(and " + " ".join(filters_to_query) + ")"

        # If SAM-request or Sejrs Sedler
        if "ids" in query_params.getlist("view"):
            key_args["returnFields"] = "_no_fields"
            key_args["size"] = query_params.get("size", 1000, int)
            if query_params.get("cursor"):
                key_args["cursor"] = query_params.get("cursor")
            else:
                key_args["cursor"] = "initial"

        # Else standard-request
        else:
            key_args["facet"] = json.dumps(
                {
                    "availability": {},
                    "usability": {},
                    "content_types": {"size": 100},
                    "subjects": {"size": 100},
                    "collection": {"size": 40},
                }
            )
            key_args[
                "returnFields"
            ] = "label,summary,collection,series,content_types,thumbnail,portrait,collectors_label,date_from,date_to,created_at,availability,updated_at"
            key_args["start"] = query_params.get("start", 0, int)
            key_args["size"] = query_params.get("size", 20, int)
        
        # Make request to Cloudsearch
        response = self.search_engine.search(**key_args)

        if filters_to_resolve:
            response["filters_to_resolve"] = filters_to_resolve

        return response

