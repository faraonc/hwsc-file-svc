import grpc
import pytest
import server
from fake import FakeContext
from file_transaction_service import FileTransactionService
from hwsc_file_transaction_svc_pb2 import FileTransactionRequest


@pytest.mark.parametrize("input, expected_output, desc",
                         [
                             (server.State.AVAILABLE,
                              {"code": grpc.StatusCode.OK.value[0],
                               "message": grpc.StatusCode.OK.name},
                              "test for state AVAILABLE"),

                             (server.State.UNAVAILABLE,
                              {"code": grpc.StatusCode.UNAVAILABLE.value[0],
                               "message": grpc.StatusCode.UNAVAILABLE.name},
                              "test for state UNAVAILABLE"),
                         ]
                         )
def test_GetStatus(input, expected_output, desc):
    s = server.Server()
    s.set_state(input)
    file_trans_svc = FileTransactionService(s)
    req = FileTransactionRequest()
    ctx = FakeContext()

    response = file_trans_svc.GetStatus(req, ctx)
    assert response.code == expected_output["code"]
    assert response.message == expected_output["message"]
