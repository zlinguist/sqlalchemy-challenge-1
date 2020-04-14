import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    import datetime as dt
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


if __name__ == "__main__":
    app.run(debug=True)