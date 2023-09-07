from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
jwt = JWTManager(app)

# Configure API rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Basic in-memory database to store uploaded image names
uploaded_images = []

# Page to upload images
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # Check if user is authenticated
        if 'Authorization' not in request.headers:
            return redirect(url_for('login_page'))
        
        # Verify the JWT token
        try:
            access_token = request.headers['Authorization'].split()[1]
            jwt.decode_token(access_token)
        except Exception as e:
            return jsonify({'message': 'Authentication error'}), 401
        
        # Handle image upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                uploaded_images.append(file.filename)
                return redirect(url_for('show_image', image_name=file.filename))
    
    return render_template('upload.html')

# Page to display uploaded image name
@app.route('/image/<image_name>')
def show_image(image_name):
    return f'Uploaded Image: {image_name}'

# Login page for JWT token generation
@app.route('/login', methods=['POST'])
def login_page():
    data = request.get_json()
    if data.get('username') == 'your_username' and data.get('password') == 'your_password':
        access_token = create_access_token(identity=data.get('username'))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
