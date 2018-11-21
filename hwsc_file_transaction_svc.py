import os
from concurrent import futures

import grpc
import time

import hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc

CHUNK_SIZE = 1024 * 1024


def download_chunk(file):
    with open(file, 'rb')as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return
            yield hwsc_file_transaction_svc_pb2.chunk(buffer=chunk)


def save_chunks_to_file(chunks, filename):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)


class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
    def __init__(self):

        class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
            def __init__(self):
                pass


            def get_status(self, request, context):
                print("Get Status")

            def download_zip_files(self, request_iterator, context):
                if request_iterator.name:
                    return download_chunk(self.tmp_file_name)

          #  def UploadFile(self, request_iterator, context):
           #     print("[INFO] Requesting UploadFile service")
                # save_chunks_to_file(request_iterator, context.fileName)
                # print(request_iterator.Chunk.fileName)
            #    print(context.Chunk.fileName)
             #   return hwsc_file_transaction_svc_pb2.FileTransactionResponse()
                # if not request_iterator.buffer.is_valid or request_iterator.fileName.is_valid:
                #     message = 'Upload Error!'
                #     context.set_details(message)
                #     context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                #     return hwsc_file_transaction_svc_pb2.FileTransactionResponse()
                #
                # status = hwsc_file_transaction_svc_pb2.FileTransactionResponse()
                # status.code = grpc.StatusCode.OK
                # assert status.HasField("code")
                #
                # return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                #     message='OK',
                #     status=status.code,
                #     url='url: /res' + context.fileName,
                #     length=64)

            def upload_file(self, request_iterator, context):
                print("[INFO] Requesting UploadFile service")

                for getName in request_iterator:
                    save_chunks_to_file(request_iterator, getName.fileName)

                return hwsc_file_transaction_svc_pb2.FileTransactionResponse(message='OK')


            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

        hwsc_file_transaction_svc_pb2_grpc.add_FileTransactionServiceServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()
        print("Server is running...")

        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.server.stop(0)
