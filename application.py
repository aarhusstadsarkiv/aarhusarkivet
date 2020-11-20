import os

from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import redirect

import settings
import views

try:
    load_dotenv()
except IOError:
    pass


##################
# INITIALIZE APP #
##################
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.debug = os.environ.get("DEBUG", False)
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", False)

# app.jinja_env.auto_reload = True
app.url_map.strict_slashes = False
app.jinja_env.globals["ICONS"] = settings.ICONS


@app.before_request
def before_request():
    # Copied from https://github.com/kennethreitz/flask-sslify
    criteria = [
        request.is_secure,
        app.debug,
        app.testing,
        request.headers.get("X-Forwarded-Proto", "http") == "https",
    ]

    if not any(criteria):
        if request.url.startswith("http://"):
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)


@app.after_request
def after_request(response):
    criteria = [app.debug, app.testing]

    if not any(criteria):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=63072000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Access-Control-Allow-Origin"] = "*"

    return response


##########
# ROUTES #
##########
app.add_url_rule(
    "/", defaults={"page": "index"}, view_func=views.AppView.as_view("index")
)

# Auth-pages
app.add_url_rule(
    "/<any('login', 'signup'):page>", view_func=views.LoginView.as_view("login")
)

app.add_url_rule("/logout", view_func=views.LogoutView.as_view("logout"))

app.add_url_rule("/callback", view_func=views.CallbackView.as_view("callback"))

# Static ROOT files
app.add_url_rule(
    "/<any(" + ", ".join(settings.STATIC_PAGES) + "):filepath>",
    defaults={"root": True},
    view_func=views.FileView.as_view("serve_static_rootfile"),
)

# Static application files (css, images...)
app.add_url_rule(
    "/static/<path:filepath>", view_func=views.FileView.as_view("serve_static_file")
)

# Imagesites-page
app.add_url_rule(
    "/images",
    defaults={"page": "imagesites"},
    view_func=views.AppView.as_view("show_imagesites"),
)

# Guide-pages (subpaged)
app.add_url_rule(
    "/guides/<any(" + ", ".join(settings.GUIDE_PAGES) + "):page>",
    view_func=views.AppView.as_view("show_guide"),
)

# About-pages (subpaged)
app.add_url_rule(
    "/about/<any(" + ", ".join(settings.ABOUT_PAGES) + "):page>",
    view_func=views.AppView.as_view("show_about"),
)

# Vocabulary-pages (subpaged)
app.add_url_rule(
    "/<any(" + ", ".join(settings.VOCAB_PAGES) + "):collection>/<int:_id>",
    view_func=views.VocabularyView.as_view("show_vocabulary"),
)

# Resource-pages
app.add_url_rule(
    "/<any(" + ", ".join(settings.RESOURCE_PAGES) + "):collection>/<int:_id>",
    view_func=views.ResourceView.as_view("show_resource"),
)

# Search-page
app.add_url_rule("/search", view_func=views.SearchView.as_view("search"))

# Profile (subpaged)
app.add_url_rule(
    "/users/me",
    defaults={"page": "profile"},
    view_func=views.ProfileView.as_view("show_profile"),
)
app.add_url_rule(
    "/users/me/<path:page>", view_func=views.ProfileView.as_view("show_profile_subpage")
)

# CartView
app.add_url_rule(
    "/cart", view_func=views.CartView.as_view("show_cart"), methods=["GET"]
)

# Testpage
app.add_url_rule("/testpage", view_func=views.TestView.as_view("test"), methods=["GET"])

##############
# API-ROUTES #
##############

# AutosuggestAPI
app.add_url_rule("/autosuggest", view_func=views.AutosuggestAPI.as_view("autosuggest"))

# CartAPI
app.add_url_rule(
    "/cart", view_func=views.CartAPI.as_view("add_to_cart"), methods=["POST"]
)

app.add_url_rule(
    "/cart/<resource_id>",
    view_func=views.CartAPI.as_view("remove_from_cart"),
    methods=["DELETE"],
)

# OrderAPI
app.add_url_rule(
    "/users/me/orders",
    view_func=views.OrderAPI.as_view("create_order"),
    methods=["POST"],
)
app.add_url_rule(
    "/users/me/orders/<resource_id>",
    view_func=views.OrderAPI.as_view("delete_order"),
    methods=["DELETE"],
)

# BookmarkAPI
app.add_url_rule(
    "/users/me/bookmarks",
    view_func=views.BookmarkAPI.as_view("create_bookmark"),
    methods=["POST"],
)
app.add_url_rule(
    "/users/me/bookmarks/<resource_id>",
    view_func=views.BookmarkAPI.as_view("delete_bookmark"),
    methods=["DELETE"],
)

# SavedSearchesAPI
app.add_url_rule(
    "/users/me/searches",
    view_func=views.SearchesAPI.as_view("create_search"),
    methods=["POST"],
)
app.add_url_rule(
    "/users/me/searches/<created>",
    view_func=views.SearchesAPI.as_view("delete_search"),
    methods=["DELETE"],
)
app.add_url_rule(
    "/users/me/searches/<created>",
    view_func=views.SearchesAPI.as_view("update_search"),
    methods=["PUT"],
)

###########
# RUN APP #
###########
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 3000))
