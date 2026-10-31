# EstateHub — Real Estate Management Platform

A full-stack web application that streamlines the real estate sales process. Agents can manage
properties, customers, contractors, sales and contracts from one dashboard, backed by a cloud-hosted
PostgreSQL database.

Built by a team of students for CSCE 310 (Database Systems) at Texas A&M University, Summer 2023.

## Features

- **Agent authentication:** session-based login for agents.
- **Full CRUD for six entities:** agents, properties, customers, contractors, sales and contracts, each
  with list, create, update and delete views.
- **Relational data model:** foreign keys link each property to its listing agent, each sale to an agent,
  customer and property, and each contract to a contractor and property.
- **Sales reporting:** a per-agent sales report listing every sale with a running total.
- **Dynamic forms:** property dropdowns filter by agent through a JSON endpoint
  (`/get_properties/<agent_id>`).
- **Continuous deployment:** auto-deployed to Render on every push, with Gunicorn as the WSGI server.

## Tech stack

| Layer      | Technologies                                         |
| ---------- | ---------------------------------------------------- |
| Backend    | Python 3.10, Flask, Flask-SQLAlchemy, Flask-Session, Flask-Migrate |
| Database   | PostgreSQL 14 (hosted on Google Cloud SQL)           |
| Frontend   | Jinja2 templates, HTML, CSS                          |
| Deployment | Render, Gunicorn                                     |

## Data model

- An **Agent** lists many **Properties**.
- A **Sale** ties together one Agent, one **Customer** and one Property.
- A **Contract** ties a **Contractor** to a Property.

| Table        | Purpose                                         |
| ------------ | ----------------------------------------------- |
| `Agent`      | Real estate agents and their contact details    |
| `Property`   | Listings: address, ZIP, beds/baths, price, listing date and listing agent |
| `Customer`   | Buyers and their preferences (ZIP, beds, baths, price) |
| `Sale`       | Completed transactions linking agent, customer and property, with date and amount |
| `Contractor` | Service providers and their contact details     |
| `Contract`   | Work agreements between a contractor and a property |

## Getting started

### Prerequisites

- Python 3.10
- PostgreSQL 14 (local or hosted)

### 1. Install dependencies

```bash
git clone https://github.com/segunoluwole30/EstateHub.git
cd EstateHub
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

A Conda environment file is also provided:
`conda env create -f estateHubNew/environment-estatehubapp3.yml`.

### 2. Create the database

```sql
CREATE DATABASE estatehub WITH OWNER = postgres ENCODING = 'UTF8';
CREATE SCHEMA estatehub AUTHORIZATION postgres;
```

Point the app at your database by setting `SQLALCHEMY_DATABASE_URI` in `estateHubNew/app.py`:

```
postgresql://<user>:<password>@<host>:5432/estatehub
```

The tables are created automatically on first run.

### 3. Run

```bash
cd estateHubNew
flask run
```

Then open <http://localhost:5000>.

## Deployment

The app is deployed as a Render Web Service:

| Setting       | Value                              |
| ------------- | ---------------------------------- |
| Build command | `pip install -r requirements.txt`  |
| Start command | `gunicorn estateHubNew.app:app`    |

Auto-deploy is enabled, so every push to `main` triggers a new deployment.

## Project structure

```
EstateHub/
├── requirements.txt
└── estateHubNew/
    ├── app.py              # Flask app, models and routes
    ├── templates/          # Jinja2 views (list / create / update per entity, login, sales report)
    └── staticFiles/        # CSS and images
```
