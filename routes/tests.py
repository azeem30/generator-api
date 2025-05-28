import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import jsonify, request
from utils.db_utils import get_db_connection
from utils.test_utils import generate_test_id

def register_test_routes(app, db_pool):
    @app.route("/save_test", methods=["POST"])
    def save_test():
        """Save the test and its metadata in the database"""
        try:
            # Validation of data received in the request
            data = request.get_json()
            if not data:
               return jsonify( { "error": "No data provided" } ), 400
            test = data["test"]
            if not all( key in test for key in  ( "title", "subject", "pairs", "marks", "difficulty", "date", "teacher_email" ) ):
               return jsonify( { "error": "Missing required fields" } ), 400
            if not data["questions_and_answers"]:
               return jsonify( { "error": "No questions and answers provided" } ), 400
            
            questions_and_answers = data["questions_and_answers"]
            id = generate_test_id()
            title = test["title"]
            subject = test["subject"]
            marks = test["marks"]
            pairs = test["pairs"]
            difficulty = test["difficulty"]
            scheduled_at = test["date"]
            teacher_email = test["teacher_email"]
            
            if difficulty not in [ "easy", "medium", "hard" ]:
                return jsonify( { "error": "Invalid difficulty" } ), 400
            if not teacher_email:
                return jsonify( { "error": "No credentials found in the request" } ), 400

            # Save the test and the questions and answers in the database
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = "insert into tests (id, title, subject, marks, difficulty, scheduled_at, teacher_email, pairs) values (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (id, title, subject, marks, difficulty, scheduled_at, teacher_email, pairs)
                    cursor.execute(query, data)
                    connection.commit()
            
                    query = "insert into questions_and_answers (id, question, answer) values (%s, %s, %s)"
                    for item in questions_and_answers:
                       question = item["Q"]
                       answer = item["A"]
                       data = (id, question, answer)
                       cursor.execute(query, data)
                    connection.commit()
                    return jsonify( { "message": "Test saved successfully" } ), 200

            return jsonify( { "error": "Failed to save test" } ), 400
        except Exception as e:
            print(str(e))
            return jsonify( { "error": str(e) } ), 500
