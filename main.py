import config
import server

if __name__ == '__main__':
    server.Server().serve(config.CONFIG['port'])
