from helpers import is_valid_zip, is_valid_participants
from flask import Flask, jsonify, request
import requests


app = Flask(__name__)

# localhost:5000/activity?zipcode=94704&participants=3
@app.route("/activity")
def get_random_activity():
    """Given zipcode and participants, return city and random activity."""

    zipcode = request.args.get("zipcode")
    participants = request.args.get("participants")

    result = {}

    # Ensure zipcode and partipants are valid
    if zipcode is None or participants is None:
        result["error"] = "Zipcode and participants are required parameters"
        return jsonify(result), 400

    if not is_valid_zip(zipcode):
        result["error"] = "Invalid entry for zipcode"
        return jsonify(result), 400

    if not is_valid_participants(participants):
        result["error"] = "Invalid entry for participants"
        return jsonify(result), 400

    # Make call to zipcode API
    zip_res = requests.get(f"http://api.zippopotam.us/us/{zipcode}")
    
    if zip_res.status_code != 200:
        result["error"] = "Could not retrieve city information"
        return jsonify(result), 500
    try:
        zip_res_dict = zip_res.json()
    except ValueError:
        result["error"] = "Could not retrieve city information"
        return jsonify(result), 500

    city = zip_res_dict["places"][0]["place name"]

    # Make call to activity API
    activity_res = requests.get("https://www.boredapi.com/api/activity?"
                               f"participants={participants}")

    if activity_res.status_code != 200:
        result["error"] = "Could not retrieve activity"
        return jsonify(result), 500
    try:
        activity_res_dict = activity_res.json()
    except ValueError:
        result["error"] = "Could not retrieve activity"
        return jsonify(result), 500

    activity = activity_res_dict["activity"]

    result["city"]= city
    result["activity"] = activity
    return jsonify(result), 200


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
