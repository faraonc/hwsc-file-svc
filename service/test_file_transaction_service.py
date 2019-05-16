import grpc
import pytest
from service import server
import string
import random
from azure_client import azure_client
import config
from azure.storage.blob import BlockBlobService
from service.fake import FakeContext
from service.file_transaction_service import FileTransactionService
from hwsc_file_transaction_svc_pb2 import FileTransactionRequest


@pytest.mark.parametrize("state_input, azure_input, expected_output, desc",
                         [
                             (server.State.AVAILABLE,
                              None,
                              {"code": grpc.StatusCode.UNAVAILABLE.value[0],
                               "message": grpc.StatusCode.UNAVAILABLE.name},
                              "test for state UNAVAILABLE"),

                             (server.State.UNAVAILABLE,
                              None,
                              {"code": grpc.StatusCode.UNAVAILABLE.value[0],
                               "message": grpc.StatusCode.UNAVAILABLE.name},
                              "test for state UNAVAILABLE"),

                             (server.State.AVAILABLE,
                              BlockBlobService(connection_string=config.CONFIG["blob_storage"]),
                              {"code": grpc.StatusCode.OK.value[0],
                               "message": grpc.StatusCode.OK.name},
                              "test for state AVAILABLE"),

                             (server.State.UNAVAILABLE,
                              BlockBlobService(connection_string=config.CONFIG["blob_storage"]),
                              {"code": grpc.StatusCode.UNAVAILABLE.value[0],
                               "message": grpc.StatusCode.UNAVAILABLE.name},
                              "test for state UNAVAILABLE"),
                         ]
                         )
def test_GetStatus(state_input, azure_input, expected_output, desc):
    s = server.Server()
    s.set_state(state_input)
    file_trans_svc = FileTransactionService(s)
    azure_client.block_blob_service = azure_input
    req = FileTransactionRequest()
    ctx = FakeContext()

    response = file_trans_svc.GetStatus(req, ctx)
    assert response.code == expected_output["code"]
    assert response.message == expected_output["message"]


valid_uuid_1 = "".join(random.choices(string.ascii_lowercase + string.digits, k=26))


@pytest.mark.parametrize("uuid_input, expected_output, desc",
                         [
                             (valid_uuid_1,
                              {"code": grpc.StatusCode.OK.value[0],
                               "message": "user folder creation successful"},
                              "test for successful user folder creation"),

                             (valid_uuid_1,
                              {"code": grpc.StatusCode.UNKNOWN.value[0],
                               "message": "user folder already exists"},
                              "test for preexisting folder"),

                             ("1234abcd5454efef8842ll3fs",
                              {"code": grpc.StatusCode.UNKNOWN.value[0],
                               "message": "invalid uuid"},
                              "test for invalid uuid"),
                         ]
                         )
def test_CreateUserFolder(uuid_input, expected_output, desc):
    s = server.Server()
    file_trans_svc = FileTransactionService(s)
    req = FileTransactionRequest()
    req.uuid = uuid_input
    ctx = FakeContext()

    response = file_trans_svc.CreateUserFolder(req, ctx)
    assert response.code == expected_output["code"]
    assert response.message == expected_output["message"]
