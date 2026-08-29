from flask_jwt_extended import get_jwt_identity
from json import loads

def admin_only():
    identity =loads(get_jwt_identity())
    
    print("🪪 identity from JWT:", identity, type(identity))  # Debug line

    if isinstance(identity, dict):
        return identity.get("role") == "admin"
    return False
