from multiprocessing import synchronize
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2


app = Flask(__name__)
# Please change your port to 5432 wherever you find it. I am using port 5433.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:csce310@localhost:5433/estatehub'
db = SQLAlchemy(app)



# Agent- Agent(agent_id, agent_name, agent_phone)
class Agent(db.Model):
    agent_id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(100))
    agent_phone = db.Column(db.String(20))

# Property- Property(property_id, property_address, property_zip,
# number_beds, number_baths, agent_id, listing_date, price)
class Property(db.Model):
    property_id = db.Column(db.Integer, primary_key=True)
    property_address = db.Column(db.String(100))
    property_zip = db.Column(db.String(10))
    number_beds = db.Column(db.Integer)
    number_baths = db.Column(db.Integer)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.agent_id'))
    listing_date = db.Column(db.Date)
    price = db.Column(db.Numeric(10, 2))

# Customer - Customer(customer_id, preferred_zip,
# preferred_beds, preferred_baths, preferred_price)
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    preferred_zip = db.Column(db.String(10))
    preferred_beds = db.Column(db.Integer)
    preferred_baths = db.Column(db.Integer)
    preferred_price = db.Column(db.Numeric(10, 2))

# Contractor- Contractor(contractor_id, contractor_name, contractor_phone)
class Contractor(db.Model):
    contractor_id = db.Column(db.Integer, primary_key=True)
    contractor_name = db.Column(db.String(100))
    contractor_phone = db.Column(db.String(20))

# Sale- Sale(sale_id, agent_id, customer_id, property_id, sale_date, sale_amount)
class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.agent_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'))
    sale_date = db.Column(db.Date)
    sale_amount = db.Column(db.Numeric(10, 2))

# Contract-Contract(contract_id, contractor_id, property_id)
class Contract(db.Model):
    contract_id = db.Column(db.Integer, primary_key=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.contractor_id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'))

# Contractors CRUD
# @app.route('/contractors', methods=['GET', 'POST'])
# def contractors_CRUD():
   #  pass


@app.route('/contractors', methods=['GET'])
def contractors_page():
    table_contractors = Contractor.query.all()
    return render_template('contractors.html', contractors=table_contractors)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
