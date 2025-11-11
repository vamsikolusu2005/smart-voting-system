# routes/vote.py
from flask import Blueprint, request, jsonify
from models import db, Vote, Voter
from utils.sms import send_sms
import datetime

vote_bp = Blueprint('vote', __name__)

@vote_bp.route('/cast', methods=['POST'])
def cast_vote():
    data = request.json
    voter_db_id = data.get('voter_db_id')
    candidate_id = data.get('candidate_id')
    location = data.get('location', '')
    # check if already voted
    if Vote.query.filter_by(voter_id=voter_db_id).first():
        return jsonify({'error':'Already voted'}), 400
    v = Vote(voter_id=voter_db_id, candidate_id=candidate_id, location=location)
    db.session.add(v); db.session.commit()
    # send confirmation
    voter = Voter.query.get(voter_db_id)
    msg = f"Your vote has been recorded at {location} on {v.voted_at}. If this wasn't you, report: /complaint"
    send_sms(voter.mobile, msg)
    return jsonify({'message':'Vote recorded'}), 200
