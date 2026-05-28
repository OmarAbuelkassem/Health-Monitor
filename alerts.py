import smtplib
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()


class AlertManager:
    """Handles sending notifications via Gmail and Webhooks."""

    def __init__(self, config):
        self.config = config.get("alerts", {})
        # Pulls your Gmail credentials directly from your .env
        self.email_sender = os.getenv("ALERT_EMAIL")
        self.email_password = os.getenv("ALERT_PASSWORD")

    def send_email_alert(self, subject, body):
        """Send an email alert using Gmail's SMTP server."""
        if not self.config.get("email_enabled"):
            return

        # Safety check to ensure credentials exist before trying to connect
        if not self.email_sender or not self.email_password:
            print(
                "WARNING: Email alerts are enabled, but Gmail credentials are missing in your .env file."
            )
            return

        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_sender
            msg["To"] = self.config.get("email_to")
            msg["Subject"] = subject
            msg["Date"] = formatdate(
                localtime=True
            )  # Adds a legitimate timestamp header
            msg.attach(MIMEText(body, "plain"))

            # Gmail's official SMTP settings
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrades the connection to a secure TLS tunnel
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)

            print("Alert email successfully sent via Gmail!")

        except smtplib.SMTPAuthenticationError:
            print(
                "GMAIL ERROR: Authentication failed. Please check that your App Password is correct and has no spaces."
            )
        except Exception as e:
            print(f"--- GMAIL ERROR DETAILS ---")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {e}")
            print(f"---------------------------")

    def send_webhook_alert(self, data):
        """Send a JSON payload to a configured webhook URL."""
        webhook_url = self.config.get("webhook_url")
        if not self.config.get("webhook_enabled") or not webhook_url:
            return

        try:
            response = requests.post(webhook_url, json=data, timeout=5)
            response.raise_for_status()
            print("Webhook successfully sent")
        except Exception as e:
            print(f"Webhook failed: {e}")
