import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# CORS: allow only your portfolio domain
CORS(app, resources={r"/*": {"origins": os.getenv("ALLOWED_ORIGIN", "*")}})

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        recipient = os.getenv("RECIPIENT_EMAIL", sender)

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = f"New Contact from {name}"
        msg.attach(MIMEText(f"From: {name} <{email}>\n\n{message}", "plain"))

        # Send via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        return jsonify({"success": True, "message": "Email sent!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
