from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configure your email
EMAIL_ADDRESS = "ahmedtube2005@gmail.com"
EMAIL_PASSWORD = "faea izki eqpq jgyt"

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.form
    sender_name = data.get("name")
    sender_email = data.get("email")
    message_content = data.get("message")

    # Create email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS  # send to yourself
    msg["Subject"] = f"Portfolio Contact Form - {sender_name}"

    body = f"From: {sender_name} <{sender_email}>\n\nMessage:\n{message_content}"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

        return jsonify({"status": "success", "message": "Email sent!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
