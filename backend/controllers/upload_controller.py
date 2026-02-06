from flask import Blueprint, request, jsonify, render_template
from backend.services.upload_service import upload_file_to_cloud
upload_blueprint = Blueprint('upload', __name__) #blueprint for upload routes


@upload_blueprint.route("/upload", methods=["GET", "POST"])
def upload_file():
        if request.method=="POST":
                file = request.files['csv_file']
                upload_file_to_cloud(file)
                
        return render_template('upload.html')


        