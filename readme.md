# Stores REST-API
This was built with Flask, Flask-RESTful, Flask-JWT and Flask-SQLAlchemy.

Deployed on Heroku.

You can test it with tools like postman using this url: 
https://rest-api-flask-python-stores.herokuapp.com/

Another way is clone github repository on your computer, and follow this steps:
1. Create virtual environment and activate it:

    - python3.8 - m venv myvenv
    
    - source venv/bin/activate

2. Load all dependencies:

    - pip install -r requirements.txt

3. Create local lightweight sql database SQLlite3:

    - flask shell
    
    - from app import app
    
    - from db import db
    
    - db.init_app(app)
    
    - db.create_all()

To reformat new code using black just run this command from root directory:

    - black .