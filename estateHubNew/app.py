from multiprocessing import synchronize
from flask import Flask, render_template, request, flash, redirect
from flask import Flask, render_template, request, flash, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2


app = Flask(__name__)


# Login page
# Please change your port to 5432 wherever you find it. I am using port 5433.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:csce310@localhost:5433/estatehub'
db = SQLAlchemy(app)


# Agent- Agent(agent_id, agent_name, agent_phone)
class Agent(db.Model):
    agent_id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(100))
    agent_phone = db.Column(db.String(20))
    sales = db.relationship('Sale', backref='agent', lazy=True)

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
    # Add the relationship to Agent
    agent = db.relationship('Agent', backref='properties', lazy=True)
    contracts = db.relationship('Contract', backref='property', lazy=True)
    sales = db.relationship('Sale', backref='property', lazy=True)

# Customer - Customer(customer_id, preferred_zip,
# preferred_beds, preferred_baths, preferred_price)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    preferred_zip = db.Column(db.String(10))
    preferred_beds = db.Column(db.Integer)
    preferred_baths = db.Column(db.Integer)
    preferred_price = db.Column(db.Numeric(10, 2))
    sales = db.relationship('Sale', backref='customer', lazy=True)

# Contractor- Contractor(contractor_id, contractor_name, contractor_phone)


class Contractor(db.Model):
    contractor_id = db.Column(db.Integer, primary_key=True)
    contractor_name = db.Column(db.String(100))
    contractor_phone = db.Column(db.String(20))
    contracts = db.relationship('Contract', backref='contractor', lazy=True)

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
    contractor_id = db.Column(
        db.Integer, db.ForeignKey('contractor.contractor_id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'))


# All routes for entities
@app.route('/contractors', methods=['GET'])
def contractors():
    all_contractors = Contractor.query.all()
    return render_template('contractors.html', contractors=all_contractors)


@app.route('/agents', methods=['GET'])
def agents():
    all_agents = Agent.query.all()
    return render_template('agents.html', agents=all_agents)


@app.route('/properties', methods=['GET'])
def properties():
    all_properties = Property.query.all()
    return render_template('properties.html', properties=all_properties)


@app.route('/customers', methods=['GET'])
def customers():
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)


@app.route('/sales', methods=['GET'])
def sales():
    all_sales = Sale.query.all()
    return render_template('sales.html', sales=all_sales)


@app.route('/contracts', methods=['GET'])
def contracts():
    all_contracts = Contract.query.all()
    return render_template('contracts.html', contracts=all_contracts)


@app.route('/')
def index():
    return render_template('startup.html')


# CRUD routes for Contractors
@app.route('/contractors/<action>', methods=['GET', 'POST'])
@app.route('/contractors/<action>/<int:contractor_id>', methods=['GET', 'POST'])
def contractor_CRUD(action, contractor_id=None):
    # CREATE method for CRUD - C
    if action == 'create':
        if request.method == 'POST':
            contractor_name = request.form['contractor_name']
            contractor_phone = request.form['contractor_phone']
            new_contractor = Contractor(
                contractor_name=contractor_name, contractor_phone=contractor_phone)

            # Adding contractor
            db.session.add(new_contractor)
            db.session.commit()

            # Return to contractor oage
            return redirect('/contractors')

        return render_template('create_contractor.html')
    # CRUD - U, Update
    elif action == 'update':
        # Get the PK for updates
        contractor = Contractor.query.get_or_404(contractor_id)

        if request.method == 'POST':
            contractor_name = request.form['contractor_name']
            contractor_phone = request.form['contractor_phone']

            # Updating to current values
            contractor.contractor_name = contractor_name
            contractor.contractor_phone = contractor_phone
            db.session.commit()

            return redirect('/contractors')

        # Render the contractor update form
        return render_template('update_contractor.html', contractor=contractor)

    elif action == 'delete':
        # PK retrival for deletion
        contractor = Contractor.query.get_or_404(contractor_id)

        # Delete contractor found from the PK
        db.session.delete(contractor)
        db.session.commit()
        return redirect('/contractors')

    else:
        return redirect('/contractors')

# End of CRUD for Contractors

# Start of CRUD for Contracts


@app.route('/contracts/<action>', methods=['GET', 'POST'])
@app.route('/contracts/<action>/<int:contract_id>', methods=['GET', 'POST'])
def contract_CRUD(action, contract_id=None):
    # CREATE method for CRUD - C
    if action == 'create':
        if request.method == 'POST':
            contractor_id = request.form['contractor_id']
            property_id = request.form['property_id']

            new_contract = Contract(
                contractor_id=contractor_id,
                property_id=property_id
            )

            db.session.add(new_contract)
            db.session.commit()

            return redirect('/contracts')

        # Fetch all contractors and properties for the dropdown lists
        all_contractors = Contractor.query.all()
        all_properties = Property.query.all()
        return render_template('create_contract.html', contractors=all_contractors, properties=all_properties)

    # CRUD - U, Update
    elif action == 'update':
        contract = Contract.query.get_or_404(contract_id)

        if request.method == 'POST':
            contractor_id = request.form['contractor_id']
            property_id = request.form['property_id']

            contract.contractor_id = contractor_id
            contract.property_id = property_id

            db.session.commit()

            return redirect('/contracts')

        # Fetch all contractors and properties for the dropdown lists
        all_contractors = Contractor.query.all()
        all_properties = Property.query.all()
        return render_template('update_contract.html', contract=contract, contractors=all_contractors, properties=all_properties)

    # CRUD - D, Delete
    elif action == 'delete':
        contract = Contract.query.get_or_404(contract_id)

        db.session.delete(contract)
        db.session.commit()

        return redirect('/contracts')

    # CRUD - R, Retrieve
    else:
        return redirect('/contracts')

# End of CRUD for Contracts


# Start of CRUD for Agents


@app.route('/agents/<action>', methods=['GET', 'POST'])
@app.route('/agents/<action>/<int:agent_id>', methods=['GET', 'POST'])
def contractor_CRUD(action, agent_id=None):
    # CREATE method for CRUD - C
    if action == 'create':
        if request.method == 'POST':
            agent_name = request.form['agent_name']
            agent_phone = request.form['agent_phone']
            new_agent = Agent(
                agent_name=agent_name, agent_phone=agent_phone)

            # Adding agent
            db.session.add(new_agent)
            db.session.commit()

            # Return to agent page
            return redirect('/agents')

        return render_template('create_agent.html')
    # CRUD - U, Update
    elif action == 'update':
        # Get the PK for updates
        agent = Agent.query.get_or_404(agent_id)

        if request.method == 'POST':
            agent_name = request.form['agent_name']
            agent_phone = request.form['agent_phone']

            # Updating to current values
            agent.agent_name = agent_name
            agent.agent_phone = agent_phone
            db.session.commit()

            return redirect('agents')

        # Render the agent update form
        return render_template('update_agent.html', agent=agent)

    elif action == 'delete':
        # PK retrival for deletion
        agent = Agent.query.get_or_404(agent_id)

        # Delete contractor found from the PK
        db.session.delete(agent)
        db.session.commit()
        return redirect('/agents')

    else:
        return redirect('/agents')
# End of CRUD for Agents


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
