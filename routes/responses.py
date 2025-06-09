from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_response_routes(app, db_pool):
    @app.route("/responses", methods=["GET"])
    def get_responses():
        """Fetch all the available responses for the user"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "No email in the request" } ), 400
            
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    # Query the Test Details and the Response Details
                    query = f"""
                        select
                        t.id as test_id,
                        t.title,
                        t.subject,
                        t.marks as total_marks,
                        t.difficulty,
                        t.scheduled_at,
                        t.pairs,
                        t.duration,
                        r.id as response_id,
                        r.student_email,
                        r.marks_obtained,
                        r.submitted_at
                        from tests as t inner join responses as r
                        on t.id = r.test_id
                        where t.teacher_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    results = cursor.fetchall()

                    # Query the Questions and Answers in the Response along with the Student Details
                    for result in results:
                        query = f"""
                            select
                            question,
                            sample_answer,
                            user_answer,
                            similarity,
                            marks
                            from response_data
                            where response_id = %s
                        """
                        data = (result["response_id"], )
                        cursor.execute(query, data)
                        result["questions_and_answers"] = cursor.fetchall()
                        
                        query = f"""
                            select name
                            from students
                            where email = %s
                        """
                        data = (result["student_email"], )
                        cursor.execute(query, data)
                        name = cursor.fetchone()
                        result["name"] = name["name"]

                    return jsonify( { "responses": results } ), 200
            return jsonify( { "error": "An unexpected error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500
