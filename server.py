import grpc
import hwsc_file_transaction_svc_pb2_grpc
from concurrent import futures
from enum import Enum
from file_transaction_service import FileTransactionService


class State(Enum):
    """A current state class of file transaction service"""
    AVAILABLE = 0
    UNAVAILABLE = 1


class Server:

    def __init__(self):
        self.__state = State.AVAILABLE

    # TODO test
    def get_state(self):
        return self.__state

    # TODO test
    def set_state(self, new_state):
        self.__state = new_state

    # TODO test
    def serve(self, port):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        hwsc_file_transaction_svc_pb2_grpc.add_FileTransactionServiceServicer_to_server(FileTransactionService(self),
                                                                                        server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        print("[INFO] hwsc-file-transaction-svc initializing...")
        print("[INFO] hwsc-file-transaction started at:", port)
        try:
            while True:
                pass
        except KeyboardInterrupt:
            server.stop(0)
