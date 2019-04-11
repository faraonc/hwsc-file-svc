import os

CONFIG = {
    "address": os.environ.get("hosts_file_address"),
    "port": os.environ.get("hosts_file_port"),
    "hosts_grpc_network": os.environ.get("hosts_file_network"),
    "storage": os.environ.get("hosts_azure_storage"),
    "storage_key": os.environ.get("hosts_azure_key"),
    "blob_storage": os.environ.get("hosts_blob_storage")
}