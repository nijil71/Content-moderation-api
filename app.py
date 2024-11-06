# app.py
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import jwt
from models.text_moderation import TextModerator
from models.image_moderation import ImageModerator
from models.video_moderation import VideoModerator
from utils.rate_limiter import RateLimiter
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/moderation_api.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Content Moderation API startup')

# Initialize moderators
text_moderator = TextModerator()
image_moderator = ImageModerator()
video_moderator = VideoModerator()
rate_limiter = RateLimiter()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

def validate_content_size(content, max_size):
    """Validate content size"""
    if len(content) > max_size:
        raise ValueError(f"Content exceeds maximum size of {max_size} bytes")
    
users = {
    "test_user": generate_password_hash("test_password")
}

@app.route('/api/auth/token', methods=['POST'])
def get_token():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generate token
    token = jwt.encode({
        'user': username,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

@app.route('/api/auth/test', methods=['GET'])
@token_required
def test_auth():
    return jsonify({'message': 'Authentication successful!'})
@app.route('/api/moderate/text', methods=['POST'])
@token_required
@rate_limiter.limit
def moderate_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        validate_content_size(data['text'], app.config['MAX_TEXT_SIZE'])
        
        result = text_moderator.analyze(data['text'])
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f'Error in text moderation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/moderate/image', methods=['POST'])
@token_required
@rate_limiter.limit
def moderate_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        if not image.filename:
            return jsonify({'error': 'No image selected'}), 400
        
        filename = secure_filename(image.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(temp_path)
        
        result = image_moderator.analyze(temp_path)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f'Error in image moderation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/moderate/video', methods=['POST'])
@token_required
@rate_limiter.limit
def moderate_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video provided'}), 400
        
        video = request.files['video']
        if not video.filename:
            return jsonify({'error': 'No video selected'}), 400
        
        filename = secure_filename(video.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(temp_path)
        
        result = video_moderator.analyze(temp_path)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f'Error in video moderation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)