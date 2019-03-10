#!/bin/bash

# clean up files
rm hwsc-file-transaction-svc.proto
rm hwsc_file_transaction_svc_pb2.py
rm hwsc_file_transaction_svc_pb2_grpc.py
rm protobuf/lib/authority.proto
rm protobuf/lib/authority_pb2.py
rm protobuf/lib/authority_pb2_grpc.py

# pull proto and protocol buffers
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/hwsc-file-transaction-svc.proto
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2_grpc.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/protobuf/lib/authority.proto -P protobuf/lib/
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/protobuf/lib/authority_pb2.py -P protobuf/lib/
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/protobuf/hwsc-file-transaction-svc/file/protobuf/lib/authority_pb2_grpc.py -P protobuf/lib/
pipenv install --dev
