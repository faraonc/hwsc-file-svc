import pytest
import utility

def test_get_file_type():
    assert utility.get_file_type("cat.jpg") == "images"
    assert utility.get_file_type("cat.jpeg") == "images"
    assert utility.get_file_type("cat.png") == "images"
    assert utility.get_file_type("cat.bmp") == "images"
    assert utility.get_file_type("cat.tif") == "images"
    assert utility.get_file_type("cat.gif") == "images"
    assert utility.get_file_type("cat.tiff") == "images"

    assert utility.get_file_type("cat.wav") == "audios"
    assert utility.get_file_type("cat.wma") == "audios"
    assert utility.get_file_type("cat.ogg") == "audios"
    assert utility.get_file_type("cat.m4a") == "audios"
    assert utility.get_file_type("cat.mp3") == "audios"

    assert utility.get_file_type("cat.flv") == "videos"
    assert utility.get_file_type("cat.wmv") == "videos"
    assert utility.get_file_type("cat.mov") == "videos"
    assert utility.get_file_type("cat.avi") == "videos"
    assert utility.get_file_type("cat.mp4") == "videos"

    assert utility.get_file_type("cat.dat") == "files"
    assert utility.get_file_type("cat.xml") == "files"
    assert utility.get_file_type("cat.csv") == "files"
    assert utility.get_file_type("cat.py") == "files"
    assert utility.get_file_type("cat.html") == "files"

def test_create_uuid_container_in_azure():
     assert utility.create_uuid_container_in_azure(0, "1234abcd5454efef8842ll3fsc") == True
     assert utility.create_uuid_container_in_azure(4, "1234abcd5454efef8842ll3fsc") == False
     assert utility.create_uuid_container_in_azure(-4, "1234abcd5454efef8842ll3fsc") == False

def test_verify_uuid():
    # testing with correct uuid
    assert utility.verify_uuid("1234abcd5454efef8842ll3fsc") == True

    # testing with shorter length uuid
    assert utility.verify_uuid("1234abcd5454efef8842ll3fs") == False

    # testing with longer length uuid
    assert utility.verify_uuid("1234abcd5454efef8842llaaaab") == False

    # testing with special case in uuid
    assert utility.verify_uuid("1234abcd5454efef8842ll3!ss") == False