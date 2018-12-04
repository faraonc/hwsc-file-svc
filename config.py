import os

CONFIG = {
    'address': os.environ.get('hosts_grpc_address'),
    'port': os.environ.get('hosts_grpc_port'),
    'hosts_grpc_network': os.environ.get('hosts_grpc_network'),
    'storage': os.environ.get('hosts_azure_storage'),
    'storage_key': os.environ.get('hosts_azure_key')
}