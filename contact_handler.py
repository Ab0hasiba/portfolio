#!/usr/bin/env python3
"""
Self-contained contact form handler
Saves submissions to a local file - no external services needed
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# File to store contact submissions
CONTACT_FILE = "contact_submissions.json"

def load_submissions():
    """Load existing submissions from file"""
    if os.path.exists(CONTACT_FILE):
        try:
            with open(CONTACT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_submission(name, email, subject, message):
    """Save a new submission to file"""
    submissions = load_submissions()
    
    new_submission = {
        "id": len(submissions) + 1,
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "status": "new"
    }
    
    submissions.append(new_submission)
    
    with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2, ensure_ascii=False)
    
    return new_submission

@app.route("/send-email", methods=["POST"])
def handle_contact():
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        
        # Extract subject from message if it contains one
        lines = message.split('\n')
        subject = lines[0] if lines else "Contact Form Submission"
        message_body = '\n'.join(lines[1:]) if len(lines) > 1 else message
        
        # Basic validation
        if not name or not email or not message_body:
            return jsonify({
                "success": False, 
                "message": "Please fill in all required fields"
            })
        
        # Email validation
        if "@" not in email or "." not in email:
            return jsonify({
                "success": False, 
                "message": "Please enter a valid email address"
            })
        
        # Save submission
        submission = save_submission(name, email, subject, message_body)
        
        # Also create a readable text file for easy viewing
        create_readable_log(name, email, subject, message_body)
        
        return jsonify({
            "success": True, 
            "message": "Message received! I'll get back to you soon.",
            "submission_id": submission["id"]
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Error processing your message: {str(e)}"
        })

def create_readable_log(name, email, subject, message):
    """Create a human-readable log file"""
    log_entry = f"""
{'='*60}
NEW CONTACT FORM SUBMISSION
{'='*60}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

{'='*60}
"""
    
    with open("contact_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

@app.route("/submissions", methods=["GET"])
def get_submissions():
    """Get all contact submissions (for admin viewing)"""
    submissions = load_submissions()
    return jsonify({
        "success": True,
        "submissions": submissions,
        "count": len(submissions)
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Contact form handler is running",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🚀 Starting self-contained contact form handler...")
    print("📁 Contact submissions will be saved to:")
    print(f"   - {CONTACT_FILE} (JSON format)")
    print(f"   - contact_log.txt (Human readable)")
    print("🌐 Server running on http://localhost:5000")
    print("📧 No external email services required!")
    
    app.run(debug=True, port=5000)
