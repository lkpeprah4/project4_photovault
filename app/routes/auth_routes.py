from flask import Blueprint, request, jsonify
from ..models import User
from .. import db, bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")
    username=data.get("username")

    if not username or not password or not email:
        return jsonify({"msg":"ALL FIELDS ARE REQUIRED"}),400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg":"USER ALREADY EXISTS"}),400
    
    hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
    new_user=User(
        username= username,
        email=email,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201