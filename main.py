# import config
# from service import server
from auth import jwt


if __name__ == '__main__':
    # server.Server().serve(config.CONFIG['port'])
    jwt.test()
