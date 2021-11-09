
# MLaaS ML Backend Project

## Setting development environment
Create virtual environment with the following command:
```
$ python -m venv env
```
Activate the virtual environment with the following command:
```
$ source env/bin/activate
```
Install the packages from **requirements.txt** with the following command:
```
$ pip install -r requirements.txt
```
Run the server with following command:
```
$ python manage.py runserver
```
Open the postman and goto 

 1. `http://localhost:8000/analysis?document_name=` to get simple key value pairs extracted from AWS Textract response.
 2. `http://localhost:8000/predict/` to get the prediction using the output of the above REST API as input.

## Stopping the development environment
Ctrl + C to quit server
Deactivate the virtual environment with the following command:
```
deactivate
```