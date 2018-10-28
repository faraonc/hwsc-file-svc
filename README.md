# HWSC-File-Transaction-SVC
This is one of the microservices in the Humpback Whale Social Call project, which allows user to manage their files. 

### Purpose
This provides file management service which includes the following:
- Downloading
- Uploading
- Deleting

## Prerequisites
- Python 3.7 or greater
- pip
- pipenv
- Webstorm

## Check your python version
- On your terminal, type [python --version] to check the python version

## How to install Python3.7 with Homebrew
- If you don't have python version 3.7, you can install it with Homebrew
- On your terminal, type [ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"] to install Homebrew
- Insert Homebrew directory into your path by typing [sublime ~./profile]. sublime can be substituted with your favorite text editor
- On the opening text file, insert [export PATH=/usr/local/bin:/usr/local/sbin:$PATH] as a path
- Type [brew install python] on the command to install python 
- Type [python3 --version] to check the version is 3.7
- Whenever you work with python3.7, you need to call it by [python3]

## How to install pipenv with Homebrew
- If you installed python3.7 with Homebrew, you would have pip installed already
- Use pip to install pipenv by typing [pip install --user pipenv] as a command

## How to manage dependency with pipenv (to create Pipfile and Pipfile.lock)
- Spawn a shell in a virtual environment by typing [pipenv shell]
- If you are not already in the project directory, change into your projects directory by doing cd [project directory]
- In created shell, you run the bash script by typing [./generate.sh]
- This will create Pipfile and Pipfile.lock files that are used for dependency management
- Pipfile: track which dependencies your project needs in case you need to reinstall them
- Pipfile.lock: enables deterministic builds by specifying the exact requirements for reproducing an environment

## How to manage dependency with pipenv (project already contains generated Pipfile and Pipfile.lock)
- Type [pipenv install] on the command
- This does installation that from Pipfile.lock

## Pull the proto file and compiled pb from the hwsc-api-blocks
- Working on it

## Additional useful commands
- pip install pytest --dev (Unit test for the application)
- pipenv install -dev (Put dependency in [dev-packages])
- pipenv install -env (Update Pipfile.lock)
- pipenv lock (lock the environment so ensures the same dependency in production)
- pipenv install --ignore-pipfile (Ignore the Pipfile for installation and use what's in the Pipfile.lock. This might be useful after you lock for the production, install the last successful environment)

# How to run service

- Type [pipenv run python nameofthefile.py]. This running ensures that your installed packages are available. Also, 
it ensures that all the commands that can use installed packages. 
- Example: [pipenv run python main.py]


- Create a contract with API
- Develop a new service for hwsc-file-transaction-svc (e.g., Download, Upload, Delete)
- TO-DO

### 1. Upload
The path for uploading a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The uploaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The uploaded request will be sent to the file service
- The file service received connection
- The file will be sent to the file service
- The file service uploads the file to the Blob Storage
- The Blob Storage returns an url link to the file service
- The file service returns the url link to the gateway service
- The gateway service requests the metadata-file service to create a file
- The metadata-file service sends the file to MongoDB for storaging
- The MongoDB returns update to the meta-data service
- The meta-data service returns update to the gateway service.
- The file has been successfully uploaded 
### 2. Download
The path for downloading a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The downloaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The downloaded request will be sent to the file service
- The file service received connection
- TO-DO
### 3. Delete
The path for deleting a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The downloaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The deleting request will be sent to the file service
- The file service received connection
- TO-DO
