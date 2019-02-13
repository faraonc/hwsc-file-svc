import utility
import pytest


@pytest.mark.parametrize("input, output",
                         [
                             ("cat.jpg", "images"),
                             ("cat.jpeg", "images"),
                             ("cat.png", "images"),
                             ("cat.bmp", "images"),
                             ("cat.tif", "images"),
                             ("cat.gif", "images"),
                             ("cat.tiff", "images"),
                             ("cat_song.wav", "audios"),
                             ("cat_song.wma", "audios"),
                             ("cat_song.ogg", "audios"),
                             ("cat_song.m4a", "audios"),
                             ("cat_song.mp3", "audios"),
                             ("cat_jump.flv", "videos"),
                             ("cat_jump.wmv", "videos"),
                             ("cat_jump.mov", "videos"),
                             ("cat_jump.avi", "videos"),
                             ("cat_jump.mp4", "videos"),
                             ("cat.pdf", "files"),
                             ("cat.txt", "files"),
                             ("cat.html", "files"),
                             ("cat.doc", "files")
                         ]
                         )
def test_get_file_type(input, output):
    file_type = utility.get_file_type(input)
    assert file_type == output


@pytest.mark.parametrize("input1, input2, output",
                         [
                             (0, "1234abcd5454efef8842ll3fsc", True),
                             (4, "1234abcd5454efef8842ll3fsc", False),
                             (-4, "1234abcd5454efef8842ll3fsc", False)
                         ]
                         )
def test_create_uuid_container_in_azure(input1, input2, output):
    created = utility.create_uuid_container_in_azure(input1, input2)
    assert created == output


@pytest.mark.parametrize("input, output",
                         [
                             # testing with correct uuid
                             ("1234abcd5454efef8842ll3fsc", True),
                             # testing with shorter length uuid
                             ("1234abcd5454efef8842ll3fs", False),
                             # testing with longer length uuid
                             ("1234abcd5454efef8842llaaaab", False),
                             # testing with special case in uuid
                             ("1234abcd5454efef8842ll3!ss", False)
                         ]
                         )
def test_verify_uuid(input, output):
    verified = utility.verify_uuid(input)
    assert verified == output
