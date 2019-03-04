import service
import config

if __name__ == '__main__':
    service.Server().serve(config.CONFIG['port'])
