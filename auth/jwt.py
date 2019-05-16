import base64
import json
import hmac
import hashlib
from enum import IntEnum
from utility import utility


class AlgEnum(IntEnum):
    MIN = -1
    NO_ALG = 0
    HS256 = 1
    HS512 = 2
    MAX = 3


class TokenTypEnum(IntEnum):
    MIN = -1
    NO_TYPE = 0
    JWT = 1
    JET = 2
    MAX = 3


class PermissionEnum(IntEnum):
    MIN = -1
    NO_PERMISSION = 0
    USER_REGISTRATION = 1
    USER = 2
    ADMIN = 3
    MAX = 4


def validate_token_len(token_str):
    """Validate the length of the token_str
    throws ValueError if token_str is empty
    throws ValueError if token_str doesn't have 3 elements header.body.signature
    """

    if not token_str:
        raise ValueError("token string is None")

    result = token_str.strip().split(".")
    if len(result) != 3:
        raise ValueError("invalid token")


def base64_decode(input_str):
    """Decode a token string
    throws ValueError if input_str is empty
    return a decoded dictionary for the valid input_str
    """

    if not input_str:
        raise ValueError("base64 decode input string is None")

    for x in range(4 - (len(input_str) % 4)):
        input_str += "="

    base64_str = (base64.b64decode(input_str)).decode()
    base64_dict = json.loads(base64_str)

    return base64_dict


def get_decoded_header(header_str):
    """Get the decoded header_dict with the input header_str"""

    return base64_decode(header_str)


def get_decoded_body(body_str):
    """Get the decoded body_dict with the input body_str"""

    return base64_decode(body_str)


def validate_header(header_dict):
    """Validate a header_dict
    throws ValueError if header_dict is empty
    throws ValueError if Alg <= -1 or >= 3
    throws ValueError if TokenTyp <= -1 or >=3
    """

    if not header_dict:
        raise ValueError("header_dict is None")

    alg = header_dict["Alg"]
    if alg <= AlgEnum.MIN or alg >= AlgEnum.MAX:
        raise ValueError("invalid Alg")

    token_typ = header_dict["TokenTyp"]
    if token_typ <= TokenTypEnum.MIN or token_typ >= TokenTypEnum.MAX:
        raise ValueError("invalid TokenTyp")


def validate_body(body_dict):
    """Validate a body_dict
   throws ValueError if body_dict is empty
   throws ValueError for invalid UUID
   throws ValueError if Permission <= -1 or >=4
   throws ValueError if ExpirationTimestamp is expired
   """

    if not body_dict:
        raise ValueError("body_dict is None")

    uuid = body_dict["UUID"]
    if not utility.verify_uuid(uuid):
        raise ValueError("UUID not valid")

    permission = body_dict["Permission"]
    if permission <= PermissionEnum.MIN or permission >= PermissionEnum.MAX:
        raise ValueError("invalid permission")

    expiration_timestamp = body_dict["ExpirationTimestamp"]
    if utility.is_expired(expiration_timestamp):
        raise ValueError("ExpirationTimestamp not valid")


def validate_permission_with_alg(permission, alg):
    """Validate ADMIN permission with HS512 Alg
    throws ValueError if the token is ADMIN permission but Alg is not HS512
    """

    if permission == PermissionEnum.ADMIN and alg != AlgEnum.HS512:
        raise ValueError("admin permission not valid")


def validate_permission_requirement(req_permission, token_permission):
    """Validate token_permission >= req_permission
    throws ValueError if req_permission > token_permission
    """

    if req_permission > token_permission:
        raise ValueError("invalid permission requirement")


def validate_signature(header_body_token, secret_key, header_dict, signature_token):
    """Rebuild and validate a signature
    throws ValueError if Alg is not HS256 or HS512
    throws ValueError if the rebuild signature != signature_token
    """

    if header_dict["Alg"] == AlgEnum.HS256:
        signature_rebuild = base64.urlsafe_b64encode(hmac.new(secret_key.encode(),
                                                              header_body_token.encode(),
                                                              hashlib.sha256).digest()).decode()
    elif header_dict["Alg"] == AlgEnum.HS512:
        signature_rebuild = base64.urlsafe_b64encode(hmac.new(secret_key.encode(),
                                                              header_body_token.encode(),
                                                              hashlib.sha512).digest()).decode()
    else:
        raise ValueError("invalid Alg")

    if signature_rebuild != signature_token:
        raise ValueError("invalid Signature")


def validate(token_str, secret_key, req_permission):
    """Validate a token with secret_key and req_permission"""

    # split the token_str to get a list of header, body, signature
    token_list = token_str.strip().split(".")
    # get the header.body token from the token_list
    header_body_token = token_list[0] + "." + token_list[1]
    # get the signature of the token from the token_list
    signature_token = token_list[2]
    # validate if the token_str has 3 elements
    validate_token_len(token_str)
    # decode header token to get the header dictionary
    header_dict = get_decoded_header(token_list[0])
    # decode body token to get the body dictionary
    body_dict = get_decoded_body(token_list[1])
    # validate header dictionary
    validate_header(header_dict)
    # validate body dictionary
    validate_body(body_dict)
    # validate the signature by rebuild from the header.body token and compared to the original signature
    validate_signature(header_body_token, secret_key, header_dict, signature_token)
    # validate permission ADMIN and Alg HS512
    validate_permission_with_alg(body_dict["Permission"], header_dict["Alg"])
    # Validate requirement permission with the token permission
    validate_permission_requirement(req_permission, body_dict["Permission"])
