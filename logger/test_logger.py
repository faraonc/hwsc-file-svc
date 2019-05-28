import pytest
import re
import sys
from logger import logger


@pytest.mark.parametrize("input, expected_output",
                         [
                             ("", "[INFO] Requesting  service\n"),
                             (" ", "[INFO] Requesting   service\n"),
                             ("TestService", "[INFO] Requesting TestService service\n"),
                             ("1", "[INFO] Requesting 1 service\n")
                         ]
                         )
def test_request_service(capsys, input, expected_output):
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    logger.request_service(input)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)


@pytest.mark.parametrize("input, input2, expected_output",
                         [
                             ("", "", "[DEBUG]  \n"),
                             (" ", "", "[DEBUG]   \n"),
                             ("test", "", "[DEBUG] test \n"),
                             ("test", "text", "[DEBUG] test text\n"),
                             ("", "2", "[DEBUG]  2\n")
                         ]
                         )
def test_debug(capsys, input, input2, expected_output):
    logger.debug(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)


@pytest.mark.parametrize("input, input2, expected_output",
                         [
                             ("", "", "[INFO]  \n"),
                             (" ", "", "[INFO]   \n"),
                             ("test", "", "[INFO] test \n"),
                             ("test", "text", "[INFO] test text\n"),
                             ("", "2", "[INFO]  2\n")
                         ]
                         )
def test_info(capsys, input, input2, expected_output):
    logger.info(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)


@pytest.mark.parametrize("input, input2, expected_output",
                         [
                             ("", "", "[ERROR]  \n"),
                             (" ", "", "[ERROR]   \n"),
                             ("test", "", "[ERROR] test \n"),
                             ("test", "text", "[ERROR] test text\n"),
                             ("", "2", "[ERROR]  2\n")
                         ]
                         )
def test_error(capsys, input, input2, expected_output):
    logger.error(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)


@pytest.mark.parametrize("input, input2, expected_output",
                         [
                             ("", "", "[ERROR]  \n"),
                             (" ", "", "[ERROR]   \n"),
                             ("test", "", "[ERROR] test \n"),
                             ("test", "text", "[ERROR] test text\n"),
                             ("", "2", "[ERROR]  2\n")
                         ]
                         )
def test_exception(capsys, input, input2, expected_output):
    logger.exception(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)


@pytest.mark.parametrize("input, input2, expected_output",
                         [
                             ("", "", "[FATAL]  \n"),
                             (" ", "", "[FATAL]   \n"),
                             ("test", "", "[FATAL] test \n"),
                             ("test", "text", "[FATAL] test text\n"),
                             ("", "2", "[FATAL]  2\n")
                         ]
                         )
def test_fatal(capsys, input, input2, expected_output):
    logger.fatal(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err)
