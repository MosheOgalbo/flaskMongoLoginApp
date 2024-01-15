# Project Setup

## The application is divided into two parts, server and client :

### <span style="color:red"> server:   

#### Create main (flaskMongoDB) project folder

1. Create main (app_server) project folder

2. Fcreate virtual environment inside of it(main project folder)
```bash
#Linux and Mac
python -m venv venv

#windows users
python -m venv c:\path\to\myenv
``` 

3. Activate the virtual environment
```bash
# Linux and Mac
source venv/bin/activate

#Windows users
\venv\Scripts\activate.bat
```
4.Install all project dependencies

```bash
pip install flask Flask-PyMongo Flask-WTF

python -m pip install "pymongo[srv]
```
5.The file structure in the server app infrastructure
```bash
project_root_dir
│
|
|
|__ application
|    |
|    |__ templates
|    |__ __init__.py
|    |__ routes.py
|    |__ forms.py
|
|
|__ venv
|
|
|
|__ README.md
|
|
|__ run.py
```