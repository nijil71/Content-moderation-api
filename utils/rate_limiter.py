# utils/rate_limiter.py
from functools import wraps
from flask import jsonify, request
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def limit(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            
            # Get current timestamp
            now = time.time()
            
            # Remove requests older than 1 minute
            self.requests[client_ip] = [req_time for req_time in self.requests[client_ip] 
                                      if now - req_time < 60]
            
            # Check if request limit is exceeded
            if len(self.requests[client_ip]) >= self.requests_per_minute:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            # Add current request timestamp
            self.requests[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated

# config.py


