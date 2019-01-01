import pytest
import utility

# testing with already existing uuid
def test_valid_uuid():
    with pytest.raises(Exception) as e_info:
        utility.create_uuid_container_in_azure("1234abcd5454efef8842ll3fsc")

# testing with shorter length uuid
def test_valid_uuid1():
    with pytest.raises(Exception) as e_info:
        utility.create_uuid_container_in_azure("1234abcd5454efef8842ll3fs")

# testing with special case in uuid
def test_valid_uuid2():
    with pytest.raises(Exception) as e_info:
        utility.create_uuid_container_in_azure("1234abcd5454efef8842ll3!ss")

# should be not passed. but how?
def test_valid_uuid4():
    with pytest.raises(Exception) as e_info:
        utility.create_uuid_container_in_azure("1234abcd5454efef8842llaaaa")