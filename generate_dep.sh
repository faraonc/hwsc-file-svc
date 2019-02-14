#!/usr/bin/env bash

wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc-file-transaction-svc.proto
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/hwsc_file_transaction_svc_pb2_grpc.py
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/lib/authority_pb2.py -P lib/
wget https://raw.githubusercontent.com/hwsc-org/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/file/lib/authority_pb2_grpc.py lib/
pipenv install
