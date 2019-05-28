import config
from azure.storage.blob import BlockBlobService, PublicAccess
from utility import utility
from logger import logger

block_blob_service = BlockBlobService(connection_string=config.CONFIG["blob_storage"])


def upload_file_to_azure(stream, has_folder, uuid, file_name):
    """Upload file to azure blob storage."""
    # TODO
    # ADD try-catch block

    # Checking whether the blobs that associated with uuid exists
    if has_folder:
        container_type = utility.get_file_type(file_name)
        container_name = uuid + "-" + container_type

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # stream = io.BytesIO()
        # for chunk in buffer:
        #    stream.write(chunk.buffer)

        stream.seek(0)

        block_blob_service.create_blob_from_stream(container_name, file_name, stream)
        logger.debug("uploading to folder with the file name:", file_name)

        url_upload = block_blob_service.make_blob_url(container_name, file_name)
        print(url_upload)
        return url_upload

    else:
        return ""


def create_uuid_container_in_azure(uuid):
    """Create uuid folder in the azure blob storage."""
    # TODO
    # ADD try-catch block
    if utility.verify_uuid(uuid):
        images_container = uuid + "-images"
        audios_container = uuid + "-audios"
        files_container = uuid + "-files"
        videos_container = uuid + "-videos"

        block_blob_service.create_container(images_container)
        block_blob_service.create_container(audios_container)
        block_blob_service.create_container(files_container)
        block_blob_service.create_container(videos_container)
        logger.debug("user folder creation successful")


def find_folder_in_azure(uuid, f_name):
    """Find folder in the azure blob storage."""
    container_name = uuid + "-" + f_name
    return block_blob_service.exists(container_name)


def user_folders_exist_in_azure(uuid):
    """Count folders in azure blob storage."""
    list_generator = block_blob_service.list_containers(uuid)
    return len(list(list_generator)) != 0
