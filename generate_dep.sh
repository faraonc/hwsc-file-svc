#!/usr/bin/env bash

wget https://raw.githubusercontent.com/faraonc/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/proto/hwsc-file-transaction-svc.proto -O hwsc-file-transaction-svc.proto
wget https://raw.githubusercontent.com/faraonc/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/proto/hwsc_file_transaction_svc_pb2.py -O hwsc_file_transaction_svc_pb2.py
wget https://raw.githubusercontent.com/faraonc/hwsc-api-blocks/master/int/hwsc-file-transaction-svc/proto/hwsc_file_transaction_svc_pb2_grpc.py -O hwsc_file_transaction_svc_pb2_grpc.py
pipenv install
