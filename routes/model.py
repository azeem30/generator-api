import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import jsonify, request
from utils.file_utils import parse_pdf_to_text, clean_text, parse_string_to_json
from werkzeug.utils import secure_filename

def register_model_routes(app, model_client, db_pool):
    @app.route("/generate", methods=["POST"])
    def generate():
        """Generate questions and answers according to the requirements of the user"""
        try:
            # Read the file received in the request
            if request.content_type != "application/pdf":
                return jsonify( { "error": "Content-Type must be application/pdf" } ), 400
            file_data = request.get_data()
            if not file_data:
                return jsonify( { "error": "No file data received" } ), 400
            filename = request.headers.get("X-File-Name", "uploaded_file.pdf")
            filename = secure_filename(filename)
            parent = (os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
            temp_path = os.path.join(parent + "/temp", filename)
            with open(temp_path, "wb") as file:
                file.write(file_data)
            text = parse_pdf_to_text(temp_path)
            os.remove(temp_path)

            # Read the number of Q&A pairs to be generated
            qa_count = request.headers.get("X-QA-Pairs", "1")
            qa_count = int(qa_count)
            if qa_count < 1 or qa_count > 20:
                return jsonify( { "error": "Q&A pairs should be more than 1 or less than 20" } ), 400

            # Perform preprocessing on the extracted text
            if text:
                text = clean_text(text)
                questions_and_answers = model_client.generate_qa(text, qa_count)
                questions_and_answers = parse_string_to_json(questions_and_answers)
                return jsonify( { "data": questions_and_answers } ), 200
            else:
                return jsonify( { "error": "The text is empty" } ), 400
        except Exception as e:
            return jsonify(
                {
                    "error": str(e)
                }
            ), 500
