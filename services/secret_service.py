import secrets
import string

class SecretService:
    @staticmethod
    def generate_secret(length=32):
        alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def validate_secret(existing_secret, provided_secret):
        if existing_secret is None or existing_secret == "":
            return False
            
        return existing_secret == provided_secret