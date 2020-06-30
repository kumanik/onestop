# **One Stop**
A web app to manage records using MongoDB.  
Uses MongoEngine Document-Object Mapper to simulate Django ORM functions for MongoDB.  
Visit [MongoEngine docs](http://docs.mongoengine.org/) to see more.


### Local build Instructions

- Edit .env.example to .env
- Create a mongo database add databse details to .env
- Create a postgres databse add DATABASE_URL in .env in this format: "postgresql://[user:[password]]@[netloc]:[port]/[dbname]"
- Create a python virtual environment using virtualenv or pipenv
- Inside the project directory run
```shell
# for virtualenv
pip install -r requirements.txt
# for pipenv
pipenv install
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
