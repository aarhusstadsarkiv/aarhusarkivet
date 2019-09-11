import os
import json

# from six.moves.urllib.parse import urlencode
from urllib.parse import urlencode

# Third party
import requests
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import jsonify

# from flask import abort
from flask import redirect
from flask import session
from flask import flash
from flask import url_for
from flask.views import View, MethodView

# Application
import session as ses
import db
import settings
import api_client
from decorators import login_required, employee_required

# import clientInterface
# import autosuggestInterface

IP_WHITELIST = ["193.33.148.24"]


#############
# BASEVIEWS #
#############
class GUIView(View):
    def __init__(self):
        self.context = {}
        ip = request.headers.get("X-Forwarded-For")
        self.context["readingroom"] = ip in IP_WHITELIST
        self.context["host"] = request.host
        self.api = api_client.ApiHandler()
        # self.client = clientInterface.Client()
        # facet_dicts = self.client.list_facets_v2()
        facet_dicts = self.api.list_facets()
        self.context["active_facets"] = facet_dicts.get("active_facets")
        self.context["total_facets"] = facet_dicts.get("total_facets")
        ses.set_current_url(request)

    def error_response(self, errors):
        if request.args.get("fmt", "") == "json":
            return jsonify(errors)
        else:
            return render_template("errorpages/error.html", errors=errors)


class FileView(View):
    def dispatch_request(self, filepath, root=False):
        folder = "./static/root" if root else "./static"
        if (
            filepath.startswith("robots.txt")
            and request.host_url != "https://www.aarhusarkivet.dk/"
        ):
            filepath = "robots_dev.txt"
        return send_from_directory(folder, filepath)


class LoginView(View):
    def dispatch_request(self, page):
        # initialScreen = page if page == 'login' else 'signUp'
        if session.get("profile"):
            return redirect(url_for("show_profile"))
        else:
            params = {
                "redirect_uri": request.host_url + "callback",
                "response_type": "code",
                "scope": "openid profile email",
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
                "audience": os.environ.get("AUTH0_AUDIENCE"),
            }
            url = "https://" + os.environ.get("AUTH0_DOMAIN") + "/authorize?"
            return redirect(url + urlencode(params))


