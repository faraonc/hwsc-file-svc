from concurrent import futures
import grpc
import time
import utility
import hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc

class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
     def __init__(self):

         class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
             def __init__(self):
                 pass

             def GetStatus(self, request, context):
                 print("Get Status")

             def DownloadZippedFiles(self, request_iterator, context):
                 if request_iterator.name:
                     return utility.download_chunk(self.tmp_file_name)

             def UploadFile(self, request_iterator, context):
                 print("[INFO] Requesting UploadFile service")
                 get_url=''
                 for get_name in request_iterator:
                     get_url = utility.upload_file_to_azure(request_iterator, get_name.file_name)

                 status = hwsc_file_transaction_svc_pb2.FileTransactionResponse()
                 for status in request_iterator:
                     status.code = grpc.StatusCode.OK

                 get_message = grpc.StatusCode.OK.name

                 if get_url != '':
                     return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                     code=status.code,
                     message=get_message,
                     url=get_url
                 )

                 else:
                     return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                     code=grpc.StatusCode.ABORTED,
                     message=grpc.StatusCode.ABORTED.name,
                     url=get_url
                 )


             def CreateUserFolder(self, request, context):
                print("[INFO] Requesting CreateUuidFolder service")

                created = utility.create_uuid_container_in_azure(request)

                if created:
                    return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                        code=grpc.StatusCode.OK,
                        message=grpc.StatusCode.OK.name
                    )
                else:
                    return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                        code=grpc.StatusCode.ABORTED,
                        message=grpc.StatusCode.ABORTED.name
                    )
             #TODO
             self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

         hwsc_file_transaction_svc_pb2_grpc.add_FileTransactionServiceServicer_to_server(Servicer(), self.server)

     def start(self, port):
         self.server.add_insecure_port(f'[::]:{port}')
         self.server.start()
         print("[INFO] hwsc-file-transaction-svc initializing...")

         try:
           while True:
                pass
         except KeyboardInterrupt:
                  self.server.stop(0)
