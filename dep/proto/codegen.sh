#!/usr/bin/env bash

python -m grpc_tools.protoc -I. --python_out=proto --grpc_python_out=/proto ./hwsc-file-svc.proto