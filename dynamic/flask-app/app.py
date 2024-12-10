from flask import Flask, jsonify, request
from flask_cors import CORS
import polars as pl
from clean import load_state_agg, load_states, load_counties

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/overview.csv')
def get_overview():
    overview = load_state_agg()
    return overview

@app.route('/max')
def get_max():
    counties = load_counties()
    max = counties.select(pl.max("drd_AIAN_p100k"))
    max_int = max.item()
    return str(max_int)

@app.route('/quantile-states')
def get_quantile_states():
    quant = float(request.args.get('quantile'))
    states = load_states()
    q_num = states["drd_AIAN_p100k"].quantile(quant)
    return jsonify({"quantile" : str(q_num)})

@app.route('/quantile-counties')
def get_quantile_counties():
    quant = float(request.args.get('quantile'))
    counties = load_counties()
    q_num = counties["drd_AIAN_p100k"].quantile(quant)
    return jsonify({"quantile" : str(q_num)})

@app.route('/all-states')
def get_states():
    year = int(request.args.get('year'))
    states = load_states()
    states = states.filter(pl.col("Year") == year)
    states = states.write_csv()
    return states

@app.route('/counties')
def get_counties():
    id = int(request.args.get('id'))
    year = int(request.args.get('year'))
    counties = load_counties()
    counties = counties.filter(pl.col("STATEFP") == id
                               ).filter(pl.col("Year") == year)

    return counties.write_csv()

if __name__ == '__main__':
    # need to pass an IP and a port
    app.run(host="0.0.0.0", port=8080)