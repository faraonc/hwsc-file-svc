import service.hwsc_file_transaction_svc as hwsc_file_transaction_svc

if __name__ == '__main__':
    hwsc_file_transaction_svc.FileTransactionService().start(50051)


#------------------------------------------------------
# This should be in a separate client.py file ???
import os
import service.hwsc_file_transaction_svc as hwsc_file_transaction_svc

if __name__ == '__main__':
    client = hwsc_file_transaction_svc.FileTransactionClient('localhost:50051')

    # download data
    download_request = ''
    if os.path.exists(download_request):
        os.remove(download_request)
    client.download('downLoad_data',download_request)

    # upload data
    upload_request = ''
    client.upload(upload_request)

    os.system(f' sha1sum{download_request}')
    os.system(f' sha1sum{upload_request}')
