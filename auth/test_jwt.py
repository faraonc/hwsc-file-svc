import pytest
from auth import jwt
from contextlib import nullcontext as does_not_raise
import time


@pytest.mark.parametrize("input_token, expectation, description",
                         [
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==" , does_not_raise(), "test valid token length"),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ" , pytest.raises(ValueError), "test invalid token with missing 1 element"),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", pytest.raises(ValueError), "test invalid token with missing 2 elements"),
                            ("", pytest.raises(ValueError), "test invalid token with empty string"),
                         ]
                         )
def test_validate_token_len(input_token, expectation, description):
    with expectation:
        jwt.validate_token_len(input_token)


@pytest.mark.parametrize("input_str, expect_output, expectation, description",
                         [
                            ("", {}, pytest.raises(ValueError), "test invalid input with empty input string"),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': jwt.AlgEnum.HS512, 'TokenTyp': jwt.TokenTypEnum.JWT}, does_not_raise(), "test valid decoded header"),
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid decoded body"),
                         ]
                         )
def test_base64_decode(input_str, expect_output, expectation, description):
    with expectation:
        actual_output = jwt.base64_decode(input_str)
        assert actual_output == expect_output, description


@pytest.mark.parametrize("input_str, expect_output, description",
                         [
                             ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': jwt.AlgEnum.HS512, 'TokenTyp': jwt.TokenTypEnum.JWT}, "test get decoded header"),
                         ]
                         )
def test_get_decoded_header(input_str, expect_output, description):
    actual_output = jwt.get_decoded_header(input_str)
    assert actual_output == expect_output, description


@pytest.mark.parametrize("input_str, expect_output, description",
                         [
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, "test get decoded body"),
                         ]
                         )
def test_get_decoded_body(input_str, expect_output, description):
    actual_output = jwt.get_decoded_body(input_str)
    assert actual_output == expect_output, description


@pytest.mark.parametrize("input_header_dict, expectation, description",
                         [
                             ("", pytest.raises(ValueError), "test invalid input with empty header_dict"),
                             ({'Alg': jwt.AlgEnum.MIN, 'TokenTyp': jwt.TokenTypEnum.JWT}, pytest.raises(ValueError), "test invalid Alg"),
                             ({'Alg': jwt.AlgEnum.MAX, 'TokenTyp': jwt.TokenTypEnum.JWT}, pytest.raises(ValueError), "test invalid Alg"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.MIN}, pytest.raises(ValueError), "test invalid TokenTyp"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.MAX}, pytest.raises(ValueError), "test invalid TokenTyp"),
                             ({'Alg': jwt.AlgEnum.NO_ALG, 'TokenTyp': jwt.TokenTypEnum.JWT}, does_not_raise(), "test valid Alg"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.JWT}, does_not_raise(), "test valid Alg"),
                             ({'Alg': jwt.AlgEnum.HS512, 'TokenTyp': jwt.TokenTypEnum.JWT}, does_not_raise(), "test valid Alg"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.NO_TYPE}, does_not_raise(), "test valid TokenTyp"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.JWT}, does_not_raise(), "test valid TokenTyp"),
                             ({'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.JET}, does_not_raise(), "test valid TokenTyp"),
                         ]
                         )
def test_validate_header(input_header_dict, expectation, description):
    with expectation:
        jwt.validate_header(input_header_dict)


@pytest.mark.parametrize("input_body_dict, expectation, description",
                         [
                             ("", pytest.raises(ValueError), "test invalid input: empty body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with shorter length"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dxxx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with longer length"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d!', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with special case"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.MIN, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid Permission"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.MAX, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid Permission"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 0}, pytest.raises(ValueError), "test invalid Timestamp"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': time.time()}, pytest.raises(ValueError), "test invalid Timestamp"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.NO_PERMISSION, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.USER_REGISTRATION, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.USER, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': jwt.PermissionEnum.ADMIN, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                         ]
                         )
def test_validate_body(input_body_dict, expectation, description):
    with expectation:
        jwt.validate_body(input_body_dict)


