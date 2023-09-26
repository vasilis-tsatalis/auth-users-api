from .auth_schema import pwd_context

def verify_password(plain_password, hashed_password):
    """
    function which returns true/false compare result
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    function to generate hashed password
    """
    return pwd_context.hash(password)
