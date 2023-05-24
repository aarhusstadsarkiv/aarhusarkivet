from openaws import (
    HTTPValidationError,
    ErrorModel,
)


class OpenAwsException(Exception):
    def __init__(self, status_code: int, message: str, text: str = ""):
        self.status_code = status_code
        self.message = message
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


def extract_validation_error(error_dict):
    try:
        error_detail = error_dict['detail']
        if isinstance(error_detail, list) and len(error_detail) > 0:
            first_error = error_detail[0]
            error_type = first_error.get('type')
            return error_type
    except (KeyError, IndexError):
        pass

    return "value_error.unknown_error"


def extract_model_error(error_dict):
    try:
        if isinstance(error_dict.get('detail'), dict):
            error_code = error_dict['detail'].get('code')
        else:
            error_code = error_dict.get('detail')
    except KeyError:
        error_code = "UNKNOWN_MODEL_ERROR"

    return error_code


def get_error_string(error):
    # register errors
    if error == "REGISTER_INVALID_PASSWORD":
        return "Password skal mindst være 8 tegn langt."
    if error == "REGISTER_USER_ALREADY_EXISTS":
        return "En bruger med denne email eksisterer allerede. Du kan anmode om et nyt password."
    if error == "value_error.email":
        return "Email skal være korrekt."

    # verify errors
    if error == "VERIFY_USER_BAD_TOKEN":
        return "Nøglen eksisterer ikke i systemet. Eller den er udløbet. Du må logge ind for at få tilsendt en ny nøgle."
    if error == "VERIFY_USER_ALREADY_VERIFIED":
        return "Bruger er allerede verificeret."

    # login errors
    if error == "LOGIN_BAD_CREDENTIALS":
        return "Email eller password er forkert."
    if error == "LOGIN_USER_NOT_VERIFIED":
        return "Bruger er ikke verificeret. Tjek din email for at verificere din bruger."

    # reset password errors
    if error == "RESET_PASSWORD_BAD_TOKEN":
        return "Nøglen eksisterer ikke i systemet. Eller den er udløbet. Du må anmode om en mail under 'Glemt password'."
    if error == "RESET_PASSWORD_INVALID_PASSWORD":
        return "Password skal mindst være 8 tegn langt."

    # unknow errors
    if error == "value_error.unknown_error":
        return "Ukendt fejl i validering af data. Prøv igen senere."
    if error == "UNKNOWN_MODEL_ERROR":
        return "Ukendt fejl i validering af data. Prøv igen senere."


def validate_response(error):
    raise_message = None
    if isinstance(error, ErrorModel):
        error_message = error.to_dict()
        error_code = extract_model_error(error_message)
        raise_message = get_error_string(error_code)

    if isinstance(error, HTTPValidationError):
        error_message = error.to_dict()
        error_code = extract_validation_error(error_message)
        raise_message = get_error_string(error_code)

    if raise_message:
        raise OpenAwsException(400, raise_message)
