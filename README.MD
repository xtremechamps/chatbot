# Chat Bot using Python Flask

## Contribute to Projecct
* Fork the project
* Put pull request

## Installation Guide

* Install a virtualenv
$ pip install virtualenv

* Create virtualenv
$ virtualenv doraenv

* Activate virtualenv
$ doraenv\Scripts\activate

* Install all required libs by using pip
$ pip install -r requirements.txt

* To run locally
$ python facebookbot.py 5000

* Open Web browser and enter url
http://localhost:5000/ or http://127.0.0.1:5000/

## Testing How-To:


1. Activate Virtual environment as given in `Installation Guide`
2. Install requirements
> pip install -r test-requirements.txt
3. Run nosetests
> nosetests --verbose

*Note* `--verbose` flag not required but recommended

## Heroku support
* Create a new account on heroku and download heroku cli
* Login into heroku
$ heroku login

* Go to your project 
$ heroku create appname  or $ heroku git:clone appname

* To deploy code to heroku
$ git push heroku master

