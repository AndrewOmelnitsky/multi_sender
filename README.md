# Multi sender


## Installation
To install project clone repository:
```sh
git clone https://github.com/AndrewOmelnitsky/multi_sender.git
```
Go to project folder:
```sh
cd multi_sender
```
To install the dependencies, make sure you have `poetry` installed. Then run this:
```sh
poetry install
```

## Run server
There are several ways to start the server.
To run server go to the project directory `multi_sender`.

### Basic way
Than Activate virtual environment:
```sh
poetry shell
```
Add run app:
```sh
python main.py
```

### Poetry way to run server
Run this:
```sh
poetry run run-server
```

### Poetry way to run testing servers
If you want to run several test servers at once to test the code or demonstrate local operation, then do so.
Run this:
```sh
poetry run run-test-servers
```
