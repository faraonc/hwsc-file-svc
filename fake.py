import grpc


class FakeRpcError(RuntimeError, grpc.RpcError):
    """Fake RPC error for testing"""

    def __init__(self, code, details):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details


class FakeContext(object):
    """Fake context for testing"""

    def __init__(self):
        self._invocation_metadata = []

    def abort(self, code, details):
        raise FakeRpcError(code, details)

    def invocation_metadata(self):
        return self._invocation_metadata
