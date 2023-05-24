from openaws import (
    # auth
    AuthJwtLoginPost,
    auth_jwt_login_post,
    BearerResponse,
    # verify
    auth_verify_post,
    VerifyPost,
    # request verify
    auth_request_verify_post,
    RequestVerifyPost,
    # reset password
    auth_reset_password_post,
    ResetPasswordPost,
    # me
    UserRead,
    UserPermissions,
    users_me_get,
    # errors
    HTTPValidationError,
    ErrorModel,
    # Register. Forgot password
    ForgotPasswordPost,
    UserCreate,
    UserFlag,
    auth_register_post,
    auth_forgot_password_post,
    # schema
    SchemaCreate,
    SchemaRead,
    SchemaCreateData,
    schemas_name_get,
    schemas_post,
    schemas_get,
    # entity
    EntityRead,
    EntityCreate,
    EntityUpdate,
    entities_uuid_patch,
    entities_get,
    entities_post,
    entities_uuid_get,
    # records
    RecordsIdGet,
    RecordsSearchGet,
    record_id_get,
    records_search_get,
    # client related
    AuthenticatedClient,
    Client,
)

from api_openaws_error import OpenAwsException, validate_response
from flask import request, session
from app_log import log
import settings


class OpenAwsSession:
    @staticmethod
    def in_jwt_session():
        if "access_token" in session and "token_type" in session:
            return True
        else:
            return False

    @staticmethod
    def set_jwt_session(access_token: str, token_type: str):
        session["access_token"] = access_token
        session["token_type"] = token_type

    @staticmethod
    def in_cookie_session():
        if "_auth" in session:
            return True
        else:
            return False

    @staticmethod
    def clear_jwt_session():
        session.pop("access_token")
        session.pop("token_type")

    @staticmethod
    def clear_cookie_session():
        session.pop("_auth")


base_url = settings.WEBSERVICE_URL
timeout = 10
verify_ssl = True


def get_client() -> Client:
    client = Client(
        raise_on_unexpected_status=False,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )
    return client


def get_auth_client(request: request) -> AuthenticatedClient:
    if not OpenAwsSession.in_jwt_session():
        raise OpenAwsException(401, "Du skal være logget ind for at se denne side.")

    token = session["access_token"]
    auth_client = AuthenticatedClient(
        raise_on_unexpected_status=False,
        token=token,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )

    return auth_client


def jwt_login_post(request: request):
    username = request.form.get("username")
    password = request.form.get("password")

    client: Client = get_client()
    login_dict = {"username": username, "password": password}
    form_data: AuthJwtLoginPost = AuthJwtLoginPost.from_dict(login_dict)

    bearer_response = auth_jwt_login_post.sync(
        client=client, form_data=form_data)

    validate_response(bearer_response)

    if not isinstance(bearer_response, BearerResponse):
        raise OpenAwsException(
            500, "System fejl. Prøv igen senere.", "Unauthorized")

    access_token: str = bearer_response.access_token
    token_type: str = bearer_response.token_type
    OpenAwsSession.set_jwt_session(access_token, token_type)


def register_post(request: request):

    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    client: Client = get_client()

    src_dict = {"email": email, "password": password}
    json_body = UserCreate.from_dict(src_dict=src_dict)
    user_read = auth_register_post.sync(client=client, json_body=json_body)

    validate_response(user_read)
    if not isinstance(user_read, UserRead):
        raise OpenAwsException(
            500, "System fejl. Prøv igen senere.", "Unauthorized")


def verify_post(request: request):
    token = request.view_args["token"]

    client: Client = get_client()

    src_dict = {"token": token}
    json_body = VerifyPost.from_dict(src_dict=src_dict)
    user_read = auth_verify_post.sync(client=client, json_body=json_body)

    validate_response(user_read)
    if not isinstance(user_read, UserRead):
        raise OpenAwsException(
            500, "System fejl. Prøv igen senere.", "Unauthorized")


def forgot_password_post(request: request) -> None:
    email = request.form.get("email")
    client: Client = get_client()

    src_dict = {"email": email}
    forgot_password_post: ForgotPasswordPost = ForgotPasswordPost.from_dict(
        src_dict=src_dict
    )

    forgot_password_response = auth_forgot_password_post.sync(
        client=client, json_body=forgot_password_post
    )

    if isinstance(forgot_password_response, HTTPValidationError):
        raise OpenAwsException(
            422,
            "Denne email eksisterer ikke i vores system.",
        )


def reset_password_post(request: request) -> None:

    token = request.view_args["token"]

    client: Client = get_client()
    src_dict = {"token": token, "password": request.form.get("password")}

    reset_password_post: ResetPasswordPost = ResetPasswordPost.from_dict(
        src_dict=src_dict
    )
    reset_password_response = auth_reset_password_post.sync(
        client=client, json_body=reset_password_post
    )

    validate_response(reset_password_response)


def me_get(request: request) -> dict:
    client: AuthenticatedClient = get_auth_client(request)

    if hasattr(request, "me"):
        return request.me

    me = users_me_get.sync(client=client)

    if isinstance(me, UserRead):
        me_dict = me.to_dict()
        setattr(request, "me", me_dict)
        return me_dict

    # Clear jwt session
    OpenAwsSession.clear_jwt_session()

    raise OpenAwsException(
        401,
        "For at se denne side skal du være logget ind.",
    )


def is_logged_in(request: request) -> bool:
    try:
        me_get(request)
        return True
    except Exception:
        return False


async def permissions_as_list(permissions: dict) -> list[str]:
    """{'guest': True, 'basic': True, 'employee': True, 'admin': True}"""
    permissions_list = []
    for permission, value in permissions.items():
        if value:
            permissions_list.append(permission)
    return permissions_list


def request_verify_post(request: request):
    """request for a token sent to the user's email.
    User needs to be logged in."""
    client: Client = get_auth_client(request)

    me = me_get(request)
    email = me["email"]

    json_body = RequestVerifyPost.from_dict({"email": email})
    response = auth_request_verify_post.sync(
        client=client, json_body=json_body)

    if response:
        raise OpenAwsException(
            422,
            """Systemet kunne ikke afsende en verificerings e-mail.
            Prøv igen senere.""",
        )


def _validate_passwords(request):
    password_1 = request.form.get("password")
    password_2 = request.form.get("password_2")

    if password_1 != password_2:
        raise OpenAwsException(
            400,
            "Password er ikke ens i de to felter.",
        )

    if len(password_1) < 8:
        raise OpenAwsException(
            400,
            "Password skal mindst være 8 tegn langt.",
        )
