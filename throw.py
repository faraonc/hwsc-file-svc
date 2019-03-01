import service
import pytest
import grpc
import utility
import hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc

s = service.FileTransactionService()
s.set_state(input)
req = hwsc_file_transaction_svc_pb2.FileTransactionRequest()
# ctx = grpc.RpcContext()
print(s.GetStatus(req, {}))





