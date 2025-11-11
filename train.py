
import os, cv2, numpy as np
face_dir = 'face_data'
recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
ids = []

for voter_folder in os.listdir(face_dir):
    path = os.path.join(face_dir, voter_folder)
    if not os.path.isdir(path): continue
    voter_id = int(voter_folder)
    for file in os.listdir(path):
        img_path = os.path.join(path, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None: continue
        faces.append(img)
        ids.append(voter_id)

recognizer.train(faces, np.array(ids))
os.makedirs('recognizer', exist_ok=True)
recognizer.write('recognizer/lbph.yml')
print("Training complete, model saved.")
