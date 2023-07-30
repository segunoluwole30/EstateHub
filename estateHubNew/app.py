from multiprocessing import synchronize
from flask import Flask, render_template, request, flash, redirect
from flask import Flask, render_template, request, flash, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2



app = Flask(__name__, static_folder='staticFiles')
# Login page
app.config['SECRET_KEY'] = 'csce310'
# Initialize the Flask session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Login page

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #password fields
        if username == 'Admin' and password == 'csce310':
            session['logged_in'] = True
            return redirect('/startup')
        else:
            flash('Invalid Login Credentials! Ask Admin, All Agents can access using this login!', 'error')
    
    return render_template('login.html')



    

# Startup page route
@app.route('/startup')
def startup():
    # Check if the user is logged in before showing the startup page
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        # If the user is logged in, render the startup page
        return render_template('startup.html')



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:group8@34.29.172.246/estatehub'
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
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.contractor_id'))
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
    return render_template('login.html')

# FIXED CRUD for AGENTS
@app.route('/agents/<action>', methods=['GET', 'POST'])
@app.route('/agents/<action>/<int:agent_id>', methods=['GET', 'POST'])
def agent_CRUD(action, agent_id=None):
    # CREATE method for CRUD - C
    if action == 'create': 
        if request.method == 'POST':
            agent_name = request.form['agent_name']
            agent_phone = request.form['agent_phone']
            new_agent = Agent(agent_name=agent_name, agent_phone=agent_phone)

            # Adding agent
            db.session.add(new_agent)
            db.session.commit()

            # Return to agent page
            return redirect('/agents')

        return render_template('create_agent.html')
    
    # CRUD - U, Update 
    elif action == 'update':
        agent = Agent.query.get_or_404(agent_id)

        if request.method == 'POST':
            agent_name = request.form['agent_name']
            agent_phone = request.form['agent_phone']

            # Updating to current values
            agent.agent_name = agent_name
            agent.agent_phone = agent_phone
            db.session.commit()

            return redirect('/agents')

        # Render the agent update form
        return render_template('update_agent.html', agent=agent)

    # CRUD - D, Delete
    elif action == 'delete':
        agent = Agent.query.get_or_404(agent_id)

        # Delete agent found from the PK 
        db.session.delete(agent)
        db.session.commit()
        return redirect('/agents')

    # CRUD - R, Retrieve
    else:
        return redirect('/agents')


# End agents CRUD 

# CRUD routes for Contractors
@app.route('/contractors/<action>', methods=['GET', 'POST'])
@app.route('/contractors/<action>/<int:contractor_id>', methods=['GET', 'POST'])
def contractor_CRUD(action, contractor_id=None):
    # CREATE method for CRUD - C
    if action == 'create': 
        if request.method == 'POST':
            contractor_name = request.form['contractor_name']
            contractor_phone = request.form['contractor_phone']
            new_contractor = Contractor(contractor_name=contractor_name, contractor_phone=contractor_phone)

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

#Start of CRUD for Contracts
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

# Start of CRUD for Sales

@app.route('/sales/<action>', methods=['GET', 'POST'])
@app.route('/sales/<action>/<int:sale_id>', methods=['GET', 'POST'])
def sales_CRUD(action, sale_id=None):
    if action=='create':

        if request.method=='POST':
            agent_id = request.form['agent_id']
            property_id = request.form['property_id']
            customer_id = request.form['customer_id']
            sale_date = request.form['sale_date']
            sale_amount = request.form['sale_amount']

            new_sale = Sale(agent_id=agent_id, customer_id=customer_id, property_id=property_id, sale_date=sale_date, sale_amount=sale_amount)

            db.session.add(new_sale)
            db.session.commit()

            return redirect('/sales')
        
        all_agents = Agent.query.all()
        all_properties = Property.query.all()
        all_customers = Customer.query.all()
        return render_template('create_sale.html', agents=all_agents, properties=all_properties, customers=all_customers)

    elif action=='update':
        
        sale = Sale.query.get_or_404(sale_id)

        if request.method == 'POST':
            agent_id = request.form['agent_id']
            property_id = request.form['property_id']
            customer_id = request.form['customer_id']
            sale_date = request.form['sale_date']
            sale_amount = request.form['sale_amount']

            sale.agent_id = agent_id
            sale.property_id = property_id
            sale.customer_id = customer_id
            sale.sale_date = sale_date
            sale.sale_amount = sale_amount

            db.session.commit()

            return redirect('/sales')

        all_agents = Agent.query.all()
        all_properties = Property.query.all()
        all_customers = Customer.query.all()
        return render_template('update_sale.html', sale=sale, agents=all_agents, properties=all_properties, customers=all_customers)

    elif action=='delete':
        
        sale = Sale.query.get_or_404(sale_id)

        db.session.delete(sale)
        db.session.commit()
        return redirect('/sales')
    
    else:
        return redirect('/sales')

