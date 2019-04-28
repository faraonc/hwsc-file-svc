import pytest
from auth import jwt
from contextlib import contextmanager


@contextmanager
def does_not_raise():
    yield

@pytest.mark.parametrize("input, expectation",
                         [
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg==" , does_not_raise()),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ" , pytest.raises(ValueError)),
                            ("eyJBbGciOjIsIlRva2VuVHlwIjoxfQ", pytest.raises(ValueError)),
                            ("", pytest.raises(ValueError)),
                        ])

def test_validate_token_len(input, expectation):
    with expectation:
        jwt.validate_token_len(input)