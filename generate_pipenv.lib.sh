#!/usr/bin/env bash

# This should be changed to different github link that points to our particular project
# #egg=[] should be specified in order to run.
#Example: pipenv install -e git+https://github.com/requests/requests.git#egg=requests
#pipenv install -e git+https://github.com/faraonc/hwsc-api-blocks@master#egg=hwsc_transaction_svc_pb
#git sparse checkout
#how to make a repo pipenv

pipenv install grpcio-tools
pipenv install googleapis-common-protos
