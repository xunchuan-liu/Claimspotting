from flask import Flask
from flask_cors import CORS
import requests
from datetime import datetime
from Run_Script import Scraping

app = Flask(__name__)
CORS(app)

@app.route("/claimspotting", methods=["GET", "POST"])
def pushJSON():
	json = Scraping(datetime(2020, 3, 5))	
	return json

app.run(debug=True)