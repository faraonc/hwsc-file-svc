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
    IMAGES = "images"
    AUDIOS = "audios"
    VIDEOS = "videos"

    image_exts_dict = {"jpg":IMAGES, "jpeg":IMAGES, "png":IMAGES, "bmp":IMAGES, "tif":IMAGES, "gif":IMAGES, "tiff":IMAGES}
    audio_exts_dict = {"wav":AUDIOS, "wma":AUDIOS, "ogg":AUDIOS, "m4a":AUDIOS, "mp3":AUDIOS}
    video_exts_dict = {"flv":VIDEOS, "wmv":VIDEOS, "mov":VIDEOS, "avi":VIDEOS, "mp4":VIDEOS}

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

def upload_file_to_azure(chunks, file_name):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name=config.CONFIG["storage"], account_key=config.CONFIG["storage_key"])

        # Create a container.
        container_name = get_file_type(file_name)
        block_blob_service.create_container(container_name);

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        stream = io.BytesIO()

        for chunk in chunks:
            stream.write(chunk.buffer)

        stream.seek(0)
        block_blob_service.create_blob_from_stream(container_name, file_name, stream)

        print("\n[DEBUG]Uploading to Blob storage the file name:", file_name)

        url_upload = block_blob_service.make_blob_url(container_name, file_name)
        print(url_upload)
        return url_upload

    #TODO
    except Exception as NoSuchBlobException:
        print(NoSuchBlobException)