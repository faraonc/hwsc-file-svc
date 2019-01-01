from concurrent import futures
import grpc
import time
import utility
import io
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
                 #TODO
                 #May implement try-catch block

                 d = utility.get_property(request_iterator)

                 count = utility.count_folders(d['uuid'])
                 is_uuid_valid = utility.verify_uuid(d['uuid'])

                 if is_uuid_valid:
                     get_url = utility.upload_file_to_azure(d['stream'], count, d['uuid'], d['f_name'])

                     #TODO
                     #write a function to validate the url, like a regex check
                     if get_url != "":
                        return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                            code=grpc.StatusCode.OK.value[0],
                            message='success uploadfile',
                            url=get_url
                        )

                     else:
                        return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                            code=grpc.StatusCode.UNKNOWN.value[0],
                            message='fail uploadfile',
                        )

                 else:
                     return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                         code=grpc.StatusCode.UNKNOWN.value[0],
                         message="invalid uuid"
                     )

             def CreateUserFolder(self, request, context):
                 #TODO
                 #May implement try-catch block
                print("[INFO] Requesting CreateUuidFolder service")

                is_uuid_valid = utility.verify_uuid(request.uuid)

                if is_uuid_valid:
                    count = utility.count_folders(request.uuid)
                    created = utility.create_uuid_container_in_azure(count, request.uuid)

                    if created:
                        return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                            code=grpc.StatusCode.OK.value[0],
                            message="success"
                        )
                    else:
                        return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                            code=grpc.StatusCode.UNKNOWN.value[0],
                            message="user folder already exist"
                        )
                else:
                    return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                        code=grpc.StatusCode.UNKNOWN.value[0],
                        message="invalid uuid"
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