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
from openaws_client.models import UserPermissions
from flask import request, session
from app_log import log


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


class OpenAwsException(Exception):
    def __init__(self, status_code: int, message: str, text: str = ""):
        self.status_code = status_code
        self.message = message
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


base_url = "https://dev.openaws.dk"
base_url = "http://localhost:8000"
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


def login_jwt(request: request):
    username = request.form.get("username")
    password = request.form.get("password")

    client: Client = get_client()
    form_data: AuthJwtLoginPost = AuthJwtLoginPost(username=username, password=password)

    bearer_response = auth_jwt_login_post.sync(client=client, form_data=form_data)

    if isinstance(bearer_response, BearerResponse):
        access_token: str = bearer_response.access_token
        token_type: str = bearer_response.token_type
        OpenAwsSession.set_jwt_session(access_token, token_type)

    if isinstance(bearer_response, HTTPValidationError):
        raise OpenAwsException(
            422,
            "Bruger eksisterer allerede. Prøv at logge ind i stedet.",
        )

    if isinstance(bearer_response, ErrorModel):
        raise OpenAwsException(
            400,
            "Bruger eksisterer ikke",
        )


def user_create(request: request):
    email = str(request.form.get("email"))
    password = str(request.form.get("password"))

    client: Client = get_client()

    src_dict = {"email": email, "password": password}
    json_body = UserCreate.from_dict(src_dict=src_dict)

    user_read = auth_register_post.sync(client=client, json_body=json_body)
    log.debug(user_read)
    if isinstance(user_read, HTTPValidationError):
        raise OpenAwsException(
            422,
            "Email skal være korrekt. Password skal mindst have 8 tegn.",
            "Unauthorized",
        )

    if isinstance(user_read, ErrorModel):
        raise OpenAwsException(
            400,
            "Bruger med denne email eksisterer allerede. Prøv at logge ind.",
            "Unauthorized",
        )

    if not isinstance(user_read, UserRead):
        raise OpenAwsException(500, "System fejl. Prøv igen senere.", "Unauthorized")


def user_verify(request: request):
    
    token = request.view_args['token'] 
    log.debug(token)
    
    client: Client = get_client()

    src_dict = {"token": token}
    json_body = VerifyPost.from_dict(src_dict=src_dict)
    user_read = auth_verify_post.sync(client=client, json_body=json_body)

    if isinstance(user_read, HTTPValidationError):
        raise OpenAwsException(
            422,
            "API System fejl. Prøv igen senere.",
            "Unauthorized",
        )

    if isinstance(user_read, ErrorModel):

        detail = user_read.detail
        if (detail == 'VERIFY_USER_BAD_TOKEN'):
            message = "Nøglen i URLen eksisterer ikke i systemet. Du må logge ind igen for at få tilsendt en ny nøgle."
        if (detail == 'VERIFY_USER_ALREADY_VERIFIED'):
            message = "Bruger er allerede verificeret."

        raise OpenAwsException(
            400,
            message,
            "Unauthorized",
        )

    if not isinstance(user_read, UserRead):
        raise OpenAwsException(500, "System fejl. Prøv igen senere.", "Unauthorized")


def me_read(request: request) -> dict:

    client: AuthenticatedClient = get_auth_client(request)
    me = users_me_get.sync(client=client)

    if isinstance(me, UserRead):
        me_dict = me.to_dict()
        return me_dict
    
    # Clear jwt session
    OpenAwsSession.clear_jwt_session()

    raise OpenAwsException(
        422,
        "For at se denne side skal du være logget ind.",
    )


def user_request_verify(request: request):
    """request for at token send by email. function used in order to verify email."""
    client: Client = get_client()

    me = me_read(request)
    email = me["id"]

    json_body = RequestVerifyPost.from_dict({"email": email})
    response = auth_request_verify_post.sync(client=client, json_body=json_body)
    if not isinstance(response, str):
        raise OpenAwsException(
        422,
        "Systemet kunne ikke afsende en verificerings e-mail. Prøv igen senere.",
    )
