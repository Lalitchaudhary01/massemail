import streamlit as st
import smtplib
import ssl
import time
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

SMTP_SERVER = config["SMTP_SERVER"]
SMTP_PORT = config["SMTP_PORT"]
EMAIL_SENDER = config["EMAIL_SENDER"]
EMAIL_PASSWORD = config["EMAIL_PASSWORD"]
EMAIL_SUBJECT = config["EMAIL_SUBJECT"]
DELAY = config["DELAY"]  # Delay between emails in seconds

def load_html_template(file_path="template.html"):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        st.error("Error: template.html not found.")
        return ""

def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = EMAIL_SENDER
    msg["MIME-Version"] = "1.0"
    msg["Content-Type"] = "text/html; charset=UTF-8"

    msg.attach(MIMEText(message, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        return f"✅ Email sent to {to_email}"
    except Exception as e:
        return f"❌ Failed to send email to {to_email}: {e}"

st.title("📧 Bulk Email Sender")
uploaded_file = st.file_uploader("Upload a .txt file containing email addresses", type=["txt"])

if uploaded_file is not None:
    emails = [line.decode("utf-8").strip() for line in uploaded_file.readlines() if line.strip()]
    st.write(f"Found {len(emails)} email addresses.")
    
    if st.button("Send Emails"):
        html_template = load_html_template()
        if not html_template:
            st.error("Email template not found. Please upload the template.html file.")
        else:
            for email in emails:
                result = send_email(email, EMAIL_SUBJECT, html_template)
                st.write(result)
                time.sleep(DELAY)
            st.success("All emails processed.")
