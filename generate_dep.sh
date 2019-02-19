#!/bin/bash

# clean up files
rm hwsc-file-transaction-svc.proto
rm hwsc_file_transaction_svc_pb2.py
rm hwsc_file_transaction_svc_pb2_grpc.py
rm lib/authority.proto
rm lib/authority_pb2.py
rm lib/authority_pb2_grpc.py

# pull proto and protocol buffers
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc-file-transaction-svc.proto
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2_grpc.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/lib/authority.proto -P lib/
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/lib/authority_pb2.py -P lib/
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/lib/authority_pb2_grpc.py -P lib/
pipenv install --dev
