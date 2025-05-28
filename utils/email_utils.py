import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_CONFIG
from flask import url_for

def send_verification_email(email, verification_token, app):
    """Send verification email to the user using Gmail SMTP"""
    try:
        with app.app_context():
            verification_url = url_for('verify_email', token=verification_token, _external=True)
        subject = "Activate Your InsightQA Account"
        body = f"""
        <html>
            <body>
                <p>Hello,</p>
                <p>Thank you for signing up with InsightQA!</p>
                <p>Please click the button below to activate your account:</p>
                <p>
                    <a href="{verification_url}" style="
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                    ">
                        Activate Your Account
                    </a>
                </p>
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p><code>{verification_url}</code></p>
                <p>This link will expire in 24 hours.</p>
                <p>Best regards,<br>The InsightQA Team</p>
            </body>
        </html>
        """
        msg = MIMEMultipart()
        msg['From'] = MAIL_CONFIG["EMAIL_FROM"]
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        with smtplib.SMTP(MAIL_CONFIG["SMTP_SERVER"], MAIL_CONFIG["SMTP_PORT"]) as server:
            server.ehlo()
            server.starttls()
            server.login(MAIL_CONFIG["SMTP_USERNAME"], MAIL_CONFIG["SMTP_PASSWORD"])
            server.sendmail(MAIL_CONFIG["EMAIL_FROM"], email, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        app.logger.error("Failed to authenticate with Gmail SMTP server")
        return False
    except Exception as e:
        app.logger.error(f"Error sending verification email: {str(e)}")
        return False
