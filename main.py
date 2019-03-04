import config
from service import server

if __name__ == '__main__':
    server.Server().serve(config.CONFIG['port'])
