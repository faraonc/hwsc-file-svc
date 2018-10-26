import os
from concurrent import futures

import grpc
import time

import hwsc_file_transaction_svc_pb2, hwsc_file_transaction_svc_pb2_grpc

SEGMENT_SIZE = 1024 * 1024  //1MB

def download_segment(reqFile):
    with open(reqFile, 'readFile')as f:
        while True:
            segment = f.read(SEGMENT_SIZE);
            if len(segment) == 0:
                return
            yield hwsc_file_transaction_svc_pb2.Segment(buffer=segment)

def upload_segment(segments, reqFile):
    with open(reqFile,'writeFile') as f:
        for line in segments:
            f.write(line.buffer)

class FileTransactionClient:
    def__init__(self,address):
        channel = grpc.insecure_channel(address)
        self.stub = hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceStub(channel)

    def upload(self,target_file):
        segment = download_segment(target_file)
        response = self.stub.upload(segment)
        assert response.length == os.path.getsize(target_file)

     def download(self,target_file,response_file):
        response = self.stub.download(hwsc_file_transaction_svc_pb2.Request(name=target_file))
        upload_segment(response,response_file)

class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
    def __init__(self):

        class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
            def __init__(self):
                // pass
                self.tmp_file_name = ''

            def GetStatus(self, request, context):
                print("Get Status")

            def download(self,downloadRequest,context):
                if downloadRequest.name:
                    return download_segment(self.tmp_file_name)

            def upload(self,uploadRequest,context):
                upload_segment(uploadRequest,sef.tmp_file_name)
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