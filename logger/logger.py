import logging
from io import StringIO
from logger.consts import errors


logging.addLevelName(50, "FATAL")
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%y/%m/%d %H:%M:%S")

# Set up StringIO handler for unit test
root = logging.getLogger()
root.setLevel(logging.DEBUG)
log_stream = StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%y/%m/%d %H:%M:%S"))
root.addHandler(handler)


def request_service(service):
    logging.info("Requesting %s service", service)


def debug(*args):
    logging.debug(" ".join(args))


def info(*args):
    logging.info(" ".join(args))


def error(*args):
    logging.error(" ".join(args))


def exception(*args):
    """Will print with [ERROR] level and include stack trace"""
    logging.exception(" ".join(args))


def fatal(*args):
    logging.fatal(" ".join(args))

