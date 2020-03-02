# install require packages
pip install -r requirements.txt

# Create database dir
mkdir database

# init flask migrate
rm -rf database/*
rm -rf migrations
./manage.py db init
