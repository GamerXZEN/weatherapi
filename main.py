from flask import Flask, render_template
import pandas as pd

website = Flask(__name__)

stations = pd.read_csv("stations.txt", skiprows=17)


@website.route("/")
def home():
	return render_template("index.html", data=stations.to_html())


@website.route("/v2.1/<station>/")
def station_data(station):
	data = pd.read_csv(f"stations/TG_STAID{str(station).zfill(6)}.txt",
	                   skiprows=20, parse_dates=["    DATE"])
	data = data[["STAID", "    DATE", "   TG"]]
	return render_template("station.html", data=data.to_html())


@website.route("/v2.1/<station>/year/<year>")
def year_data(station, year):
	data = pd.read_csv(f"stations/TG_STAID{str(station).zfill(6)}.txt",
	                   skiprows=20)
	data["    DATE"] = data["    DATE"].astype(str)
	data = data[["STAID", "    DATE", "   TG"]]
	result = data[data["    DATE"].str.startswith(str(year))]
	return render_template("year.html", data=data.to_html())


@website.route("/v2.1/<station>/date/<date>/")
def date_data(station, date):
	data = pd.read_csv(f"stations/TG_STAID{str(station).zfill(6)}.txt",
	                   skiprows=20, parse_dates=["    DATE"])
	temperature = data.loc[data["    DATE"] == date]["   TG"].squeeze() / 10
	if temperature == -999.9:
		temperature = "No temperature was recorded"
	web_station = f"Station: {station}"
	web_date = f"Date: {date}"
	web_temperature = f"Temperature in Celsius: {temperature}"
	return render_template("date.html", html_station=web_station, html_date = web_date, html_temp = web_temperature)


if __name__ == "__main__":
	website.run(debug=True, port=1472)
