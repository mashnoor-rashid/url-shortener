from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
    # URLValidator requires "https://" to be consider valid URL.
    url_validator = URLValidator()
    invalid1 = False
    invalid2 = False
    try:
        url_validator(value)
    except:
        invalid1 = True
    value2_url = "https://" + value
    try:
        url_validator(value2_url)
    except:
        invalid2 = True
    if invalid1 == False and invalid2 == False:
        raise ValidationError("Not a valid URL")
    return value

def validate_dot_com(value):
    if not ("com" or "org" or "ca") in value:
        raise ValidationError("Not a valid URL")
    return value
