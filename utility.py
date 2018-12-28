from concurrent import futures
from azure.storage.blob import BlockBlobService, PublicAccess
import os,uuid,sys
import io
import grpc
import time
import os.path
import re
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

def create_uuid_container_in_azure(request):
    #print(request.uuid)
    uuid = request.uuid[2:]

    # regular expression that check valid uuid
    prog = re.compile(r'^[a-zA-Z0-9]{26}$')
    uuid_regex = prog.match(uuid)
    #print(uuid)

    if uuid_regex:
        block_blob_service = BlockBlobService(account_name=config.CONFIG["storage"],
                                              account_key=config.CONFIG["storage_key"])

        list = block_blob_service.list_containers(request.uuid)
        count = 0
        for c in list:
            count = count + 1

        images_container = request.uuid + "-images"
        audios_container = request.uuid + "-audios"
        files_container = request.uuid + "-files"
        videos_container = request.uuid + "-videos"

        # Checking whether the blobs that associated with uuid exists
        if count == 0:
            block_blob_service.create_container(images_container)
            block_blob_service.create_container(audios_container)
            block_blob_service.create_container(files_container)
            block_blob_service.create_container(videos_container)
            print("Successfully creates folders.")
            return True

        else:
            raise ValueError('\n[ERROR]The user folder already exists.')

    else:
        raise ValueError('\n[ERROR]The user id is not in valid format.')

def upload_file_to_azure(request_iterator, file_name):
    try:
        # First get the uuid and check whether it meets the requirement
        uuid = ''
        for id in request_iterator:
            if len(id.uuid) > 1:
                uuid = id.uuid
            else:
                pass

        uuid = uuid[2:]
        # regular expression that check valid uuid
        prog = re.compile(r'^[a-zA-Z0-9]{26}$')
        uuid_regex = prog.match(uuid)

        if uuid_regex:
            # Create the BlockBlockService that is used to call the Blob service for the storage account
            block_blob_service = BlockBlobService(account_name=config.CONFIG["storage"],
                                                  account_key=config.CONFIG["storage_key"])

            uuid = 'u-' + uuid
            # Returns the list of blobs attached to the uuid
            list = block_blob_service.list_containers(uuid)
            count = 0
            for c in list:
                count = count + 1

            # Checking whether the blobs that associated with uuid exists
            if count == 0:
                raise ValueError('\n[ERROR]There is no folder associated with the ' + uuid)

            else:
                container_type = get_file_type(file_name)
                container_name = uuid + '-' + container_type

                # Set the permission so the blobs are public.
                block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

                stream = io.BytesIO()

                for chunk in request_iterator:
                    stream.write(chunk.buffer)

                stream.seek(0)

                if block_blob_service.exists(container_name):
                    block_blob_service.create_blob_from_stream(container_name, file_name, stream)
                    print("\n[DEBUG]Uploading to folder with the file name:", file_name)

                    url_upload = block_blob_service.make_blob_url(container_name, file_name)
                    print(url_upload)
                    return url_upload

                else:
                    raise ValueError('\n[ERROR]The folder does not exist.')
        else:
            raise ValueError('\n[ERROR]The user id is not in valid format.')

    #TODO
    except Exception:
        raise ValueError('\n[ERROR]The folder does not exist.')