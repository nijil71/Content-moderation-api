import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    MAX_TEXT_SIZE = 5000  # 5000 characters
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Model configurations
    BATCH_SIZE = 32
    MAX_SEQUENCE_LENGTH = 512
    
    # API Rate limiting
    RATE_LIMIT_REQUESTS = 60  # requests per minute
    
    # Logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Development specific
    DEBUG = False
    TESTING = False