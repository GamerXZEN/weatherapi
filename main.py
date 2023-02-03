from flask import Flask, render_template

website = Flask(__name__)


@website.route("/")
def home():
	return render_template("index.html")


@website.route("v1.2/<station>/<date>")
def web_data(station, date):
	temperature = 23
	return {"station": station,
	        "date": date,
	        "temperature": temperature}


website.run(debug=True)
