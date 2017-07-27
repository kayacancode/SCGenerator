This is the Smart Contract Generator Django webapp:
maintained and developed by: Sandro Luck

Additional documentation might be found at https://www.djangoproject.com/

To start this application:
1. Install Python (Versions >=3 should work, yet we have developed this application using 3.5.2) and pip.

2.1 pip install django
2.2 pip install naked

3. cd to \"Path to this app"\mysite\mysite
3.1 locate the manage.py file (you have to be in the folder where manage.py is)

4. python manage.py makemigrations
4.1 python manage.py migrate

5. run "python manage.py runserver"

6. Open your browser and go to localhost:8000/smartpollution/

Switching Database:
Since setting up the application is easiest with SQLite it is the default database.
However if you wish to use a different database choose one from https://docs.djangoproject.com/en/1.11/ref/databases/ and follow the django documentation.

Optional:
To create an admin user: python manage.py createsuperuser
You can now go to localhost:8000/admin/ and modify the database directly

To get the full Blockchain support (Mainly the Smart Contractg Monitor):
1. Install nodejs https://nodejs.org/en/download/
2. Install geth https://github.com/ethereum/go-ethereum/wiki/geth
  2.1 run 



