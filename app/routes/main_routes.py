from flask import Blueprint, render_template, request, redirect, session
from app.models import db, Election, Option, Candidate, Votes
# import everything from app.utils
from app.utils import *
import re
import random
import uuid
import pickle
import base64


# Define Blueprint
main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/')
def home():
    return render_template('home.html')

# Admin Dashboard route
@main_bp.route('/admin')
def admin():
    elections = Election.query.all()
    return render_template('admin.html', elections=elections)

# Create Election route
@main_bp.route('/create_election', methods=['POST', 'GET'])
def create_election():
    if request.method == 'POST':
        election_name = request.form['title']
        candidates = request.form.getlist('candidates[]')

        public_key_json, private_key_json = generate_keys()
        shares = generate_shares(private_key_json)
        
        new_election = Election(name=election_name, public_key=public_key_json, shares=shares)
        db.session.add(new_election)
        db.session.commit()
        
        # Add options to the database
        for candidate in candidates:
            if candidate:
                new_option = Option(name=candidate, election_id=new_election.id)
                db.session.add(new_option)
        db.session.commit()

        return redirect('/admin')
    
    return render_template('create_election.html')

# Election details route
@main_bp.route('/election/<int:election_id>', methods=['GET', 'POST'])
def election(election_id):
    election = Election.query.get(election_id)
    shares_list = re.search(r'\[(.*?)\]', election.shares).group(1)
    shares_list = shares_list.split(', ')
    options = Option.query.filter_by(election_id=election_id).all()
    election.shares = "Hidden"
    return render_template('election.html', election=election, options=options, shares=shares_list)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        salt = str(random.randint(1000, 9999))
        
        hashed_email = hash_data(email)
        hashed_password = hash_data(password, salt)
        
        # check if hashed_email already exists in database
        candidate = Candidate.query.filter_by(email=hashed_email).first()
        if candidate:
            return render_template('register.html', email_exists=True)
         
        new_candidate = Candidate(email=hashed_email, password=hashed_password, salt=salt)
        db.session.add(new_candidate)
        db.session.commit()
        return redirect('/login')
        
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        hashed_email = hash_data(email)
        candidate = Candidate.query.filter_by(email=hashed_email).first()
        if not candidate:
            return render_template('login.html', email_not_found=True)
        
        hashed_password = hash_data(password, candidate.salt)
        if hashed_password == candidate.password:
            # generate session token
            session_token = str(uuid.uuid4())
            candidate.session_token = session_token
            db.session.commit()
            
            session['session_token'] = session_token
            session['user_id'] = candidate.id
            session.permanent = True
            
            return redirect('/vote')
            
        else:
            return render_template('login.html', password_incorrect=True)
        
    return render_template('login.html')

@main_bp.route('/vote', methods=['GET', 'POST'])
def vote():
    session_token = session.get('session_token')
    user_id = session.get('user_id')

    if not session_token or not user_id:
        return redirect('/login')  # Redirect if no session

    # Validate session token with the database
    candidate = Candidate.query.filter_by(id=user_id, session_token=session_token).first()
    if not candidate:
        return redirect('/login')  # Redirect if invalid session

    elections = Election.query.all()
    return render_template('vote.html', elections=elections, candidate=candidate)

@main_bp.route('/vote/<int:election_id>', methods=['GET', 'POST'])
def vote_election(election_id):
    session_token = session.get('session_token')
    user_id = session.get('user_id')

    if not session_token or not user_id:
        return redirect('/login')
    
    candidate = Candidate.query.filter_by(id=user_id, session_token=session_token).first()
    if not candidate:
        return redirect('/login')
    
    election = Election.query.get(election_id)
    options = Option.query.filter_by(election_id=election_id).all()
    public_key = reconstruct_public_key(election.public_key)

    if request.method == 'POST':
        vote = request.form['option']
        vote_array = [0] * len(options)
        vote_array[int(vote)] = 1

        vote_array = encrypt_vote_vector(public_key, vote_array)
        vote_b64 = base64.b64encode(pickle.dumps(vote_array))
        print(vote_b64)
        new_vote = Votes(candidate_id=candidate.id, election_id=election_id, vote=vote_b64)

        db.session.add(new_vote)
        db.session.commit()
        return redirect('/vote')
    
    return render_template('vote_election.html', election=election, options=options, length=len(options))
