import requests

def are_entries_valid(zipcode, num_participants):

    result = {}

    if zipcode is None or num_participants is None:
        result["error"] = "Zipcode and participants are required parameters"

    elif not is_valid_zip(zipcode):
        result["error"] = "Invalid entry for zipcode"

    elif not is_valid_participants(num_participants):
        result["error"] = "Invalid entry for participants"

    return result


def is_valid_zip(zipcode):
    """Return if a zipcode is valid."""
    
    if len(zipcode) != 5 or not zipcode.isdigit():
        return False
    return True


def is_valid_participants(num_participants):
    """Return if a number of participants is valid."""

    if not num_participants.isdigit() or not 1 <= int(num_participants) <= 5:
        return False
    return True


def call_zipcode_API(zipcode):
    """Make call to zipcode API and return response, handling errors."""

    result = {}

    zip_res = requests.get(f"http://api.zippopotam.us/us/{zipcode}")
    
    if zip_res.status_code != 200:
        result["error"] = "Could not retrieve city information"
        return result
    try:
        zip_res_dict = zip_res.json()
    except ValueError:
        result["error"] = "Could not retrieve city information"
        return result

    return zip_res_dict


def call_activity_API(num_participants):
    """Make call to activity API and return response, handling errors."""
    
    result = {}

    activity_res = requests.get("https://www.boredapi.com/api/activity?"
                               f"participants={num_participants}")

    if activity_res.status_code != 200:
        result["error"] = "Could not retrieve activity"
        return result
    try:
        activity_res_dict = activity_res.json()
    except ValueError:
        result["error"] = "Could not retrieve activity"
        return result

    return activity_res_dict


