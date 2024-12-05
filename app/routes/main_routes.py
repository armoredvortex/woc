from flask import Blueprint, render_template, request, redirect
from app.models import db, Election, Option

# Define Blueprint
main_bp = Blueprint('main', __name__)

# Home/Dashboard route
@main_bp.route('/')
def home():
    elections = Election.query.all()
    return render_template('dashboard.html', elections=elections)

# Create Election route
@main_bp.route('/create_election', methods=['POST', 'GET'])
def create_election():
    if request.method == 'POST':
        election_name = request.form['title']
        candidates = request.form.getlist('candidates[]')
        # Store in database
        new_election = Election(name=election_name)
        db.session.add(new_election)
        db.session.commit()

        # Add options to the database
        for candidate in candidates:
            if candidate:
                new_option = Option(name=candidate, election_id=new_election.id)
                db.session.add(new_option)
        db.session.commit()

        return redirect('/')
    
    return render_template('create_election.html')

# Election details route
@main_bp.route('/election/<int:election_id>', methods=['GET', 'POST'])
def election(election_id):
    election = Election.query.get(election_id)
    options = Option.query.filter_by(election_id=election_id).all()
    return render_template('election.html', election=election, options=options)
