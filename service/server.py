import grpc
import hwsc_file_transaction_svc_pb2_grpc
from concurrent import futures
from enum import Enum
from service.file_transaction_service import FileTransactionService
from logger import logger
from readerwriterlock import rwlock


class State(Enum):
    """A current state class of file transaction service"""
    AVAILABLE = 0
    UNAVAILABLE = 1


class StateLocker:
    """Synchronizes the state of file_transaction_svc"""
    __lock = rwlock.RWLockWrite()
    __current_service_state = None

    def get_lock(self):
        return self.__lock

    def get_current_service_state(self):
        return self.__current_service_state

    def set_current_service_state(self, new_state):
        self.__current_service_state = new_state


class Server:

    def __init__(self):
        self.__state_locker = StateLocker()
        self.set_state(State.AVAILABLE)
        self.__uuid_locker = {}

    # TODO test
    def get_state_locker(self):
        return self.__state_locker

    # TODO test
    def set_state(self, new_state):
        self.__state_locker.set_current_service_state(new_state)

    def get_uuid_locker(self):
        return self.__uuid_locker

    # TODO test
    def serve(self, port):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        hwsc_file_transaction_svc_pb2_grpc.add_FileTransactionServiceServicer_to_server(FileTransactionService(self),
                                                                                        server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        logger.info("hwsc-file-transaction-svc initializing...")
        logger.info("hwsc-file-transaction started at:", port)
        try:
            while True:
                pass
        except KeyboardInterrupt:
            server.stop(0)
