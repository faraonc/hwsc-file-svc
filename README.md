# hwsc-file-transaction-svc
# TO-DO How to Run
This provides instruction for how to run the file transaction service:

# Dependency
This provides instruction for how to manage dependency using pipenv.
Pipenv is a dependency manager for python projects.

Prerequisites:
Python3 or greater

First time creating the Pipfile and Pipfile.lock:

1. Install pipenv. You type 'pip install --user pipenv' on the command.

2. cd [your project]

3. Do 'pipenv install grpcio-tools'

4. Do 'pipenv install googleapis-common-protos'

5. Under your current project directory, it will create Pipfile and Pipfile.lock

After your project has Pipfile and Pipfile.lock:

1. you can simply do'pipenv install' to manage dependency.

# Purpose
This provides service for file management that includes the following:
- Downloading
- Uploading
- Deleting

# Specifications
## Download
### GET
### /api/file-management/file?loc={}

## Upload
### POST
### /api/file-management/file?name={}&type={}

## Delete
### DELETE
### /api/file-management/file?loc={}
