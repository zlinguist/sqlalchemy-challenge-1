import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)



@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/START<br/>"
        f"/api/v1.0/START/END"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_object = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    query_date = last_date_object - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date)

    session.close()

    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurement.station).\
        group_by(Measurement.station).all()

    session.close()

    stations = []

    for station in results:
        stations.append(station)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_object = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    query_date = last_date_object - dt.timedelta(days=365)

    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()[0][0]

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(Measurement.date >= query_date)

    session.close()

    tobs_all = []
    for date, temp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = temp
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)


@app_route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    start_only = []
    for minimum, average, maximum in results:
        start_dict = {}
        start_dict["TMIN"] = minimum
        start_dict["TAVG"] = average
        start_dict["TMAX"] = maximum
        start_only.append(start_dict)

    return jsonify(start_only)


@app_route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_end = []
    for minimum, average, maximum in results:
        start_dict = {}
        start_dict["TMIN"] = minimum
        start_dict["TAVG"] = average
        start_dict["TMAX"] = maximum
        start_end.append(start_dict)

    return jsonify(start_end)


if __name__ == "__main__":
    app.run(debug=True)