class LogoutView(View):
    def dispatch_request(self):
        session.clear()
        params = {
            "returnTo": url_for("index", _external=True),
            "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        }
        url = "https://" + os.environ.get("AUTH0_DOMAIN") + "/v2/logout?"
        return redirect(url + urlencode(params))


class CallbackView(View):
    def dispatch_request(self):

        if not request.args.get("code"):
            flash('Missing "code". Unable to handle login/signup at the moment.')
            if session.get("current_url"):
                return redirect(session.get("current_url"))
            else:
                return redirect(url_for("index"))

        token_payload = {
            "code": request.args.get("code"),
            "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
            "redirect_uri": request.host_url + "callback",
            "grant_type": os.environ.get("AUTH0_GRANT_TYPE"),
        }

        # get token
        token_url = "https://{domain}/oauth/token".format(
            domain=os.environ.get("AUTH0_DOMAIN")
        )
        headers = {"content-type": "application/json"}

        token_info = requests.post(
            token_url, data=json.dumps(token_payload), headers=headers
        ).json()

        # if not token
        if not token_info.get("access_token"):
            flash(
                'Missing "access_token". Unable to handle login/signup at the moment.'
            )
            if session.get("current_url"):
                return redirect(session.get("current_url"))
            else:
                return redirect(url_for("index"))

        user_url = "https://{domain}/userinfo?access_token={access_token}".format(
            domain=os.environ.get("AUTH0_DOMAIN"),
            access_token=token_info["access_token"],
        )

        # get userinfo
        try:
            userinfo = requests.get(user_url).json()
        except ValueError as e:
            flash("Unable to fetch userdata: " + e)
            if session.get("current_url"):
                return redirect(session.get("current_url"))
            else:
                return redirect(url_for("index"))

        # Insert or sync with db_user
        # return db_user with roles, max_units...
        db_user = db.sync_or_create_user(userinfo)

        if db_user.get("error"):
            flash("Error syncing user with local db: " + db_user.get("msg"))
        else:
            # Populate the session
            session["profile"] = {
                "user_id": db_user.get("user_id"),
                "name": db_user.get("federated_name"),
                "email": db_user.get("email"),
                "roles": db_user.get("roles"),
            }

            session["is_employee"] = (
                True if "employee" in db_user.get("roles") else False
            )
            session["is_admin"] = True if "admin" in db_user.get("roles") else False

            # Add bookmark_ids from db
            session["bookmarks"] = db.list_bookmarks(
                user_id=db_user.get("user_id"), ids_only=True
            )

            # Create session-cart, if not already created before login
            if not session.get("cart"):
                session["cart"] = []

            # Add active orders from db
            # session['orders'] = db.get_orders(user_id=user.get('user_id'), ids_only=True)
            session.modified = True

        if session.get("current_url"):
            return redirect(session.get("current_url"))
        else:
            return redirect(url_for("index"))


#############
# GUI-VIEWS #
#############
class AppView(GUIView):
    def dispatch_request(self, page):
        self.context["subpage"] = page
        self.context["page"] = "homepage" if page == "index" else "app-page"

        if page in settings.GUIDE_PAGES:
            return render_template("guides.html", **self.context)
        elif page in settings.ABOUT_PAGES:
            return render_template("about.html", **self.context)
        else:
            return render_template("%s.html" % page, **self.context)


class SearchView(GUIView):
    def dispatch_request(self):
        # api_resp = self.client.list_resources(request.args)
        resp = self.api.search_records(request.args)
        # return jsonify(resp)

        if resp.get("errors"):
            return self.error_response(resp.get("errors"))

        # update latest search
        ses.set_latest_search(request)

        # SAM only wants id-lists
        if "ids" in request.args.getlist("view"):
            return jsonify(resp)

        # This is also used by Aarhus Teater? Is it?
        # Todo or enhance
        elif request.args.get("fmt", "") == "json":
            result = {}
            result["status_code"] = resp.get("status_code")
            result["result"] = resp.get("result")
            result["filters"] = resp.get("filters")
            result["next"] = resp.get("next")
            result["previous"] = resp.get("previous")
            return jsonify(result)

        # Else standard request
        else:
            self.context["page"] = "searchpage"
            self.context.update(resp)
            return render_template("search.html", **self.context)
            # return jsonify(self.context)


class ResourceView(GUIView):
    def dispatch_request(self, collection, _id):
        # response = self.client.get_resource(collection, resource=str(_id), fmt=fmt)
        # response = self.resourceAPI.get_resource(collection, resource=str(_id))
        resp = self.api.get_resource(collection, str(_id))

        if resp.get("errors"):
            return self.error_response(resp.get("errors"))

        if request.args.get("fmt") == "json":
            # If request does not come from aarhusteaterarkiv-web or employee
            # then remove asset-links
            # TODO: Insecure, fix!
            if request.args.get("curators", "") == "4":
                return jsonify(resp)
            elif ses.get_user() and "employee" in ses.get_user_roles():
                return jsonify(resp)
            else:
                resp.pop("thumbnail", None)
                resp.pop("portrait", None)
                resp.pop("representations", None)
                resp.pop("resources", None)
                return jsonify(resp)

        elif request.is_xhr:
            # If ajax-requested on the results-page it returns an html-blob
            self.context["resource"] = resp
            self.context["page"] = "searchpage"
            return render_template("components/record.html", **self.context)

        else:
            self.context["resource"] = resp
            self.context["collection"] = collection
            self.context["page"] = "resourcepage"
            return render_template("resource.html", **self.context)
            # return jsonify(self.context)


class VocabularyView(GUIView):
    def dispatch_request(self, collection, _id):
        self.context["page"] = "vocabpage"
        self.context["resource"] = _id
        self.context["collection"] = collection

        if collection in ["usability", "availability"] and _id not in [1, 2, 3, 4]:
            return self.error_response({"code": 404, "msg": "No such resource"})

        return render_template("vocabulary.html", **self.context)


class ProfileView(GUIView):
    decorators = [login_required]

    def dispatch_request(self, page):
        if page == "cart":
            self.context["subpage"] = "cart"
            # Fetch full records from remote api
            # cart = self.client.batch_records(ses.get_cart())
            cart = self.api.get_multi_records(ses.get_cart())

            self.context["cart"] = cart

        elif page == "orders":
            self.context["subpage"] = "orders"
            # Fetch orders from db
            orders = db.list_orders(key="user_id", value=ses.get_user_id())
            # Fetch resources
            if orders:
                id_list = [i.get("resource_id") for i in orders]
                # resources = self.client.batch_records(id_list)
                resources = self.api.get_multi_records(id_list)
                # Map orders and full resources
                for i, v in enumerate(orders):
                    v["resource"] = resources[i]
                self.context["orders"] = orders

        elif page == "bookmarks":
            self.context["subpage"] = "bookmarks"
            # Fetch full records from remote api
            # full_bookmarks = self.client.batch_records(ses.get_bookmarks())
            full_bookmarks = self.api.get_multi_records(ses.get_bookmarks())
            self.context["bookmarks"] = full_bookmarks

        elif page == "searches":
            self.context["subpage"] = "searches"
            # Fetch searches from local database
            searches = db.list_searches(ses.get_user_id())
            self.context["searches"] = searches

        elif page == "profile":
            self.context["subpage"] = "profile"

        elif page == "session":
            self.context["subpage"] = "session"

        else:
            return self.error_response({"code": 404, "msg": "No such resource"})

        self.context["page"] = "userpage"
        return render_template("profile.html", **self.context)
        # return jsonify(self.context)


class AdminView(GUIView):
    decorators = [employee_required]

    def dispatch_request(self, page):
        # if page == 'orders':
        #     self.context['subpage'] = 'orders'

        # elif page == 'units':
        #     self.context['subpage'] = 'units'
        # elif page == 'default':
        #     self.context['page'] = 'default'

        # elif page == 'users':
        #     self.context['subpage'] = 'users'
        #     # Fetch users from local database
        #     self.context['users'] = db.get_users()
        render_template("admin.html", **self.context)


class CartView(GUIView):
    def dispatch_request(self):
        cart = ses.get_cart()
        # self.context["cart"] = self.client.batch_records(cart)
        self.context["cart"] = self.api.get_multi_records(cart)
        self.context["page"] = "cart"
        return render_template("cart.html", **self.context)


class TestView(GUIView):
    def dispatch_request(self):
        # cart = ses.get_cart()
        self.context["self"] = str(self)
        self.context["page"] = "test"
        self.context["request"] = request
        # self.context["json_data"] = desktop.get_local_file()
        # return jsonify(self.context)
        return render_template("test.html", **self.context)


#############
# API-VIEWS #
#############
class AutosuggestAPI(MethodView):
    def get(self):
        self.api = api_client.ApiHandler()
        key_args = {}
        key_args["term"] = request.args.get("q")
        key_args["limit"] = request.args.get("limit", 10)
        key_args["domain"] = request.args.get("domain")
        if key_args["term"]:
            return jsonify(self.api.autosuggest(**key_args))
        else:
            return jsonify([])


class OrderAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    decorators = [login_required]

    # def post(self):
    #     payload = request.get_json()
    #     unit_id = payload.get('storage_id')
    #     resource_id = payload.get('resource_id')

    #     if resource_id in ses.get_orders():
    #         resp = {'error': True,
    #                 'msg': "Du har allerede bestilt materialet.'}

    #     elif unit_id and resource_id:
    #         # resp = db.create_order(user, resource_id, unit_id)
    #         resp = db.put_order(ses.get_user_id(), resource_id, unit_id)
    #         if not resp.get('error'):
    #             ses.add_order(resource_id)  # Add to session also

    #     else:
    #         resp = {'error': True,
    #                 'msg': "Manglende information: unit_id eller \
    #                     resource_id.'}

    #     return jsonify(resp)

    # def delete(self, resource_id):
    # response = db.delete_order(ses.get_user_id(), resource_id)
    # key = {'user_id': ses.get_user_id(), 'resource_id': resource_id}
    # response = db.delete_order(key)

    # if not response.get('error'):
    #     ses.remove_order(resource_id)

    # m = response.get('mail')
    # if m:
    #     mail.send_mail(recipient=m.get('email'),
    #                    event='order_available',
    #                    data={'name': m.get('name'),
    #                          'resource': m.get('resource_id')})
    # return jsonify(response)


class BookmarkAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    # AND uses gui-login decorators
    decorators = [login_required]

    def post(self):
        user_id = ses.get_user_id()
        payload = request.get_json()
        resource_id = payload.get("resource_id")

        if resource_id:
            if resource_id in ses.get_bookmarks():
                return jsonify(
                    {"error": True, "msg": "Materialet var allerede bogmærket"}
                )
            else:
                bookmark = {"user_id": user_id, "resource_id": resource_id}
                response = db.put_bookmark(bookmark)
                if not response.get("error"):
                    ses.add_bookmark(resource_id)  # Add to session also
                return jsonify(response)
        else:
            return jsonify({"error": True, "msg": "Manglende materialeID"})

    def delete(self, resource_id):
        user_id = ses.get_user_id()
        bookmark = {"user_id": user_id, "resource_id": resource_id}
        response = db.delete_bookmark(bookmark)
        if not response.get("error"):
            ses.remove_bookmark(resource_id)  # Remove from session also
        return jsonify(response)


class SearchesAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    decorators = [login_required]

    def post(self):
        user_id = ses.get_user_id()
        payload = request.get_json()
        url = payload.get("url")
        description = payload.get("description")
        if url:
            search = {"user_id": user_id, "url": url, "description": description}
            return jsonify(db.add_search(search))
        else:
            return jsonify({"error": True, "msg": "Manglende url-parameter"})

    def put(self, created):
        user_id = ses.get_user_id()
        payload = request.get_json()
        description = payload.get("description")

        if description:
            response = db.update_search(user_id, created, description)
            if response.get("error"):
                return jsonify(response)
            else:
                response["msg"] = "Søgning opdateret"
                return jsonify(response)
        else:
            return jsonify({"error": True, "msg": "Manglende beskrivelse"})

    def delete(self, created):
        search = {"user_id": ses.get_user_id(), "created": created}
        return jsonify(db.delete_search(search))


class CartAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    def post(self):
        payload = request.get_json()
        resource_id = payload.get("resource_id")
        if resource_id:
            return jsonify(ses.add_to_cart(resource_id))
        else:
            return jsonify({"error": "Missing resource_id"})

    def delete(self, resource_id):
        return jsonify(ses.remove_from_cart(resource_id))


# TO IMPLEMENT
class UnitAPI(MethodView):
    def get(self):
        return jsonify({"implemented": False})
