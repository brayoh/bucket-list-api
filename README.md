[![Build Status](https://travis-ci.org/brayoh/bucket-list-api.svg?branch=develop)](https://travis-ci.org/brayoh/bucket-list-api)
[![Coverage Status](https://coveralls.io/repos/github/brayoh/bucket-list-api/badge.svg?branch=develop)](https://coveralls.io/github/brayoh/bucket-list-api?branch=develop)

# Awesome Bucketlist API
A Bucketlist is a list of items, activities or goals you want to achieve before you "kick the bucket" this is an API to allow you create a new user account, login into your account, create, update, view or delete bucketlists and bucketlist items.

- API Documentation - http://docs.awesomebucketlist.apiary.io/

## Installation and Set Up
Clone the repo from GitHub:
```
git clone https://github.com/brayoh/bucket-list-api
```

Fetch from the develop branch:
```
git fetch origin develop
```

Navigate to the root folder:
```
cd bucketlist-api
```

Install the required packages:
```
pip install -r requirements.txt
```

Initialize, migrate, and upgrade the database:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Launching the Program
Run ```python run.py```. You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to test the API.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/auth/register/` | POST  | User registration | FALSE |
|  `/api/v1/auth/login/` | POST | User login | FALSE |
| `/api/v1/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/api/v1/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item | TRUE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |



## Testing
To run tests locally, run the following command: ```nosetests```

## Built With...
* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
