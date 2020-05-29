from flask import Flask, jsonify, request
import requests


app = Flask(__name__)


# localhost:5000/?zipcode=94704&participants=3
@app.route("/")
def get_random_activity():
    """Given zipcode and participants, return city and random activity."""

    zipcode = request.args.get("zipcode")
    participants = request.args.get("participants")

    result = {}

    # Ensure zipcode is a 5-digit number
    if len(zipcode) != 5 or not zipcode.isdigit():
        result["error"] = "Invalid entry for zipcode"
        return jsonify(result), 400

    # Ensure participants is a number from 1 to 5
    if not participants.isdigit() or not 1 <= int(participants) <= 5:
        result["error"] = "Invalid entry for participants"
        return jsonify(result), 400

    # Make call to zipcode API
    zip_res = requests.get(f"http://api.zippopotam.us/us/{zipcode}")
    zip_res_dict = zip_res.json()

    # Ensure that zipcode API call returned a valid response
    if len(zip_res_dict) == 0:
        result["error"] = "Invalid entry for zipcode"
        return jsonify(result), 400

    city = zip_res_dict["places"][0]["place name"]

    # Make call to activity API
    activity_res = requests.get("https://www.boredapi.com/api/activity?"
                               f"participants={participants}")
    activity_res_dict = activity_res.json()
    activity = activity_res_dict["activity"]

    result["city"]= city
    result["activity"] = activity

    return jsonify(result), 200


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
