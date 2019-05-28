import pytest
from azure_client import azure_client
import random
import string

valid_uuid_1 = "".join(random.choices(string.ascii_lowercase + string.digits, k=26))


@pytest.mark.parametrize("input_uuid, expected_output",
                         [
                             # testing with valid uuid
                             (valid_uuid_1, True),
                             # testing with duplicate uuid
                             (valid_uuid_1, True),
                             # testing with invalid uuid
                             ("1234abcd5454efef8842llaaaab", False),
                         ]
                         )
def test_create_uuid_container_in_azure(input_uuid, expected_output):
    azure_client.create_uuid_container_in_azure(input_uuid)
    actual_output = azure_client.user_folders_exist_in_azure(input_uuid)
    assert actual_output == expected_output


@pytest.mark.parametrize("input_uuid, input_filename, expected_output",
                         [
                             # testing with valid uuid
                             (valid_uuid_1, "audios", True),
                             # testing with valid uuid and invalid filename
                             (valid_uuid_1, "test", False),
                             # testing with invalid uuid
                             ("1234abcd5454efef8842llaaaab", "audios", False),
                         ]
                         )
def test_find_folder_in_azure(input_uuid, input_filename, expected_output):
    assert azure_client.find_folder_in_azure(input_uuid, input_filename) == expected_output


@pytest.mark.parametrize("input_uuid, expected_output",
                         [
                             # testing with valid uuid
                             (valid_uuid_1, True),
                             # testing with invalid uuid
                             ("1234abcd5454efef8842llaaaab", False),
                         ]
                         )
def test_user_folders_exist_in_azure(input_uuid, expected_output):
    assert azure_client.user_folders_exist_in_azure(input_uuid) == expected_output
