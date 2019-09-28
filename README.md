# webapp
Flask webapp for showing aggregate hydrometer data

## Requirements
### Install postgresql

```bash
    $ sudo apt-get update
    $ sudo apt-get install postgresql postgresql-contrib
```

### Add a postgresql user

```bash
    $ sudo -i -u postgres

    $ createuser --interactive -W
    Enter name of role to add: dyp
    Shall the new role be a superuser? (y/n) y
    Password: dyp

    $ createdb dyp_web
    $ exit
```

### Install virtualenv and postgresql python adapter and create new venv

```bash
    $ cd backend
    $ sudo pip3 install virtualenv psycopg2
    $ python3 -m venv venv
```

### Activate venv and install required python frameworks

```bash
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

### Populate Database

```bash
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
```

### Start Flask

```bash
    $ python appserver.py
```