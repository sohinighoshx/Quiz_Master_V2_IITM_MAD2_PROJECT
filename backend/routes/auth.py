from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from json import dumps

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        email=data['email'],
        password=hashed_pw,
        full_name=data['full_name'],
        qualification=data['qualification'],
        dob=data['dob'],
        role="user"
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Registration successful"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity=dumps({"id": user.id, "role": user.role}),
            expires_delta=timedelta(hours=2)
        )
        return jsonify(access_token=access_token, role=user.role), 200

    return jsonify({"msg": "Invalid credentials"}), 401
