import os
import sqlalchemy
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, render_template



app = Flask(__name__)


app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/happinessData.sqlite"
db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine,reflect=True)

happinessAll = Base.classes.happiness

Countries = Base.classes.Country

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/map")
def mapembed():
    return render_template("map.html")

@app.route("/2018")
def embed():
    return render_template("2018.html")

@app.route("/years")
def years():
	return jsonify(['2015','2016','2017'])



@app.route("/<year>")
def countries_happiness_year(year):

	year_sel = [
		happinessAll.Country_id,
		happinessAll.Country,
		happinessAll.Rank,
		happinessAll.Score,
		happinessAll.Economy,
		happinessAll.Family,
		happinessAll.Health,
		happinessAll.Freedom,
		happinessAll.Trust,
		happinessAll.Generosity,
		happinessAll.DystopiaResidual,
		happinessAll.Code,
		happinessAll.Year
	]

	year_results = db.session.query(*year_sel).filter(happinessAll.Year == year).all()


	happiness_year_data_list = []
	for result in year_results:
		happiness_year_data = {}
		happiness_year_data['Country']= result[1]
		happiness_year_data['Code'] = result[11]
		happiness_year_data['Country_id'] = result[0]
		happiness_year_data['Rank'] = result[2]
		happiness_year_data['Score'] = result[3]
		happiness_year_data['Economy'] = result[4]
		happiness_year_data['Family'] = result[5]
		happiness_year_data['Health'] = result[6]
		happiness_year_data['Freedom'] = result[7]
		happiness_year_data['Trust'] = result[8]
		happiness_year_data['Generosity'] = result[9]
		happiness_year_data['DystopiaResidual'] = result[10]
		happiness_year_data_list.append(happiness_year_data)
	
	
	return jsonify(happiness_year_data_list)

	

@app.route("/countries")
def countries():
	countries_sel = [Countries.Country,Countries.Code]
	countries_results = db.session.query(*countries_sel).all()

	countries_name = {}

	for result in countries_results:
		countries_name[result[0]] = result[1]

	return jsonify([countries_name])



@app.route("/<year>/<country>")
def countries_happiness(year,country):

	sel = [
		happinessAll.Country_id,
		happinessAll.Country,
		happinessAll.Rank,
		happinessAll.Score,
		happinessAll.Economy,
		happinessAll.Family,
		happinessAll.Health,
		happinessAll.Freedom,
		happinessAll.Trust,
		happinessAll.Generosity,
		happinessAll.DystopiaResidual,
		happinessAll.Code,
		
	]

	results = db.session.query(*sel).filter(happinessAll.Year == year).filter(happinessAll.Country == country).all()

	happiness_data = {}
	for result in results:
		happiness_data['Year'] = year
		happiness_data['Country_id'] = result[0]
		happiness_data['Country'] = result[1]
		happiness_data['Code'] = result[11]
		happiness_data['Rank'] = result[2]
		happiness_data['Score'] = result[3]
		happiness_data['Economy'] = result[4]
		happiness_data['Family'] = result[5]
		happiness_data['Health'] = result[6]
		happiness_data['Freedom'] = result[7]
		happiness_data['Trust'] = result[8]
		happiness_data['Generosity'] = result[9]
		happiness_data['DystopiaResidual'] = result[10]
		
	return jsonify(happiness_data)


if __name__ =="__main__":
	app.run(debug = True)