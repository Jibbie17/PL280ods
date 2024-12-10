from flask import Flask, jsonify, request
from flask_cors import CORS
import polars as pl
from clean import load_state_agg, load_states, load_counties

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/overview.csv')
def get_overview():
    """
    This call returns aggregated state-level data. All 36 mapped states 
    are included. Death rates are averaged accross years. 
    Returns: CSV
    """
    overview = load_state_agg()
    return overview

@app.route('/max')
def get_max():
    """
    This call return the max death rate in the county level data.
    It returns it as a string object.
    Returns: String
    """
    counties = load_counties()
    max = counties.select(pl.max("drd_AIAN_p100k"))
    max_int = max.item()
    return str(max_int)

@app.route('/quantile-states')
def get_quantile_states():
    """
    This call taxes the argument 'quantile' and returns the specified quantile
    of AIAN drug-related death rates from the state-level data.
    Returns: JSON
    """
    quant = float(request.args.get('quantile'))
    states = load_states()
    q_num = states["drd_AIAN_p100k"].quantile(quant)
    return jsonify({"quantile" : str(q_num)})

@app.route('/quantile-counties')
def get_quantile_counties():
    """
    This call taxes the argument 'quantile' and returns the specified quantile
    of AIAN drug-related death rates from the county-level data.
    Returns: JSON
    """
    quant = float(request.args.get('quantile'))
    counties = load_counties()
    q_num = counties["drd_AIAN_p100k"].quantile(quant)
    return jsonify({"quantile" : str(q_num)})

@app.route('/all-states')
def get_states():
    """
    This call taxes the argument 'year' and returns the state-level data
    for the year requested.
    Returns: CSV
    """
    year = int(request.args.get('year'))
    states = load_states()
    states = states.filter(pl.col("Year") == year)
    states = states.write_csv()
    return states

@app.route('/counties')
def get_counties():
    """
    This call taxes the argument 'year' and 'id; returns the county-level data
    for the year and state requested. 'id' refers to the state FIPS code.
    Returns: CSV
    """
    id = int(request.args.get('id'))
    year = int(request.args.get('year'))
    counties = load_counties()
    counties = counties.filter(pl.col("STATEFP") == id
                               ).filter(pl.col("Year") == year)

    return counties.write_csv()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)