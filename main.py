import service
import config

if __name__ == '__main__':
    service.FileTransactionService().start(config.CONFIG['port'])
