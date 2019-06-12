
##############
# AUTH-VIEWS #
##############
# @app.route('/<any("login", "signup"):page>')
# def login(page):
#     # initialScreen = page if page == 'login' else 'signUp'
#     if session.get("profile"):
#         return redirect(url_for("show_profile"))
#     else:
#         params = {
#             "redirect_uri": request.host_url + "callback",
#             "response_type": "code",
#             "scope": "openid profile email",
#             "client_id": os.environ.get("AUTH0_CLIENT_ID"),
#             "audience": os.environ.get("AUTH0_AUDIENCE"),
#         }
#         url = "https://" + os.environ.get("AUTH0_DOMAIN") + "/authorize?"
#         return redirect(url + urlencode(params))


# @app.route("/logout")
# def logout():
#     session.clear()
#     params = {
#         "returnTo": url_for("index", _external=True),
#         "client_id": os.environ.get("AUTH0_CLIENT_ID"),
#     }
#     url = "https://" + os.environ.get("AUTH0_DOMAIN") + "/v2/logout?"
#     return redirect(url + urlencode(params))


# @app.route("/callback")
# def callback_handler():
#     if not request.args.get("code"):
#         flash('Missing "code". Unable to handle login/signup at the moment.')
#         if session.get("current_url"):
#             return redirect(session.get("current_url"))
#         else:
#             return redirect(url_for("index"))

#     token_payload = {
#         "code": request.args.get("code"),
#         "client_id": os.environ.get("AUTH0_CLIENT_ID"),
#         "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
#         "redirect_uri": request.host_url + "callback",
#         "grant_type": os.environ.get("AUTH0_GRANT_TYPE"),
#     }

#     # get token
#     token_url = "https://{domain}/oauth/token".format(
#         domain=os.environ.get("AUTH0_DOMAIN")
#     )
#     headers = {"content-type": "application/json"}

#     token_info = requests.post(
#         token_url, data=json.dumps(token_payload), headers=headers
#     ).json()

#     # if not token
#     if not token_info.get("access_token"):
#         flash('Missing "access_token". Unable to handle login/signup at the moment.')
#         if session.get("current_url"):
#             return redirect(session.get("current_url"))
#         else:
#             return redirect(url_for("index"))

#     user_url = "https://{domain}/userinfo?access_token={access_token}".format(
#         domain=os.environ.get("AUTH0_DOMAIN"), access_token=token_info["access_token"]
#     )

#     # get userinfo
#     try:
#         userinfo = requests.get(user_url).json()
#     except ValueError as e:
#         flash("Unable to fetch userdata: " + e)
#         if session.get("current_url"):
#             return redirect(session.get("current_url"))
#         else:
#             return redirect(url_for("index"))

#     # Insert or sync with db_user
#     # return db_user with roles, max_units...
#     db_user = db.sync_or_create_user(userinfo)

#     if db_user.get("error"):
#         flash(u"Error syncing user with local db: " + db_user.get("msg"))
#     else:
#         # Populate the session
#         session["profile"] = {
#             "user_id": db_user.get("user_id"),
#             "name": db_user.get("federated_name"),
#             "email": db_user.get("email"),
#             "roles": db_user.get("roles"),
#         }

#         session["is_employee"] = True if "employee" in db_user.get("roles") else False
#         session["is_admin"] = True if "admin" in db_user.get("roles") else False

#         # Add bookmark_ids from db
#         session["bookmarks"] = db.list_bookmarks(
#             user_id=db_user.get("user_id"), ids_only=True
#         )

#         # Create session-cart, if not already created before login
#         if not session.get("cart"):
#             session["cart"] = []

#         # Add active orders from db
#         # session['orders'] = db.get_orders(user_id=user.get('user_id'), ids_only=True)
#         session.modified = True

#     if session.get("current_url"):
#         return redirect(session.get("current_url"))
#     else:
#         return redirect(url_for("index"))