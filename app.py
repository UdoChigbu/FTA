from flask import Flask, jsonify, render_template
from backend.controllers.upload_controller import upload_blueprint #imports ALL routes from upload controller
app = Flask(__name__)

app.register_blueprint(upload_blueprint) #registers all the routes from the upload controller

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)