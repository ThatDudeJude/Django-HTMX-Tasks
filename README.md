# Tasks App

A simple web application for planning and saving details on tasks.

## Project Description

This web application lets users write plans on future tasks. Tasks can be prioritized, updated and deleted. The backend is built using the Django framework, relying on its customizable features to design an admin and authentication system. A postgresql database connection is integrated for data storage.  The frontend ui uses the htmx library for handling dynamic behavior.

### Technology used
| Technology  |       Version    |      Utility    |
|-------------|------------------|-----------------|
|    Django   |  v3.2.13         | Python based web-framework|
|   Postgres  | v14.0            | SQL based Relational Database Management System (RDMS)|
| Psycopg2    |     v2.9.1       | A PostgreSQL database adapter for Python web apps |
| HTMX       |     v1.8.6      | A Javascript-based library that facilitates access to modern browser features via hypertext for building dynamic frontend uis with minimum or no Javascript|



## Installation and Setup


1. Launch your terminal.
2. Create a new folder and navigate to it.
   ```
    mkdir Tasks_App
    cd Tasks_App
   ```
3. Clone this github repository here: https://github.com/ThatDudeJude/Tasks_App
   `
4. Ensure that [python](https://www.python.org) version v3.8+ and pip is installed in your computer.
5. Install a postgres server for your OS ([more info here](https://www.postgres.org/download)) if not installed. For windows users, you can add psql.exe to path.
6. Create a new virtual environment and activate it .For Linux and Mac OS run `python3 -m venv venv && ./venv/bin/activate` . For Windows cmd.exe run `c:\>c:\Python38\python -m venv venv && venv/SCRIPTS/activate.bat` .
7. Install a postgres server for your OS if not installed ([more info here](https://www.postgres.org/download)). 
8. Install all required libraries. 
   ```
   python3 -m pip install -r requirements.txt
   ```
9.    Set up an smtp service, preferrably [gmail's smtp](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab). Add the following variables to your environment
```
    DEFAULT_FROM_EMAIL=[youraccount@gmail.com]
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=[youraccount@gmail.com]
    EMAIL_HOST_PASSWORD=[your smtp service account password]        
```
1.     Open a new terminal and create a postgres database for development and testing purposes. 

For Mac and Linux users, run :
```    
    sudo su postgres
    psql postgres
    \! hostname
```

For Windows users, run:
```
    psql -U postgres    
    \! hostname
```
You need to create a role and assign the necessary priviledges
```    
    CREATE USER tasks_app with password 'tasks_app_password';        
    CREATE DATABASE tasks_app_db;
    GRANT ALL PRIVILEDGES ON DATABASE tasks_app_db TO tasks_app;
    \connect tasks_app_db
    \conninfo    
    \q
```
   
Now set the environment variables using information from hostname, the ez_pizza password, and the database's `\conninfo` output.
   ```
   DATABASE_URL=postgres://USERNAME:PASSWORD@HOSTNAME:PORT/tasks_app_db   
   ``` 
1.   Add a secret key for the Django app. To generate a secret key, type in ``python3 -c "import secrets; print(secrets.token_hex());" `` and use the output as the secret key.
```
    SECRET_KEY=[secret_key]        
    
```
To launch the django server, run ``python3 manage.py runserver`` and navigate to http://127.0.0.1:8000/ to view the application

## Tests

To run the tests make sure to press Ctrl + C to stop the server first and set the environment variable
```
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
For unit tests, run
```
    python manage.py test
```

## Contributing
Want to contribute? See contributing guidelines [here](/CONTRIBUTING.md).

## Codebeat

[![codebeat badge](https://codebeat.co/badges/f49762c5-7506-446a-b738-fe7f9fb8bc28)](https://codebeat.co/a/thatdudejude/projects/github-com-thatdudejude-bibliophiliac-profile_branch_final)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE.txt)