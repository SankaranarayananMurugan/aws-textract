
# AWS Textract Project

## Setting development environment
Clone the project using below command
```
git clone $CLONE_URL$
```
Create virtual environment with the following command in the same directory where the project is cloned:
```
$ python -m venv env
```
Activate the virtual environment with the following command:
```
$ source env/bin/activate
```
Change directory to the root of the project
```
cd aws-textract
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
