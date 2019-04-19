web: export FLASK_APP='migration.py'
web: flask db init
web: flask db migrate
web: flask db upgrade
web: python run.py
web: sudo apt-get install nginx
web: sudo service nginx start
web: gunicorn -b 0.0.0.0:8080 wsgi 
