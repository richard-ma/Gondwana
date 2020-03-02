# generate migrate script
./manage.py db migrate

# upgrade database
./manage.py db upgrade

# run server as development
FLASK_ENV=development ./manage.py runserver
