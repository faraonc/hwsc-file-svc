import os
from concurrent import futures

import grpc
import time

import hwsc_file_transaction_svc_pb2 as hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc as hwsc_file_transaction_svc_pb2_grpc

CHUNK_SIZE = 1024 * 1024

def download_chunk(reqFile):
    with open(reqFile, 'readFile')as f:
        while True:
            chunk = f.read(CHUNK_SIZE);
            if len(chunk) == 0:
                return
            yield hwsc_file_transaction_svc_pb2.chunk(buffer=chunk)

def upload_chunk(chunk, reqFile):
    with open(reqFile,'writeFile') as f:
        for line in chunk:
            f.write(line.buffer)

class FileTransactionClient:
    def __init__(self,address):
        channel = grpc.insecure_channel(address)
        self.stub = hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceStub(channel)

    def upload(self,target_file):
        chunk = download_chunk(target_file)
        response = self.stub.UploadFile(chunk)
        assert response.length == os.path.getsize(target_file)

    def download(self,target_file,response_file):
        response = self.stub.DownloadFile(hwsc_file_transaction_svc_pb2.Request(name=target_file))
        upload_chunk(response,response_file)

class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
    def __init__(self):

        class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
            def __init__(self):
                # pass
                self.tmp_file_name = ''

            def GetStatus(self, request, context):
                print("Get Status")

            def download(self,downloadRequest,context):
                if downloadRequest.name:
                    return download_chunk(self.tmp_file_name)

            def upload(self,uploadRequest,context):
                upload_chunk(uploadRequest,self.tmp_file_name)
                return hwsc_file_transaction_svc_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
            hwsc_file_transaction_svc_pb2_grpc.add_FileTransactionServiceServicer_to_server(Servicer(), self.server)

    def start(self, port):
        print("1")

        self.server.add_insecure_port(f'[::]:{port}')
        print("2")

        self.server.start()
        print("3")

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)
