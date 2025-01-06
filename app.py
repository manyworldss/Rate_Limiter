from flask import Flask, request
from collections import defaultdict
from datetime import datetime, timedelta
  
app = Flask(__name__)

your_request = defaultdict(list)

def clean_old_requests(ip):
    """Remove Requests older than 1 minute for given IP"""
    current_time = datetime.now()
    minute_ago = current_time - timedelta(minutes=1)
    
    your_request[ip] = [
        time for time in your_request[ip]
        if time > minute_ago    # This line was missing - it's the actual filter!
    ]

@app.route('/')
def hello():
    visitor_ip = request.remote_addr
    current_time = datetime.now()
    
    # Clean old requests first
    clean_old_requests(visitor_ip)
    
    # Add new request
    your_request[visitor_ip].append(current_time)
    
    # Fixed: use visitor_ip instead of current_time
    num_requests = len(your_request[visitor_ip])
    
    return f"Hello! Your IP {visitor_ip} has made {num_requests} requests in the last minute"

if __name__ == '__main__':
    app.run(debug=True)