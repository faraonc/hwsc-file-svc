from concurrent import futures
from azure.storage.blob import BlockBlobService, PublicAccess
import os, uuid,sys
import io
import grpc
import time
import os.path
import config
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

def get_file_type(file_name):
    image_exts_dict = {"jpg": True, "jpeg": True, "png": True, "bmp": True, "tif": True, "gif": True, "tiff": True}
    audio_exts_dict = {"wav": True, "wma": True, "ogg": True, "m4a": True, "mp3": True}
    video_exts_dict = {"flv": True, "wmv": True, "mov": True, "avi": True, "mp4": True}

    file_list = file_name.split('.')
    extension = file_list[-1]
    file_type = "files"

    if image_exts_dict.get(extension):
        file_type = "images"
    elif audio_exts_dict.get(extension):
        file_type = "audios"
    elif video_exts_dict.get(extension):
        file_type = "videos"

    return file_type

def upload_file_to_azure(request_iterator, file_name):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=config.CONFIG["storage"], account_key=config.CONFIG["storage_key"])

        # Create a container.
        container_name = get_file_type(file_name)
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        stream = io.BytesIO()

        for chunk in request_iterator:
            stream.write(chunk.buffer)

        stream.seek(0)

        if block_blob_service.exists(container_name):
            block_blob_service.create_blob_from_stream(container_name, file_name, stream)
            print("\n[DEBUG]Uploading to Blob storage the file name:", file_name)

            url_upload = block_blob_service.make_blob_url(container_name, file_name)
            print(url_upload)
            return url_upload
        else:
            print("\n[ERROR]The container does not exist.")
            return None

    #TODO
    except Exception as NoSuchBlobException:
        print(NoSuchBlobException)