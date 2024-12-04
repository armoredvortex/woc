from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy(app)

# Define the models for election and options
class Election(db.Model):
    __tablename__ = 'election'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), default='active')
    options = db.relationship('Option', backref='election', lazy=True)

class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    votes = db.Column(db.Integer, default=0)

# Create tables in the database if they do not exist
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error initializing database: {e}")


#  Dashboard
@app.route('/')
def home():
    elections = Election.query.all()  # Get all elections from the database
    return render_template('dashboard.html', elections=elections)

# Create Election
@app.route('/create_election', methods=['POST', 'GET'])
def create_election():
    if request.method == 'POST':
        election_name = request.form['title']
        candidates = request.form.getlist('candidates[]')
        # store in database
        new_election = Election(name=election_name)
        db.session.add(new_election)
        db.session.commit()
        print("Election added to the database")
        # add options to the database
        for candidate in candidates:
            if candidate:
                new_option = Option(name=candidate, election_id=new_election.id)
                db.session.add(new_option)
        db.session.commit()
        print("Options added to the election")


        return redirect('/')
    
    return render_template('create_election.html')

@app.route('/election/<int:election_id>', methods=['GET', 'POST'])
def election(election_id):
    election = Election.query.get(election_id)
    print(election)
    options = Option.query.filter_by(election_id=election_id).all()
    return render_template('election.html', election=election, options=options)

if (__name__ == "__main__"):
    app.run(debug=True)