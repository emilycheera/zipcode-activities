from helpers import (is_valid_zip, is_valid_participants, call_zipcode_API, 
                     call_activity_API, are_entries_valid)
from flask import Flask, jsonify, request


app = Flask(__name__)

# localhost:5000/activity?zipcode=94704&participants=3
@app.route("/activity")
def get_random_activity():
    """Given zipcode and participants, return city and random activity."""

    zipcode = request.args.get("zipcode")
    participants = request.args.get("participants")

    # Ensure zipcode and partipants are valid
    result = are_entries_valid(zipcode, participants)
    if result.get("error"):
        return jsonify(result), 400

    # Make call to zipcode API
    zip_res = call_zipcode_API(zipcode)
    if zip_res.get("error"):
        return jsonify(zip_res), 500
    else:
        city = zip_res["places"][0]["place name"]

    # Make call to activity API
    activity_res = call_activity_API(participants)
    if activity_res.get("error"):
        return jsonify(activity_res), 500
    else:
        activity = activity_res["activity"]

    return jsonify({"city": city, "activity": activity}), 200


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
