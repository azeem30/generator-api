from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_profile_routes(app, db_pool):
    @app.route("/update_user/<string:email>", methods=["PUT"])
    def update_user(email):
        """Update the Profile Details of the User"""
        try:
            data = request.get_json()
            if not data:
                return jsonify( { "error": "No data received in the request" } ), 400
            new_email = data["email"]
            name = data["name"]
            department = data["department"]
            allowed_departments = ["Computer Science", "Information Technology", "Mechanical", "Electrical", "Electronics and Telecommunication"]
            if department not in allowed_departments:
                return jsonify( { "error": "The department should be one of the following: Computer Science, Information Technology, Mechanical, Electrical, Electronics and Telecommunication" } ), 400
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        update teachers
                        set email = %s, name = %s, dept_name = %s
                        where email = %s
                    """
                    data = (new_email, name, department, email)
                    cursor.execute(query, data)
                    connection.commit()
                    return jsonify( { "message": "Profile updated successfully" } ), 200
            return jsonify( { "error": "An unexpected error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500
