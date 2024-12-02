from flask import Flask, jsonify, request
from flask_cors import CORS
import polars as pl
from clean import load_state_agg, load_states, load_counties

app = Flask(__name__)


@app.route('/overview.csv')
def get_overview():
    overview = load_state_agg()
    return overview

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
    counties = load_counties()
    counties = counties.filter(pl.col("STATEFP")==id).with_columns(
        pl.col("County.Code").alias("FIPS")
    )

    return counties.write_csv()

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)