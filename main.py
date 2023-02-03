from flask import Flask, render_template
import pandas as pd

website = Flask(__name__)


@website.route("/")
def home():
	return render_template("index.html")


@website.route("/v1.2/<station>/<date>/")
def web_data(station, date):
	data = pd.read_csv(f"stations/TG_STAID{str(station).zfill(6)}.txt", skiprows=20, parse_dates=["    DATE"])
	temperature = data.loc[data["    DATE"] == date]["   TG"].squeeze() / 10
	if temperature == -999.9:
		temperature = "No temperature was recorded"
	return {"stations": station,
	        "date": date,
	        "temperature": temperature}

if __name__ == "__main__":
	website.run(debug=True, port=1472)
