import traceroute
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/traceroute')
def default_traceroute():
    geoip = traceroute.main('google.com')
    return jsonify(geoip)

@app.route('/traceroute', methods=['POST'])
def user_traceroute():
    if not request.json:
        abort(400); # bad request
    remote_server = request.json.get('remote-server')
    geoip = traceroute.main(remote_server)
    return jsonify(geoip)

app.run(debug=True)
