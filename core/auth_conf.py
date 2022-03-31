
jwt_skip_rules = [
    # method, endpoint
    ("POST", '/api/auth/login'),
    ("POST", '/api/register_user/login'),
    ("PUT", '/api/auth/login'),
    ("POST", '/api/register_user/register'),
]