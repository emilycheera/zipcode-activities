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