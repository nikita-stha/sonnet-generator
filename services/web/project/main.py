# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session

from project import inference

app = Flask(__name__)

app.secret_key = os.urandom(64)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = f"{os.getenv('APP_FOLDER')}/project/static"

app.config["UPLOAD_FOLDER"] = f"{os.getenv('APP_FOLDER')}/project/static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024


# set up the routes and logic for the webserver
@app.route("/")
def home():
    return render_template('writer_home.html', generated=None)


@app.route("/", methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route('/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('Write-your-story-with-AI.html', generated=data)
    else:
        return render_template('Write-your-story-with-AI.html', generated=None)


@app.route('/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    if prompt is not None:
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_length":300, "top_p":0.95, "temperature":1.9, "repetition_penalty":1.5}
        }
        response = inference.query(payload)
        print(response)
    
    if 'error' in response:
        session['error'] = response['error']
    else:
        session['data'] = response[0]["generated_text"]
    return redirect(url_for('results'))
