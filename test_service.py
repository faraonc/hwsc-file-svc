import pytest
from hwsc_file_transaction_svc_pb2 import FileTransactionRequest


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from hwsc_file_transaction_svc_pb2_grpc import add_FileTransactionServiceServicer_to_server

    return add_FileTransactionServiceServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from service import FileTransactionService

    return FileTransactionService()


@pytest.fixture(scope="module")
def grpc_stub_cls(grpc_channel):
    from hwsc_file_transaction_svc_pb2_grpc import FileTransactionServiceStub

    return FileTransactionServiceStub


def test_GetStatus(grpc_stub):
    request = FileTransactionRequest()
    print("request =", request)
    response = grpc_stub.GetStatus(request)
    print(response)
    assert response == 1


# @pytest.mark.parametrize("input, expected_output, desc",
#                          [
#                             (service.State.AVAILABLE, {"code": 0, "msg": "OK"}, "test for AVAILABLE"),
#                             (service.State.UNAVAILABLE, {"code": 0, "msg": "OK"}, "testfor UNAVAILABLE"),
#                          ]
#                          )
# def test_GetStatus(input, expected_output):
#     request = FileTransactionRequest
#     response = grpc_servicer.
#     assert actual_output == expected_output