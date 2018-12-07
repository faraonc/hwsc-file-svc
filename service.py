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

                 for get_Name in request_iterator:
                     get_Url = utility.upload_file_to_azure(request_iterator, get_Name.fileName)

                 status = hwsc_file_transaction_svc_pb2.FileTransactionResponse()
                 for status in request_iterator:
                     status.code = grpc.StatusCode.OK

                 get_Message = grpc.StatusCode.OK.name

                 return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                     code=status.code,
                     message=get_Message,
                     url=get_Url
                 )

             #TODO
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
