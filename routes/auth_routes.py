from flask import Blueprint, request, jsonify, current_app
from extensions import db, mail
from models.user import User
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from utils.decorators import admin_required

auth_bp = Blueprint("auth", __name__)

# Admin: list all users
@auth_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.filter_by(role='user').all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'is_verified': u.is_verified
        }
        for u in users
    ])


verification_message ="Hello  {user_email},\n\nPlease click the link below to verify your email address:\n\n{confirm_url}\n\nIf you did not create an account, please ignore this email.\n\nThank you! \nRental Management System Team"

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["JWT_SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirm")


def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    confirm_url = f" https://overdramatically-flashier-zofia.ngrok-free.dev/auth/verify/{token}"

    msg = Message("Confirm Your Email - Rental Management System", recipients=[user_email])
    msg.body = verification_message.format(user_email=user_email, confirm_url=confirm_url)

    mail.send(msg)


@auth_bp.route("/verify/<token>")
def verify_email(token):
    serializer = URLSafeTimedSerializer(current_app.config["JWT_SECRET_KEY"])

    try:
        email = serializer.loads(token, salt="email-confirm", max_age=3600)
    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_verified = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully!"})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(
        name=data["name"],
        email=data["email"],
        role=data.get("role", "user")
    )

    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    send_verification_email(new_user.email)

    return jsonify({"message": "Verification email sent. Please check your inbox."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_verified:
        return jsonify({"error": "Email not verified. Please check your inbox."}), 403

    access_token = create_access_token(
        identity=str(user.id),   # must be string
        additional_claims={
            "role":  user.role,
            "name":  user.name,
            "email": user.email
        }
    )

    return jsonify({"access_token": access_token})
