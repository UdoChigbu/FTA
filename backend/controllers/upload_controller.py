from flask import Blueprint, request
from backend.services.upload_service import upload_file_to_cloud
upload_blueprint = Blueprint('upload', __name__) #blueprint for upload routes


@upload_blueprint.route("/upload", methods=["POST"])
def upload_file():
        file = request.files['csv_file']
        upload_file_to_cloud(file)
        return "File uploaded successfully"
       