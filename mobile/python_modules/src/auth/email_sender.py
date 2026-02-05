"""
Email Utility for OTP and Verification
Note: For production, configure SMTP settings in config.yaml
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from src.utils import logger, config


class EmailSender:
    """Send emails for OTP and verification"""
    
    def __init__(self):
        self.logger = logger
        # Get email configuration from config
        self.smtp_server = config.get('email.smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('email.smtp_port', 587)
        self.sender_email = config.get('email.sender_email', '')
        self.sender_password = config.get('email.sender_password', '')
        self.enabled = config.get('email.enabled', False)
    
    def send_otp(self, recipient_email: str, otp_code: str) -> bool:
        """
        Send OTP code to user email
        
        Args:
            recipient_email: Recipient email address
            otp_code: 6-digit OTP code
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            self.logger.info(f"Email disabled. OTP for {recipient_email}: {otp_code}")
            return True  # Return True for testing without email
        
        subject = "AstroKnowledge - Your Login OTP"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #8B0000;">🔮 AstroKnowledge</h2>
                <p>Hello,</p>
                <p>Your One-Time Password (OTP) for login is:</p>
                <div style="background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #8B0000; margin: 20px 0;">
                    {otp_code}
                </div>
                <p>This OTP is valid for <strong>5 minutes</strong>.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <p style="color: #666; font-size: 12px;">
                    AstroKnowledge - Vedic Astrology & Horoscope Analysis<br>
                    This is an automated email, please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, body)
    
    def send_verification_email(self, recipient_email: str, verification_link: str) -> bool:
        """
        Send email verification link
        
        Args:
            recipient_email: Recipient email address
            verification_link: Verification link URL
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            self.logger.info(f"Email disabled. Verification link: {verification_link}")
            return True
        
        subject = "AstroKnowledge - Verify Your Email"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #8B0000;">🔮 KundaliSaga !</h2>
                <p>Hello,</p>
                <p>Thank you for registering with AstroKnowledge. Please verify your email address by clicking the link below:</p>
                <div style="margin: 30px 0; text-align: center;">
                    <a href="{verification_link}" style="background-color: #8B0000; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{verification_link}</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <p style="color: #666; font-size: 12px;">
                    AstroKnowledge - Vedic Astrology & Horoscope Analysis<br>
                    This is an automated email, please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, body)
    
    def _send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Send email via SMTP
        
        Args:
            recipient: Recipient email
            subject: Email subject
            body: Email body (HTML)
        
        Returns:
            True if sent successfully
        """
        if not self.sender_email or not self.sender_password:
            self.logger.warning("Email credentials not configured")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = recipient
            message['Subject'] = subject
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            self.logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient}: {e}")
            return False
