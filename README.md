# hwsc-file-transaction-svc
This manages HWSC user file transactions

### Purpose
This provides file management service which includes the following:
- GetStatus()
- DownloadZippedFiles()
- UploadFile()
- CreateUserFolder()

## Prerequisites
- Python 3.7 or greater
- pip
- pipenv
- Pycharm or VSCode

## Check your python version
- Open your terminal and type `$ python --version`

## How to install Python3.7 with Homebrew
- On your terminal, type 
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
- On your terminal, type `$ brew install python` to install python 
- Type `$ which python3` to figure out the path. Example: `/usr/local/Cellar/python/3.7.0/bin`
- Type `$ vim ~/.bash_profile` to open the `.bash_profile` file
- Insert `export PATH="/usr/local/Cellar/python/3.7.0/bin/:$PATH"` in the `.bash_profile` file
- Type `$ source ~/.bash_profile` to adjust the changes
- Type `$ python3 --version` to check the version is 3.7
- Call python3.7 by `$ python3`

## How to install pipenv with Homebrew
- If you installed python3.7 with Homebrew, you would have pip installed already
- On the terminal, type `$ pip install --user pipenv` 

## How to manage dependency of proto files
-Type `$./generate_dep.sh`. This will create copied proto files from the github urls.

## How to manage dependency with pipenv (to create Pipfile and Pipfile.lock)
- Change to your project directory by typing `$ cd [project name]` 
- To spawn a shell in a virtual environment, type `$ pipenv shell`
- In the shell, run the bash script by typing `$ ./generate.sh`. This will create Pipfile and Pipfile.lock files that are used for dependency management
- `Pipfile`: track which dependencies your project needs in case you need to reinstall them
- `Pipfile.lock`: enables deterministic builds by specifying the exact requirements for reproducing an environment

## Pull the proto file and compiled pb from the hwsc-api-blocks
- 

# Before running service
- `$ pip install pytest --dev` (Unit test for the application)
- `$ pipenv install -dev` (Put dependency in `dev-packages` in `Pipfile`)
- `$ pipenv install -env` (Update `Pipfile.lock`)
- `$ pipenv lock` (Lock the environment to ensure the same dependency for production)

# How to run service
- On the command, type `$ pipenv install`. This ignores the Pipfile for installation and use what's in the Pipfile.lock
- Type `$ pipenv run python3 main.py`. 

# How to test service
- Install `$pipenv install pytest` 
- Type `$py.test -v` for testing to see which cases are passed or failed

# How to report coverage
- Install `$pipenv install pipenv install pytest-cov`
- Type `$pytest --cov=[myproj] [test_file.py]` to visualize coverage in console
- Type `$pytest --cov=[test_file.py] --cov-report=html` to report the coverage in html file
