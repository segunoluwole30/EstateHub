# CSCE 310 - Group 8 Estate Hub Project

## Introduction ##

This project code was written for CSCE 310 Summer 2023 Semester. It uses the language of Python3 with PostgreSQL as the server, SQLAlchemy and Flask as the backend, and HTML and CSS as the frontend.

We utilized the following Cloud services:
- Google Cloud to host our PostgreSQL database
- Render to deploy our Web Service automatically from GitHub.

Our goal is to create an application that streamlines the real estate sales process, increases agent productivity, and efficiently handles real estate data.


## Requirements ##

* PostgreSQL - 14
* Python 3.10
* SQLAlchemy - 1.4.36
* Flask - 2.1.2
* Flask-SQLAlchemy - 2.5.1
* psycopg2-binary - 2.9.1

## Installation ##

Install [PostgreSQL](https://www.postgresql.org/download/) on your machine. This way you can connect to our database on Google Cloud. 
Ubuntu/Windows terminal can be used to connect. 

Make sure you have [Anaconda](https://www.anaconda.com/download) installed as well to access the Anaconda Prompt. 

Use our environment file named environment-estatehubapp3 in order to ensure you have all dependencies installed.

After heading to the path of the repository location on your machine in the Anaconda Prompt, make sure to enter the folder (dir estateHubNew) with the environment file.

Enter these commands to clone the environment in your Anaconda terminal: 

```
conda env create -f environment-estatehubapp3.yml
```

Then activate the environment:
 
```
conda activate estatehubapp3
```

## Connect to Shared Database ##

Make sure to start your PostgreSQL on your machine (Ubuntu/Windows) 

Enter this command to connect to our database. When asked for the password after connecting type in group8
```
psql -h 34.29.172.246 -p 5432 -U postgres -d estatehub
```
Password = group8

This should allow you to have access to the shared database.

## Alternative Connection Method Local Database (Optional) ##
Alternatively, if you want to use your own database and tables... you can change the contents of the app.py file for the connection.

Currently the line is 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:group8@34.29.172.246/estatehub'

You can set this line to your own database and tables using. 
postgresql://<user>:<password>@<hostname>/<databasename>

