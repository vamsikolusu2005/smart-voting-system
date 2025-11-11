
from flask import Blueprint, request, jsonify
from models import db, Voter, OTP
from utils.sms import send_sms
import random, datetime

auth_bp = Blueprint('auth', __name__)

def generate_otp():
    return f"{random.randint(100000,999999)}"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    aadhar = data.get('aadhar'); voter_id = data.get('voter_id')
    name = data.get('name'); mobile = data.get('mobile')
    # basic checks
    if Voter.query.filter((Voter.aadhar==aadhar)|(Voter.voter_id==voter_id)).first():
        return jsonify({'error':'Aadhar or VoterID already registered'}), 400
    v = Voter(aadhar=aadhar, voter_id=voter_id, name=name, mobile=mobile)
    db.session.add(v); db.session.commit()
    # create OTP
    otp_code = generate_otp()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    otp = OTP(voter_id=v.id, otp=otp_code, expires_at=expiry, used=False)
    db.session.add(otp); db.session.commit()
    # send SMS (in dev, print)
    send_sms(mobile, f"Your SmartVote OTP is {otp_code}")
    return jsonify({'message':'OTP sent', 'voter_db_id': v.id}), 201

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    vid = data.get('voter_db_id'); code = data.get('otp')
    otp = OTP.query.filter_by(voter_id=vid, otp=code, used=False).order_by(OTP.expires_at.desc()).first()
    if not otp: return jsonify({'error':'Invalid OTP'}), 400
    if otp.expires_at < datetime.datetime.utcnow(): return jsonify({'error':'OTP expired'}), 400
    otp.used = True
    v = Voter.query.get(vid)
    v.is_verified = True
    db.session.commit()
    return jsonify({'message':'OTP verified, proceed to face enrollment'}), 200
