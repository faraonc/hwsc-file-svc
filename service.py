from concurrent import futures
import grpc
import time
import utility
import io
import hwsc_file_transaction_svc_pb2
import hwsc_file_transaction_svc_pb2_grpc

class FileTransactionService(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
     """A FileTransactionService class contains servicer and corresponding functionalites."""
     def __init__(self):

         class Servicer(hwsc_file_transaction_svc_pb2_grpc.FileTransactionServiceServicer):
             """A servicer class contains functionalities for file service."""
             def __init__(self):
                 pass

             #TODO
             def GetStatus(self, request, context):
                 """Get and return status to the user."""
                 print("Get Status")

             #TODO
             def DownloadZippedFiles(self, request_iterator, context):
                 """Download zipped files from azrue blob storage."""
                 if request_iterator.name:
                     return utility.download_chunk(self.tmp_file_name)

             def UploadFile(self, request_iterator, context):
                 """Upload a file to the azure blob storage."""
                 print("[INFO] Requesting UploadFile service")
                 #TODO
                 #May implement try-catch block

                 d = utility.get_property(request_iterator)

                 type = utility.get_file_type(d["f_name"])
                 is_uuid_valid = utility.verify_uuid(d["uuid"])

                 if is_uuid_valid:
                     has_folder = utility.find_folder(d["uuid"], type)
                     get_url = utility.upload_file_to_azure(d["stream"], has_folder, d["uuid"], d["f_name"])

                     #TODO
                     #write a function to validate the url, like a regex check
                     if get_url != "":
                        return hwsc_file_transaction_svc_pb2.FileTransactionResponse(
                            code=grpc.StatusCode.OK.value[0],
                            message="success uploadfile",
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
                """Create user folder in the azure blob storage."""
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