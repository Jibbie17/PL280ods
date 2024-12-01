from flask import Flask, jsonify
from clean import load_state_agg, load_states
from flask_cors import CORS

app = Flask(__name__)




@app.route('/overview.csv')
def get_overview():
    overview = load_state_agg()
    return overview

@app.route('/states')
def get_states():
    states = load_states()
    return states

@app.route('/counties')
def get_counties():
    return jsonify()

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)