
import random
import string as string_lib

UNICODE_ASCII_CHARACTER_SET = string_lib.ascii_letters + string_lib.digits
DEFAULT_LENGTH = 32


def generate_random_str(length=DEFAULT_LENGTH, chars=UNICODE_ASCII_CHARACTER_SET):
    return ''.join(random.choices(chars, k=length))
