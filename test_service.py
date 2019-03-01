import service
import pytest

@pytest.mark.parametrize("input, expected_output, desc",
                         [
                            (service.State.AVAILABLE, {"code": 0, "msg": "OK"}, "test for AVAILABLE"),
                            (service.State.UNAVAILABLE, {"code": 0, "msg": "OK"}, "testfor UNAVAILABLE"),
                         ]
                         )
def test_GetStatus(input, expected_output, desc):
    s = service.FileTransactionService()
    s.set_state(input)
    req = hwsc_file_transaction_svc_pb2.FileTransactionRequest()
    # ctx = grpc.ServicerContext()
    print(s.GetStatus(req, None))

    # actual_output = utility.get_file_type(input)
    # assert s.get_state() == expected_output

