import uuid
import base64

def generate_test_id():
    """Generates a unique ID for the test"""
    try:
        unique_bytes = uuid.uuid4().bytes[:6]
        unique_str = base64.urlsafe_b64encode(unique_bytes).decode("utf-8").rstrip("=")
        return unique_str
    except Exception as e:
        raise e()
