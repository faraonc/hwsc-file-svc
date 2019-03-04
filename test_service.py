import grpc
import pytest
import service
from hwsc_file_transaction_svc_pb2 import FileTransactionRequest
from hwsc_file_transaction_svc_pb2 import FileTransactionResponse


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


@pytest.mark.parametrize("input, expected_output, desc",
                         [
                             (service.State.AVAILABLE,
                              {"code": grpc.StatusCode.OK.value[0],
                               "message": grpc.StatusCode.OK.name},
                              "test for AVAILABLE"),

                             (service.State.UNAVAILABLE,
                              {"code": grpc.StatusCode.UNAVAILABLE.value[0],
                               "message": grpc.StatusCode.UNAVAILABLE.name},
                              "testfor UNAVAILABLE"),
                         ]
                         )
def test_GetStatus(input, expected_output, desc):
    server = service.Server()
    server.set_state(input)
    file_trans_svc = service.FileTransactionService(server)
    request = FileTransactionRequest()
    context = FakeContext()

    response = file_trans_svc.GetStatus(request, context)
    assert response.code == expected_output["code"]
    assert response.message == expected_output["message"]
