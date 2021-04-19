from flask import Flask, make_response, send_from_directory

app = Flask(__name__)

@app.route('/manifest.json')
def manifest():
	return send_from_directory('static','manifest.json')