# End of CRUD for Sales

# Start of CRUD for Properties

@app.route('/properties/<action>', methods=['GET', 'POST'])
@app.route('/properties/<action>/<int:property_id>', methods=['GET', 'POST'])
def properties_CRUD(action, property_id=None):
    if action=='create':

        if request.method=='POST':
            property_address = request.form['property_address']
            property_zip = request.form['property_zip']
            number_beds = request.form['number_beds']
            number_baths = request.form['number_baths']
            agent_id = request.form['agent_id']
            listing_date = request.form['listing_date']
            price = request.form['price']


            new_property = Property(property_id=property_id, property_address=property_address, property_zip=property_zip, number_beds=number_beds, number_baths=number_baths, agent_id=agent_id, listing_date=listing_date, price=price)

            db.session.add(new_property)
            db.session.commit()

            return redirect('/properties')
        
        all_agents = Agent.query.all()
        return render_template('create_property.html', agents=all_agents)

    elif action=='update':
        
        property = Property.query.get_or_404(property_id)

        if request.method == 'POST':
            property_address = request.form['property_address']
            property_zip = request.form['property_zip']
            number_beds = request.form['number_beds']
            number_baths = request.form['number_baths']
            agent_id = request.form['agent_id']
            listing_date = request.form['listing_date']
            price = request.form['price']

            property.property_id = property_id
            property.property_address = property_address
            property.property_zip = property_zip
            property.number_beds = number_beds
            property.number_baths = number_baths
            property.agent_id = agent_id
            property.listing_date = listing_date
            property.price = price

            db.session.commit()

            return redirect('/properties')

        all_agents = Agent.query.all()
        return render_template('update_property.html', property=property, agents=all_agents)

    elif action=='delete':
        
        property = Property.query.get_or_404(property_id)

        db.session.delete(property)
        db.session.commit()
        return redirect('/properties')
    
    else:
        return redirect('/properties')

# End of CRUD for Properties

# CRUD routes for Customer
@app.route('/customers/<action>', methods=['GET', 'POST'])
@app.route('/customers/<action>/<int:customer_id>', methods=['GET', 'POST'])
def customer_CRUD(action, customer_id=None):
    # CREATE method for CRUD - C
    if action == 'create':
        if request.method == 'POST':
            preferred_zip = request.form['preferred_zip']
            preferred_beds = request.form['preferred_beds']
            preferred_baths = request.form['preferred_baths']
            preferred_price = request.form['preferred_price']
            new_customer = Customer(preferred_zip=preferred_zip, preferred_beds=preferred_beds, preferred_baths=preferred_baths, preferred_price=preferred_price)

            #Adding Customer
            db.session.add(new_customer)
            db.session.commit()

            # Return to Customer page
            return redirect('/customers')
        
        return render_template('create_customer.html')
    
    # UPDATE
    elif action == 'update':
        # Get PK for updates
        customer = Customer.query.get_or_404(customer_id)

        if request.method == 'POST':
            preferred_zip = request.form['preferred_zip']
            preferred_beds = request.form['preferred_beds']
            preferred_baths = request.form['preferred_baths']
            preferred_price = request.form['preferred_price']
            
            #update to current values
            customer.preferred_zip = preferred_zip
            customer.preferred_beds = preferred_beds
            customer.preferred_baths = preferred_baths
            customer.preferred_price = preferred_price
            db.session.commit()

            return redirect('/customers')
        
        # Render customer update form
        return render_template('update_customer.html', customer=customer)
    
    # DELETE
    elif action == 'delete':
        # Get PK
        customer = Customer.query.get_or_404(customer_id)

        # Delete customer found from PK
        db.session.delete(customer)
        db.session.commit()
        return redirect('/customers')
    
    else:
        return redirect('/customers')
    
# End of CRUD for Customers
            



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
