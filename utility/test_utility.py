import pytest
from utility import utility


@pytest.mark.parametrize("input, expected_output",
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
def test_get_file_type(input, expected_output):
    actual_output = utility.get_file_type(input)
    assert actual_output == expected_output


# @pytest.mark.parametrize("input1, input2, expected_output",
#                          [
#                              (0, "1234abcd5454efef8842ll3fsc", True),
#                              (4, "1234abcd5454efef8842ll3fsc", False),
#                              (-4, "1234abcd5454efef8842ll3fsc", False)
#                          ]
#                          )
# def test_create_uuid_container_in_azure(input1, input2, expected_output):
#     actual_output = utility.create_uuid_container_in_azure(input1, input2)
#     assert actual_output == expected_output


@pytest.mark.parametrize("input, expected_output",
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
def test_verify_uuid(input, expected_output):
    actual_output = utility.verify_uuid(input)
    assert actual_output == expected_output