@pytest.mark.parametrize("permission, alg, expectation, description",
                         [
                             (jwt.PermissionEnum.ADMIN, jwt.AlgEnum.HS512, does_not_raise(), "test matched permission with alg"),
                             (jwt.PermissionEnum.ADMIN, jwt.AlgEnum.MIN, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (jwt.PermissionEnum.ADMIN, jwt.AlgEnum.NO_ALG, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (jwt.PermissionEnum.ADMIN, jwt.AlgEnum.HS256, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (jwt.PermissionEnum.ADMIN, jwt.AlgEnum.MAX, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                         ]
                         )
def test_validate_permission_with_alg(permission, alg, expectation, description):
    with expectation:
        jwt.validate_permission_with_alg(permission, alg)


@pytest.mark.parametrize("req_permission, token_permission, expectation, description",
                         [
                             (jwt.PermissionEnum.MIN, jwt.PermissionEnum.USER_REGISTRATION, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.NO_PERMISSION, jwt.PermissionEnum.USER_REGISTRATION, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.USER_REGISTRATION, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MIN, jwt.PermissionEnum.USER, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.NO_PERMISSION, jwt.PermissionEnum.USER, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.USER, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.USER, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MIN, jwt.PermissionEnum.ADMIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.NO_PERMISSION, jwt.PermissionEnum.ADMIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.ADMIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.ADMIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.ADMIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MIN, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.NO_PERMISSION, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.MAX, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MIN, jwt.PermissionEnum.MIN, does_not_raise(), "test req_permission <= token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.MIN, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.NO_PERMISSION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.USER_REGISTRATION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.USER, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.MAX, jwt.PermissionEnum.ADMIN, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.MIN, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.NO_PERMISSION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.USER_REGISTRATION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.ADMIN, jwt.PermissionEnum.USER, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.MIN, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.NO_PERMISSION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.USER, jwt.PermissionEnum.USER_REGISTRATION, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.MIN, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (jwt.PermissionEnum.USER_REGISTRATION, jwt.PermissionEnum.NO_PERMISSION, pytest.raises(ValueError), "test req_permission > token_permission"),
                         ]
                         )
def test_validate_permission_requirement(req_permission, token_permission, expectation, description):
    with expectation:
        jwt.validate_permission_requirement(req_permission, token_permission)


@pytest.mark.parametrize("header_body_token, secret_key, header_dict, signature_token, expectation, description",
                         [
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': jwt.AlgEnum.MIN, 'TokenTyp': jwt.TokenTypEnum.JWT},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': jwt.AlgEnum.NO_ALG, 'TokenTyp': jwt.TokenTypEnum.JWT},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': jwt.AlgEnum.HS256, 'TokenTyp': jwt.TokenTypEnum.JWT},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': jwt.AlgEnum.HS512, 'TokenTyp': jwt.TokenTypEnum.JWT},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg",
                                 pytest.raises(ValueError), "test invalid signature_token"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': jwt.AlgEnum.HS512, 'TokenTyp': jwt.TokenTypEnum.JWT},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 does_not_raise(), "valid testing"
                             ),
                         ]
                         )
def test_validate_signature(header_body_token, secret_key, header_dict, signature_token, expectation, description):
    with expectation:
        jwt.validate_signature(header_body_token, secret_key, header_dict, signature_token)


@pytest.mark.parametrize("token_str, secret_key, req_permission, expectation, description",
                         [
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 jwt.PermissionEnum.USER, does_not_raise(),
                                 "test valid512JWTAdminTokenString with req_permission is USER"
                             ),
                             (
                                 "eyJBbGciOjEsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.xtOMEMbgD9YH0SDVChgSy6vykf9z-9eD0_pCK--uwQQ=",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 jwt.PermissionEnum.NO_PERMISSION, pytest.raises(ValueError),
                                 "test invalid256JWTTokenString with req_permission is USER"
                             ),
                         ]
                         )
def test_validate(token_str, secret_key, req_permission, expectation, description):
    with expectation:
        jwt.validate(token_str, secret_key, req_permission)
