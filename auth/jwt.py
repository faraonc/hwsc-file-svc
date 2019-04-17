import base64
import json
import traceback
import hmac
import hashlib
import binascii
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
    if not token_str:
        raise ValueError("token string is None")
    result = token_str.strip().split('.')
    if len(result) != 3:
        raise ValueError("invalid token")


def base64_decode(input_str):
    if not input_str:
        raise ValueError("base64 decode input string is None")

    for x in range(4 - (len(input_str) % 4)):
        input_str += "="

    base64_str = (base64.b64decode(input_str)).decode()
    base64_dict = json.loads(base64_str)

    return base64_dict


def get_decoded_header(header_str):
    return base64_decode(header_str)


def get_decoded_body(body_str):
    return base64_decode(body_str)


def validate_header(header_dict):
    if not header_dict:
        raise ValueError("header dict is None")

    alg = header_dict["Alg"]
    if alg <= AlgEnum.MIN or alg >= AlgEnum.MAX:
        raise ValueError("invalid Alg")

    token_typ = header_dict["TokenTyp"]
    if token_typ <= TokenTypEnum.MIN or token_typ >= TokenTypEnum.MAX:
        raise ValueError("invalid TokenTyp")


def validate_body(body_dict):
    if not body_dict:
        raise ValueError("body dict is None")

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
    if permission == PermissionEnum.ADMIN and alg != AlgEnum.HS512:
        raise ValueError("admin permission not valid")


def validate_signature(header_body_token, secret_key):
    # print(header_body_token)
    # print(secret_key)
    # byte_key = binascii.b2a_hex(secret_key)
    signature_hs_512 = hmac.new(secret_key.encode(), header_body_token.encode(), hashlib.sha512).hexdigest()
    print(signature_hs_512)


# if __name__ == "__main__":
def test():
    token = "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg=="
    secret_key = "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow="

    try:
        validate_token_len(token)
        token_list = token.strip().split('.')
        header_dict = get_decoded_header(token_list[0])
        validate_header(header_dict)
        body_dict = get_decoded_body(token_list[1])
        validate_body(body_dict)
        header_body_token = token_list[0] + "." + token_list[1]
        validate_signature(header_body_token, secret_key)
        print(token_list[2])


    except ValueError as err:
        traceback.print_exc()

    except Exception as err:
        traceback.print_exc()