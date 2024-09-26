from flask import Flask
from app.controllers import ai_category

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', view_func=ai_category.index, methods=["GET"])
    app.add_url_rule('/check-sheet-available', view_func=ai_category.check_sheet_available, methods=["POST"])
    app.add_url_rule('/predict', view_func=ai_category.run_predict, methods=["POST"])
    return app