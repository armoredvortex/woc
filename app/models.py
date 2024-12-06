from app import db

class Election(db.Model):
    __tablename__ = 'election'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), default='active')
    options = db.relationship('Option', backref='election', lazy=True)
    public_key = db.Column(db.Text, nullable=False)
    shares = db.Column(db.Text, nullable=False)

class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    votes = db.Column(db.Integer, default=0)
