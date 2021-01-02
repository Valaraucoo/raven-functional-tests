## Raven - functional tests

### Setup

Before running tests you must setup your virtual enviroment and install required dependencies.

First, create `venv`:
```bash
$ python -m venv venv
``` 
Activate your virtual enviroment:
```bash
$ source venv/bin/activate
```
Then, install required dependencies:
```bash
$ pip install -r requirements.txt
```

Now you can run tests using `pytest` command.

### Running tests

Before running test, make sure that your local server is running on port `8080`. After that run tests:
```bash
$ pytest
```