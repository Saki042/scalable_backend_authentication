#!/bin/sh
export FLASK_APP=./booksappcode/index.py
pipenv run flask --debug run -h 0.0.0.0
