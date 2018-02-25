import random
import string
from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)

def code_gen(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Take in instane of the model (MashURL)
def create_shortcode(instane, size=SHORTCODE_MIN):
    new_code = code_gen(size=size)
    # Check to make sure this code doesn't already exist
    MashURL_class = instane.__class__
    qs_exists = MashURL_class.objects.filter(shortcode=new_code).exists()
    if qs_exists:
        return create_shortcode(size=size)
    return new_code
