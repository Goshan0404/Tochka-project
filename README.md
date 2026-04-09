# How to run
Pull project files, install docker and run:

`docker-compose up --build`

To open pgadmin:

`http://localhost:5050/`

    - PGADMIN_DEFAULT_EMAIL=admin@example.com
    - PGADMIN_DEFAULT_PASSWORD=admin
    - POSTGRES_USER=myuser
    - POSTGRES_PASSWORD=mypassword

To install all required libs run:

`pip install -r requirements.txt`

if you add new lib don't forget to modify requirements.txt

`pip freeze -> ./app/requirements.txt`