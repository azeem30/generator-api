from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_analytics_routes(app, db_pool):
    @app.route("/created_tests", methods=["GET"])
    def get_created_tests():
        """Return the number of tests created by the user"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "Email not available in the request" } ), 400
            
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select count(*)
                        from tests
                        where teacher_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    tests = cursor.fetchone()
                    return jsonify( { "created_tests": int(tests["count(*)"]) } ), 200
            return jsonify( { "error": "An unexpected error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500

    @app.route("/created_questions", methods=["GET"])
    def get_created_questions():
        """Return the number of questions and answers created by the user"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "Email not available in the request" } ), 400
            
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select count(*)
                        from tests as t inner join questions_and_answers as q
                        on t.id = q.id
                        where t.teacher_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    questions_and_answers = cursor.fetchone()
                    return jsonify( { "created_questions": int(questions_and_answers["count(*)"]) } ), 200
            return jsonify( { "error": "An unexpected error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500

    @app.route("/submissions", methods=["GET"])
    def get_submissions():
        """Return the number of responses received by the user"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "Email not available in the request" } ), 400
            
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select count(*)
                        from tests as t inner join responses as r
                        on t.id = r.test_id
                        where t.teacher_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    submissions = cursor.fetchone()
                    return jsonify( { "submissions": int(submissions["count(*)"]) } ), 200
            return jsonify( { "error": "An unexpected error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500
