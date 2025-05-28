import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import jsonify, request
import uuid
from datetime import datetime, timedelta
from utils.db_utils import get_db_connection
from utils.email_utils import send_verification_email
from utils.crypt_utils import encrypt, decrypt

def register_auth_routes(app, db_pool):
    @app.route("/signup", methods=["POST"])
    def signup():
        """Register the teacher/user to InsightQA Platform"""
        try:
            # Validation of data received in the request
            data = request.get_json()
            if not data:
                return jsonify( { "error": "No data provided" } ), 400
            if not all(key in data for key in ("email", "password", "name", "department")):
                return jsonify( { "error": "Missing required fields" } ), 400
            email = data["email"]
            password = data["password"]
            name = data["name"]
            dept_name = data["department"]
            verification_token = str(uuid.uuid4())
            token_expiration = datetime.now() + timedelta(hours = 24)

            # Interaction of API with the database.
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    # Check if the email already exists in the database.
                    cursor.execute("select * from teachers where email = %s", (email, ))
                    if cursor.fetchone():
                        return jsonify( { "error": "User with this email already exists" } ), 400
                    
                    # Insert user into the database.
                    query = "insert into teachers (email, name, password, dept_name, verification_token, token_expiration) values (%s, %s, %s, %s, %s, %s)"
                    user_details = (email, name, encrypt(password), dept_name, verification_token, token_expiration)
                    cursor.execute(query, user_details)
                    connection.commit()
                    if not send_verification_email(email, verification_token, app):
                        return jsonify( { "error": "Failed to send verification mail" } ), 500
            return jsonify(
                {
                    "message": "User registered successfuly, Please check your email to activate your account"
                }
            ), 200
        except Exception as e:
            return jsonify(
                {
                    "error": str(e)    
                }
            ), 500

    @app.route("/verify-email/<token>", methods=["GET"])
    def verify_email(token):
        """Verify the user using the verification token"""
        try:
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    # Check if the user with the verification token exists
                    cursor.execute("select email from teachers where verification_token = %s and token_expiration > %s", (token, datetime.now()))
                    user = cursor.fetchone()
                    if not user:
                        return jsonify( { "error": "Invalid or expired verification token" } ), 400
                    # Update the verification status of the user in the database
                    query = "update teachers set is_verified = 1, verification_token = NULL, token_expiration = NULL where verification_token = %s"
                    data = (token, )
                    cursor.execute(query, data)
                    connection.commit()
            return jsonify( { "message": "Email verified successfully. Your account has now been activated." } ), 200
        except Exception as e:
            return jsonify(
                {
                    "error": str(e)
                }
            ), 500

    @app.route("/login", methods=["POST"])
    def login():
        """Authenticate the user and return the data"""
        try:
            data = request.get_json()
            if not data:
                return jsonify( { "error": "No data provided" } ), 400
            if not all(key in data for key in ("email", "password")):
                return jsonify( { "error": "Missing email or password" } ), 400
            email = data["email"]
            password = data["password"]
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = "select * from teachers where email = %s"
                    data = (email, )
                    cursor.execute(query, data)
                    teacher = cursor.fetchone()
                    if not teacher:
                        return jsonify( { "error": "Invalid email or password" } ), 400
                    if not teacher["is_verified"]:
                        return jsonify( { "error": "Your account is not verified" } ), 400
                    decrypted_password = decrypt(teacher["password"])
                    if password != decrypted_password:
                        return jsonify( { "error": "Incorrect password" } ), 400
                    teacher_details = {
                            "email": teacher["email"],
                            "name": teacher["name"],
                            "dept_name": teacher["dept_name"],
                    }
                    return jsonify(
                        {
                            "message": "Login successful",
                            "teacher": teacher_details
                        }
                    ), 200
            return jsonify( { "error": "Bad Request" } ), 400
        except Exception as e:
            return jsonify(
                 {
                     "error": str(e)
                 }
            ), 500
