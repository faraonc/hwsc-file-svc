import pytest
from auth import jwt
from contextlib import nullcontext as does_not_raise
import time


@pytest.mark.parametrize("input_token, expectation",
                         [
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==" , does_not_raise()),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ" , pytest.raises(ValueError)),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", pytest.raises(ValueError)),
                            ("", pytest.raises(ValueError)),
                         ]
                         )
def test_validate_token_len(input_token, expectation):
    with expectation:
        jwt.validate_token_len(input_token)


@pytest.mark.parametrize("input_str, expect_output, expectation",
                         [
                            ("", {}, pytest.raises(ValueError)),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': 2, 'TokenTyp': 1}, does_not_raise()),
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, does_not_raise()),
                         ]
                         )
def test_base64_decode(input_str, expect_output, expectation):
    with expectation:
        actual_output = jwt.base64_decode(input_str)
        assert actual_output == expect_output


@pytest.mark.parametrize("input_str, expect_output",
                         [
                             ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", {'Alg': 2, 'TokenTyp': 1}),
                         ]
                         )
def test_get_decoded_header(input_str, expect_output):
    actual_output = jwt.get_decoded_header(input_str)
    assert actual_output == expect_output


@pytest.mark.parametrize("input_str, expect_output",
                         [
                            ("eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ", {'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}),
                         ]
                         )
def test_get_decoed_body(input_str, expect_output):
    actual_output = jwt.get_decoded_body(input_str)
    assert actual_output == expect_output


@pytest.mark.parametrize("input_header_dict, expectation",
                         [
                             ("", pytest.raises(ValueError)),
                             ({'Alg': -1, 'TokenTyp': 1}, pytest.raises(ValueError)),
                             ({'Alg': 3, 'TokenTyp': 1}, pytest.raises(ValueError)),
                             ({'Alg': 1, 'TokenTyp': -1}, pytest.raises(ValueError)),
                             ({'Alg': 1, 'TokenTyp': 3}, pytest.raises(ValueError)),
                             ({'Alg': 0, 'TokenTyp': 1}, does_not_raise()),
                             ({'Alg': 1, 'TokenTyp': 1}, does_not_raise()),
                             ({'Alg': 2, 'TokenTyp': 1}, does_not_raise()),
                             ({'Alg': 1, 'TokenTyp': 0}, does_not_raise()),
                             ({'Alg': 1, 'TokenTyp': 1}, does_not_raise()),
                             ({'Alg': 1, 'TokenTyp': 2}, does_not_raise()),
                         ]
                         )
def test_validate_header(input_header_dict, expectation):
    with expectation:
        jwt.validate_header(input_header_dict)


@pytest.mark.parametrize("input_body_dict, expectation",
                         [
                             ("", pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dxxx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9d!', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': -1, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 4, 'ExpirationTimestamp': 1893456000}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 0}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': time.time()}, pytest.raises(ValueError)),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 0, 'ExpirationTimestamp': 1893456000}, does_not_raise()),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 1, 'ExpirationTimestamp': 1893456000}, does_not_raise()),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 2, 'ExpirationTimestamp': 1893456000}, does_not_raise()),
                             ({'UUID': '01d3x3wm2nnrdfzp0tka2vw9dx', 'Permission': 3, 'ExpirationTimestamp': 1893456000}, does_not_raise()),
                         ]
                         )
def test_validate_body(input_body_dict, expectation):
    with expectation:
        jwt.validate_body(input_body_dict)


@pytest.mark.parametrize("permission, alg, expectation",
                         [
                             (3, 2, does_not_raise()),
                             (3, -1, pytest.raises(ValueError)),
                             (3, 0, pytest.raises(ValueError)),
                             (3, 1, pytest.raises(ValueError)),
                             (3, 3, pytest.raises(ValueError)),
                         ]
                         )
def test_validate_permission_with_alg(permission, alg, expectation):
    with expectation:
        jwt.validate_permission_with_alg(permission, alg)


@pytest.mark.parametrize("req_permission, token_permission, expectation",
                         [
                             (-1, 1, does_not_raise()),
                             (0, 1, does_not_raise()),
                             (1, 1, does_not_raise()),
                             (-1, 2, does_not_raise()),
                             (0, 2, does_not_raise()),
                             (1, 2, does_not_raise()),
                             (2, 2, does_not_raise()),
                             (-1, 3, does_not_raise()),
                             (0, 3, does_not_raise()),
                             (1, 3, does_not_raise()),
                             (2, 3, does_not_raise()),
                             (3, 3, does_not_raise()),
                             (-1, 4, does_not_raise()),
                             (0, 4, does_not_raise()),
                             (1, 4, does_not_raise()),
                             (2, 4, does_not_raise()),
                             (3, 4, does_not_raise()),
                             (4, 4, does_not_raise()),
                             (-1, -1, does_not_raise()),
                             (4, -1, pytest.raises(ValueError)),
                             (4, 0, pytest.raises(ValueError)),
                             (4, 1, pytest.raises(ValueError)),
                             (4, 2, pytest.raises(ValueError)),
                             (4, 3, pytest.raises(ValueError)),
                             (3, -1, pytest.raises(ValueError)),
                             (3, 0, pytest.raises(ValueError)),
                             (3, 1, pytest.raises(ValueError)),
                             (3, 2, pytest.raises(ValueError)),
                             (2, -1, pytest.raises(ValueError)),
                             (2, 0, pytest.raises(ValueError)),
                             (2, 1, pytest.raises(ValueError)),
                             (1, -1, pytest.raises(ValueError)),
                             (1, 0, pytest.raises(ValueError)),
                         ]
                         )
def test_validate_permission_requirement(req_permission, token_permission, expectation):
    with expectation:
        jwt.validate_permission_requirement(req_permission, token_permission)


@pytest.mark.parametrize("header_body_token, secret_key, header_dict, signature_token, expectation",
                         [
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': -1, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError)
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 0, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError)
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 1, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 pytest.raises(ValueError)
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 2, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg",
                                 pytest.raises(ValueError)
                             ),
                             (
                                 "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ",
                                 "j2Yzh-VcIm-lYUzBuqt8TVPeUHNYB5MP1gWvz3Bolow=",
                                 {'Alg': 2, 'TokenTyp': 1},
                                 "8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==",
                                 does_not_raise()
                             ),
                         ]
                         )
def test_validate_signature(header_body_token, secret_key, header_dict, signature_token, expectation):
    with expectation:
        jwt.validate_signature(header_body_token, secret_key, header_dict, signature_token)
