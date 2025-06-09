import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from flask import jsonify, request
from utils.file_utils import parse_pdf_to_text, clean_text, parse_string_to_json
from werkzeug.utils import secure_filename

def register_model_routes(app, model_client, db_pool):
    @app.route("/generate", methods=["POST"])
    def generate():
        """Generate questions and answers according to the requirements of the user"""
        try:
            # Read the file received in the request
            files = request.files.getlist('files')
            if not files or len(files) == 0:
                return jsonify( { "error": "No files selected" } ), 400
            if len(files) > 10:
                return jsonify( { "error": "Maximum 10 files allowed" } ), 400

            # Read the number of Q&A pairs to be generated
            qa_pairs_array = request.form.get('pairsArray')
            if not qa_pairs_array:
                return jsonify( { "error": "No number of Q&A specified" } ), 400
            qa_pairs_array = json.loads(qa_pairs_array)

            combined_text = ""
            parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            temp_dir = os.path.join(parent, "temp")
            os.makedirs(temp_dir, exist_ok = True)

            for i, file in enumerate(files):
                if file.filename == "":
                    continue
                if not file.filename.lower().endswith(".pdf"):
                    return jsonify( { "error": "Only .pdf files are allowed" } ), 400
                filename = secure_filename(file.filename)
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                
                try:
                    text = parse_pdf_to_text(filepath)
                    if text:
                        combined_text += f"File {i + 1}:\n" + clean_text(text) + "\n\n"
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)

            if combined_text:
                questions_and_answers = model_client.generate_qa(combined_text, qa_pairs_array)
                print(questions_and_answers)
                questions_and_answers = parse_string_to_json(questions_and_answers)
                return jsonify( { "data": questions_and_answers } ), 200
            else:
                return jsonify( { "error": "The text is empty" } ), 400
        except Exception as e:
            print(str(e))
            return jsonify(
                {
                    "error": str(e)
                }
            ), 500
