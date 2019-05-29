import pytest
from azure_client import azure_client
import random
import string

valid_uuid_1 = "".join(random.choices(string.ascii_lowercase + string.digits, k=26))
invalid_uuid_1 = "1234abcd5454efef8842llaaaab"


@pytest.mark.parametrize("input_uuid, expected_output, desc",
                         [
                             (valid_uuid_1, True, "testing with valid uuid"),
                             (valid_uuid_1, True, "testing with duplicate uuid"),
                             (invalid_uuid_1, False, "testing with invalid uuid"),
                         ]
                         )
def test_create_uuid_container_in_azure(input_uuid, expected_output, desc):
    azure_client.create_uuid_container_in_azure(input_uuid)
    actual_output = azure_client.user_folders_exist_in_azure(input_uuid)
    assert actual_output == expected_output, desc


@pytest.mark.parametrize("input_uuid, input_filename, expected_output, desc",
                         [
                             (valid_uuid_1, "audios", True, "testing with valid uuid"),
                             (valid_uuid_1, "test", False, "testing with valid uuid and invalid filename"),
                             (invalid_uuid_1, "audios", False, "testing with invalid uuid"),
                         ]
                         )
def test_find_folder_in_azure(input_uuid, input_filename, expected_output, desc):
    assert azure_client.find_folder_in_azure(input_uuid, input_filename) == expected_output, desc


@pytest.mark.parametrize("input_uuid, expected_output, desc",
                         [
                             (valid_uuid_1, True, "testing with valid uuid"),
                             (invalid_uuid_1, False, "testing with invalid uuid"),
                         ]
                         )
def test_user_folders_exist_in_azure(input_uuid, expected_output, desc):
    assert azure_client.user_folders_exist_in_azure(input_uuid) == expected_output, desc
