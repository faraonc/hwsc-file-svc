from azure.storage.blob import BlockBlobService, PublicAccess
import io
import re
import config
import hwsc_file_transaction_svc_pb2

CHUNK_SIZE = 1024 * 1024
block_blob_service = BlockBlobService(account_name=config.CONFIG["storage"],
                                      account_key=config.CONFIG["storage_key"])


def download_chunk(file):
    """Download a file in chunks."""
    with open(file, "rb")as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return
            yield hwsc_file_transaction_svc_pb2.chunk(buffer=chunk)


def get_file_type(file_name):
    """Check and return correct type of the file passed in."""
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


def upload_file_to_azure(stream, has_folder, uuid, file_name):
    """Upload file to azure blob storage."""
    # TODO
    # ADD try-catch block

    # Checking whether the blobs that associated with uuid exists
    if has_folder:
        container_type = get_file_type(file_name)
        container_name = uuid + '-' + container_type

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # stream = io.BytesIO()
        # for chunk in buffer:
        #    stream.write(chunk.buffer)

        stream.seek(0)

        block_blob_service.create_blob_from_stream(container_name, file_name, stream)
        print("[DEBUG]Uploading to folder with the file name:", file_name)

        url_upload = block_blob_service.make_blob_url(container_name, file_name)
        print(url_upload)
        return url_upload

    else:
        return ""


def create_uuid_container_in_azure(count, uuid):
    """Create uuid folder in the azure blob storage."""
    # TODO
    # ADD try-catch block
    if count == 0:
        images_container = uuid + "-images"
        audios_container = uuid + "-audios"
        files_container = uuid + "-files"
        videos_container = uuid + "-videos"

        block_blob_service.create_container(images_container)
        block_blob_service.create_container(audios_container)
        block_blob_service.create_container(files_container)
        block_blob_service.create_container(videos_container)
        print("[Utility]Successful to create folders.")
        return True

    else:
        print("[Utility]Successful to create folders.")
        return False


def verify_uuid(id):
    """Verify uuid and checks it matches correct format."""
    uuid_regex = re.compile(r'^[a-zA-Z0-9]{26}$')

    if uuid_regex.match(id):
        return True
    else:
        return False


def find_folder(uuid, f_name):
    """Find folder in the azure blob storage."""
    container_name = uuid + '-' + f_name

    if block_blob_service.exists(container_name):
        return True
    else:
        return False


def count_folders(uuid):
    """Count folders in azure blob storage."""
    list_generator = block_blob_service.list_containers(uuid)

    folder_count = 0
    for c in list_generator:
        folder_count = folder_count + 1

    return folder_count


def get_property(request_iterator):
    """Store and return properties of filename, uuid, and buffer."""
    stream = io.BytesIO()
    d = dict()

    for property in request_iterator:
        if len(property.uuid) > 1:
            d["uuid"] = property.uuid
        if len(property.file_name) > 1:
            d["f_name"] = property.file_name
        if len(property.buffer) > 1:
            stream.write(property.buffer)
        else:
            pass

        d["stream"] = stream
    return d
