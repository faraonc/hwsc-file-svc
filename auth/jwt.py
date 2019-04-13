import base64
import json
import traceback
from enum import IntEnum


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


# TODO: verify UUID
# TODO: verify ExpirationTimestamp
def validate_body(body_dict):
    if not body_dict:
        raise ValueError("body dict is None")

    permission = header_dict["Permission"]
    if permission <= PermissionEnum.MIN or permission >= PermissionEnum.MAX:
        raise ValueError("invalid permission")


def validate_permission_with_alg(permission, alg):
    if permission == PermissionEnum.ADMIN and alg != AlgEnum.HS512:
        raise ValueError("admin permission not valid")


    # header_elements = [x.strip() for x in header_value.split(',')]
    #
    # alg = [x.strip() for x in header_elements[0].split(':')]
    # alg_value = alg[1]
    #
    # TokenTyp = [x.strip() for x in header_elements[1].split(':')]
    # TokenTyp_value = TokenTyp[1]
    #
    # print("Algorithm value is : " + alg_value)
    # print("Token Type is : " + TokenTyp_value)
    #
    # return TokenTyp, TokenTyp_value

    # print(header_elements[0])
    # print(header_elements[1])
    # print(len(header_elements))
#
# else:
#     print("Invalid Token!")


# def get_body():
#     result = get_element(token)
#     body = result[1]
#
#     if (result != ""):
#         for x in range(0, (116 - len(body))):
#             body += "=";
#
#         body_value = (base64.b64decode(body)).decode()
#         print("Body is : " + body_value)
#
#     else:
#         print("Invalid Token!")
#
#
# def get_signature():
#     result = get_element(token)
#     if (result != ""):
#         signature = result[2]
#         print("Signature is : " + signature)
#
#     else:
#         print("Invalid Token!")


if __name__ == "__main__":
    token = "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg=="

    # a, b = get_header()
    # print(a)
    # print("b : " + b)

    # get_body()
    # get_signature()
    try:
        validate_token_len(token)
        token_list = token.strip().split('.')
        header_dict = get_decoded_header(token_list[0])
        validate_header(header_dict)
        body_dict = get_decoded_body(token_list[1])
        validate_body(body_dict)


    except ValueError as err:
        traceback.print_exc()

    except Exception as err:
        traceback.print_exc()
