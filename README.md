# hwsc-file-transaction-svc
This manages HWSC user file transactions

### Purpose
This provides file management service which includes the following:
- DownloadFile()
- UploadFile()
- DeleteFile()

## Prerequisites
- Python 3.7 or greater
- pip
- pipenv
- Pycharm or VSCode

## Check your python version
- Open your terminal and type `$ python --version`

## How to install Python3.7 with Homebrew
- On your terminal, type `$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` 
- Open `~./profile]` 
- Insert `export PATH=/usr/local/bin:/usr/local/sbin:$PATH` in the `~./profile`
- On your terminal, type `$ brew install python` to install python 
- Type `$ python3 --version` to check the version is 3.7
- Call python3.7 by `$ python3`

## How to install pipenv with Homebrew
- If you installed python3.7 with Homebrew, you would have pip installed already
- On the terminal, type `$ pip install --user pipenv` 

## How to manage dependency with pipenv (to create Pipfile and Pipfile.lock)
- Change to your project directory by typing `$ cd [project name]` 
- To spawn a shell in a virtual environment, type `$ pipenv shell`
- In the shell, run the bash script by typing `$ ./generate.sh`. This will create Pipfile and Pipfile.lock files that are used for dependency management
- `Pipfile`: track which dependencies your project needs in case you need to reinstall them
- `Pipfile.lock`: enables deterministic builds by specifying the exact requirements for reproducing an environment

## Pull the proto file and compiled pb from the hwsc-api-blocks
- TODO

# Before running service
- `$ pip install pytest --dev` (Unit test for the application)
- `$ pipenv install -dev` (Put dependency in `dev-packages` in `Pipfile`)
- `$ pipenv install -env` (Update `Pipfile.lock`)
- `$ pipenv lock` (Lock the environment to ensure the same dependency for production)

# How to run service
- On the command, type `$ pipenv install --ignore-pipfile`. This ignores the Pipfile for installation and use what's in the Pipfile.lock
- Type `$ pipenv run python nameofthefile.py`. Example: `$ pipenv run python main.py`

