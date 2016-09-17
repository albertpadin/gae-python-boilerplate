import random
import string


def generate_random_string(length=12):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
        

def convert_to_string_properly(raw):
    try:
        return str(raw)
    except UnicodeEncodeError:
        return raw.encode('utf-8')


def normalize_email(email):
    return email.lower().strip()
    