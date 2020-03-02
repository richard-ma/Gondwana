# install require packages
pip install -r requirements.txt

# Create database dir
mkdir database

# init flask migrate
rm -rf database/*
rm -rf migrations
FLASK_ENV=development ./manage.py db init
