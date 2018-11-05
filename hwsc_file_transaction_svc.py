import os
from concurrent import futures

import grpc
import time

import hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc

CHUNK_SIZE = 1024 * 1024

def download_chunk(reqFile):
    with open(reqFile, 'readFile')as f:
        while True:
            chunk = f.read(CHUNK_SIZE);
            if len(chunk) == 0:
                return
            yield hwsc_file_transaction_svc_pb2.chunk(buffer=chunk)

def upload_chunk(chunk, reqFile):
    with open(reqFile,'wb') as f:
        for line in chunk:
            f.write(line.buffer)

class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
    def __init__(self):

        class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
            def __init__(self):
                pass

            def GetStatus(self, request, context):
                print("Get Status")

            def DownloadZipFiles(self,downloadRequest,context):
                if downloadRequest.name:
                    return download_chunk(self.tmp_file_name)

            def UploadFile(self, request_iterator, context):
                print("[INFO] Requesting UploadFile service")
                upload_chunk(request_iterator, 'dummy_img.jpg')
                return hwsc_file_transaction_svc_pb2.FileTransactionResponse(message='Hello', url='world', length=64)

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
