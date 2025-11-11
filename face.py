
from flask import Blueprint, request, jsonify
import cv2, numpy as np, os
face_bp = Blueprint('face', __name__)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer_path = 'recognizer/lbph.yml'
recognizer = cv2.face.LBPHFaceRecognizer_create()
if os.path.exists(recognizer_path):
    recognizer.read(recognizer_path)

@face_bp.route('/recognize', methods=['POST'])
def recognize():
    vid = int(request.form.get('voter_db_id'))  # claimant voter id
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return jsonify({'error':'No face detected'}), 400
    x,y,w,h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    label, confidence = recognizer.predict(face_roi)
    # Experimentally choose threshold, e.g., confidence < 60
    if label == vid and confidence < 60:
        return jsonify({'message':'Face verified', 'confidence':confidence}), 200
    else:
        return jsonify({'error':'Face mismatch', 'predicted':label, 'confidence':confidence}), 403
