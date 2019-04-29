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
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': 2, 'TokenTyp': 1}, does_not_raise(), "test valid decoded header"),
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid decoded body"),
                         ]
                         )
def test_base64_decode(input_str, expect_output, expectation, description):
    with expectation:
        actual_output = jwt.base64_decode(input_str)
        assert actual_output == expect_output


@pytest.mark.parametrize("input_str, expect_output, description",
                         [
                             ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': 2, 'TokenTyp': 1}, "test get decoded header"),
                         ]
                         )
def test_get_decoded_header(input_str, expect_output, description):
    actual_output = jwt.get_decoded_header(input_str)
    assert actual_output == expect_output


@pytest.mark.parametrize("input_str, expect_output, description",
                         [
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, "test get decoded body"),
                         ]
                         )
def test_get_decoed_body(input_str, expect_output, description):
    actual_output = jwt.get_decoded_body(input_str)
    assert actual_output == expect_output


@pytest.mark.parametrize("input_header_dict, expectation, description",
                         [
                             ("", pytest.raises(ValueError), "test invalid input with empty header_dict"),
                             ({'Alg': -1, 'TokenTyp': 1}, pytest.raises(ValueError), "test invalid Alg"),
                             ({'Alg': 3, 'TokenTyp': 1}, pytest.raises(ValueError), "test invalid Alg"),
                             ({'Alg': 1, 'TokenTyp': -1}, pytest.raises(ValueError), "test invalid TokenTyp"),
                             ({'Alg': 1, 'TokenTyp': 3}, pytest.raises(ValueError), "test invalid TokenTyp"),
                             ({'Alg': 0, 'TokenTyp': 1}, does_not_raise(), "test valid Alg"),
                             ({'Alg': 1, 'TokenTyp': 1}, does_not_raise(), "test valid Alg"),
                             ({'Alg': 2, 'TokenTyp': 1}, does_not_raise(), "test valid Alg"),
                             ({'Alg': 1, 'TokenTyp': 0}, does_not_raise(), "test valid TokenTyp"),
                             ({'Alg': 1, 'TokenTyp': 1}, does_not_raise(), "test valid TokenTyp"),
                             ({'Alg': 1, 'TokenTyp': 2}, does_not_raise(), "test valid TokenTyp"),
                         ]
                         )
def test_validate_header(input_header_dict, expectation, description):
    with expectation:
        jwt.validate_header(input_header_dict)


@pytest.mark.parametrize("input_body_dict, expectation, description",
                         [
                             ("", pytest.raises(ValueError), "test invalid input: empty body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with shorter length"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dxxx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with longer length"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d!', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid UUID with special case"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': -1, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid Permission"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 4, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError), "test invalid Permission"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 0}, pytest.raises(ValueError), "test invalid Timestamp"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': time.time()}, pytest.raises(ValueError), "test invalid Timestamp"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 0, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 1, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 2, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, does_not_raise(), "test valid body_dict"),
                         ]
                         )
def test_validate_body(input_body_dict, expectation, description):
    with expectation:
        jwt.validate_body(input_body_dict)


@pytest.mark.parametrize("permission, alg, expectation, description",
                         [
                             (3, 2, does_not_raise(), "test matched permission with alg"),
                             (3, -1, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (3, 0, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (3, 1, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                             (3, 3, pytest.raises(ValueError), "test unmatched Permission with Alg"),
                         ]
                         )
def test_validate_permission_with_alg(permission, alg, expectation, description):
    with expectation:
        jwt.validate_permission_with_alg(permission, alg)


@pytest.mark.parametrize("req_permission, token_permission, expectation, description",
                         [
                             (-1, 1, does_not_raise(), "test req_permission <= token_permission"),
                             (0, 1, does_not_raise(), "test req_permission <= token_permission"),
                             (1, 1, does_not_raise(), "test req_permission <= token_permission"),
                             (-1, 2, does_not_raise(), "test req_permission <= token_permission"),
                             (0, 2, does_not_raise(), "test req_permission <= token_permission"),
                             (1, 2, does_not_raise(), "test req_permission <= token_permission"),
                             (2, 2, does_not_raise(), "test req_permission <= token_permission"),
                             (-1, 3, does_not_raise(), "test req_permission <= token_permission"),
                             (0, 3, does_not_raise(), "test req_permission <= token_permission"),
                             (1, 3, does_not_raise(), "test req_permission <= token_permission"),
                             (2, 3, does_not_raise(), "test req_permission <= token_permission"),
                             (3, 3, does_not_raise(), "test req_permission <= token_permission"),
                             (-1, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (0, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (1, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (2, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (3, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (4, 4, does_not_raise(), "test req_permission <= token_permission"),
                             (-1, -1, does_not_raise(), "test req_permission <= token_permission"),
                             (4, -1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (4, 0, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (4, 1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (4, 2, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (4, 3, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (3, -1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (3, 0, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (3, 1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (3, 2, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (2, -1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (2, 0, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (2, 1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (1, -1, pytest.raises(ValueError), "test req_permission > token_permission"),
                             (1, 0, pytest.raises(ValueError), "test req_permission > token_permission"),
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
                                 {'Alg': -1, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 0, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 1, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError), "test invalid header_dict"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 2, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg",
                                 pytest.raises(ValueError), "test invalid signature_token"
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 2, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 does_not_raise(), "valid testing"
                             ),
                         ]
                         )
def test_validate_signature(header_body_token, secret_key, header_dict, signature_token, expectation, description):
    with expectation:
        jwt.validate_signature(header_body_token, secret_key, header_dict, signature_token)
