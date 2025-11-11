# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.auth import auth_bp
from routes.face import face_bp
from routes.vote import vote_bp

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# import models after db set
import models

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(face_bp, url_prefix='/face')
app.register_blueprint(vote_bp, url_prefix='/vote')

if __name__ == '__main__':
    app.run(debug=True)
