import os
from concurrent import futures

import grpc
import time

import dep.proto.hwsc_file_svc_pb2_grpc as hwsc_file_svc_pb2_grpc

class FileService(hwsc_file_svc_pb2_grpc.FileServiceServicer):
    def __init__(self):

        class Servicer(hwsc_file_svc_pb2_grpc.FileServiceServicer):
            def __init__(self):
                pass

            def GetStatus(self, request, context):
                print("Get Status")

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        hwsc_file_svc_pb2_grpc.add_FileServiceServicer_to_server(Servicer(), self.server)

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