import pytest
import re
import sys
from logger import logger


@pytest.mark.parametrize("input, expected_output, desc",
                         [
                             ("", "[INFO] Requesting  service\n", "test with no input"),
                             (" ", "[INFO] Requesting   service\n", "test with a space"),
                             ("TestService", "[INFO] Requesting TestService service\n", "test with TestService"),
                             ("1", "[INFO] Requesting 1 service\n", "test with 1")
                         ]
                         )
def test_request_service(capsys, input, expected_output, desc):
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    logger.request_service(input)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc


@pytest.mark.parametrize("input, input2, expected_output, desc",
                         [
                             ("", "", "[DEBUG]  \n", "test with no input"),
                             (" ", "", "[DEBUG]   \n", "test with a space and no input"),
                             ("test", "", "[DEBUG] test \n", "test with test and no input"),
                             ("test", "text", "[DEBUG] test text\n", "test with test and text"),
                             ("", "2", "[DEBUG]  2\n", "test with no input and 2")
                         ]
                         )
def test_debug(capsys, input, input2, expected_output, desc):
    logger.debug(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc


@pytest.mark.parametrize("input, input2, expected_output, desc",
                         [
                             ("", "", "[INFO]  \n", "test with no input"),
                             (" ", "", "[INFO]   \n", "test with a space and no input"),
                             ("test", "", "[INFO] test \n", "test with test and no input"),
                             ("test", "text", "[INFO] test text\n", "test with test and text"),
                             ("", "2", "[INFO]  2\n", "test with no input and 2")
                         ]
                         )
def test_info(capsys, input, input2, expected_output, desc):
    logger.info(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc


@pytest.mark.parametrize("input, input2, expected_output, desc",
                         [
                             ("", "", "[ERROR]  \n", "test with no input"),
                             (" ", "", "[ERROR]   \n", "test with a space and no input"),
                             ("test", "", "[ERROR] test \n", "test with test and no input"),
                             ("test", "text", "[ERROR] test text\n", "test with test and text"),
                             ("", "2", "[ERROR]  2\n", "test with no input and 2")
                         ]
                         )
def test_error(capsys, input, input2, expected_output, desc):
    logger.error(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc


@pytest.mark.parametrize("input, input2, expected_output, desc",
                         [
                             ("", "", "[ERROR]  \n", "test with no input"),
                             (" ", "", "[ERROR]   \n", "test with a space and no input"),
                             ("test", "", "[ERROR] test \n", "test with test and no input"),
                             ("test", "text", "[ERROR] test text\n", "test with test and text"),
                             ("", "2", "[ERROR]  2\n", "test with no input and 2")
                         ]
                         )
def test_exception(capsys, input, input2, expected_output, desc):
    logger.exception(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc


@pytest.mark.parametrize("input, input2, expected_output, desc",
                         [
                             ("", "", "[FATAL]  \n", "test with no input"),
                             (" ", "", "[FATAL]   \n", "test with a space and no input"),
                             ("test", "", "[FATAL] test \n", "test with test and no input"),
                             ("test", "text", "[FATAL] test text\n", "test with test and text"),
                             ("", "2", "[FATAL]  2\n", "test with no input and 2")
                         ]
                         )
def test_fatal(capsys, input, input2, expected_output, desc):
    logger.fatal(input, input2)
    sys.stderr.write(logger.log_stream.getvalue())
    captured = capsys.readouterr()
    logger.log_stream.truncate(0)
    logger.log_stream.seek(0)
    assert re.match(r"\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + re.escape(expected_output), captured.err), desc
