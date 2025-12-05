import logging
from app.core.config import settings

# In a real app, use fastapi-mail or boto3 SES here.
# Currently mocking to print to console like development mode.

def send_email(to: str, subject: str, text: str):
    logging.info(f"--- EMAIL SENT ---")
    logging.info(f"To: {to}")
    logging.info(f"Subject: {subject}")
    logging.info(f"Content: {text}")
    logging.info(f"------------------")

def send_reset_password_email(to: str, token: str):
    subject = "Reset password"
    # Replace logic with your frontend URL
    reset_url = f"http://localhost:3000/reset-password?token={token}"
    text = f"Dear user,\nTo reset your password, click on this link: {reset_url}\nIf you did not request any password resets, then ignore this email."
    send_email(to, subject, text)

def send_verification_email(to: str, token: str):
    subject = "Email Verification"
    verify_url = f"http://localhost:3000/verify-email?token={token}"
    text = f"Dear user,\nTo verify your email, click on this link: {verify_url}\nIf you did not create an account, then ignore this email."
    send_email(to, subject, text)