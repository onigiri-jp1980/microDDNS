import random
import string

def generate_random_string(length: int = 32) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits+'_/!@#$%^&*', k=length))