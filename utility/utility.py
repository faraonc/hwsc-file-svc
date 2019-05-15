import io
import re
import time
import hwsc_file_transaction_svc_pb2

CHUNK_SIZE = 1024 * 1024


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


def verify_uuid(id):
    """Verify uuid and checks it matches correct format."""
    uuid_regex = re.compile(r'^[a-zA-Z0-9]{26}$')
    if uuid_regex.match(id):
        return True
    else:
        return False


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


def is_expired(timestamp):
    """Determine if a given timestamp has expired"""
    return timestamp <= 0 or time.time() >= timestamp
