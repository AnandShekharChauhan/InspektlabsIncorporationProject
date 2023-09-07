from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Create a Limiter instance
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Your Flask routes and other app configuration
# ...

if __name__ == '__main__':
    app.run(debug=True)
