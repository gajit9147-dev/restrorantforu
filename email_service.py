"""
Email Service for Restaurant Booking Confirmations
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class EmailService:
    def __init__(self):
        # For demo purposes, we'll use a simple SMTP configuration
        # In production, use environment variables for credentials
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'restaurant@mediterraneandelight.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        
        # For development, we'll log emails to console instead of sending
        self.dev_mode = True  # Set to False in production
    
    def send_booking_confirmation(self, booking_data):
        """
        Send booking confirmation email to customer
        
        Args:
            booking_data: Dictionary containing booking information
        """
        customer_email = booking_data.get('email')
        if not customer_email:
            print("No email provided, skipping confirmation email")
            return False
        
        # Create email content
        subject = f"Booking Confirmation - Mediterranean Delight (ID: {booking_data['id']})"
        
        html_content = self._create_email_html(booking_data)
        text_content = self._create_email_text(booking_data)
        
        try:
            if self.dev_mode:
                # Development mode: Print to console
                print("\n" + "="*60)
                print("📧 EMAIL CONFIRMATION (Development Mode)")
                print("="*60)
                print(f"To: {customer_email}")
                print(f"Subject: {subject}")
                print("\n" + text_content)
                print("="*60 + "\n")
                return True
            else:
                # Production mode: Send actual email
                return self._send_smtp_email(customer_email, subject, html_content, text_content)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_email_html(self, booking_data):
        """Create HTML email content"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; }}
                .booking-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
                .detail-label {{ font-weight: bold; color: #e67e22; }}
                .booking-id {{ font-size: 24px; font-weight: bold; color: #27ae60; 
                              text-align: center; padding: 15px; background: #e8f8f5; 
                              border-radius: 8px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #7f8c8d; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🍽️ Mediterranean Delight</h1>
                    <h2>Booking Confirmation</h2>
                </div>
                
                <div class="content">
                    <p>Dear {booking_data['customer']},</p>
                    
                    <p>Thank you for choosing Mediterranean Delight! Your table reservation has been confirmed.</p>
                    
                    <div class="booking-id">
                        Booking ID: {booking_data['id']}
                    </div>
                    
                    <div class="booking-details">
                        <h3>Reservation Details:</h3>
                        <div class="detail-row">
                            <span class="detail-label">Name:</span> {booking_data['customer']}
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Date:</span> {booking_data['date']}
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Time:</span> {booking_data['time']}
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Number of Guests:</span> {booking_data['guests']}
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Table Preference:</span> {booking_data.get('table_pref', 'Any')}
                        </div>
                    </div>
                    
                    <p><strong>Please save this Booking ID:</strong> {booking_data['id']}</p>
                    <p>You can use this ID to manage your reservation or chat with our AI assistant.</p>
                    
                    <p>We look forward to serving you!</p>
                </div>
                
                <div class="footer">
                    <p>Mediterranean Delight<br>
                    123 Restaurant Street, Food City<br>
                    📞 +1 (555) 123-4567<br>
                    📧 info@mediterraneandelight.com</p>
                    
                    <p style="margin-top: 20px; font-size: 12px;">
                    If you need to cancel or modify your booking, please contact us or use our AI chat assistant on our website.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _create_email_text(self, booking_data):
        """Create plain text email content"""
        text = f"""
Mediterranean Delight - Booking Confirmation
{'='*50}

Dear {booking_data['customer']},

Thank you for choosing Mediterranean Delight! Your table reservation has been confirmed.

*** BOOKING ID: {booking_data['id']} ***

Reservation Details:
--------------------
Name: {booking_data['customer']}
Date: {booking_data['date']}
Time: {booking_data['time']}
Number of Guests: {booking_data['guests']}
Table Preference: {booking_data.get('table_pref', 'Any')}

Please save this Booking ID: {booking_data['id']}
You can use this ID to manage your reservation or chat with our AI assistant.

We look forward to serving you!

---
Mediterranean Delight
123 Restaurant Street, Food City
Phone: +1 (555) 123-4567
Email: info@mediterraneandelight.com

If you need to cancel or modify your booking, please contact us or use our AI chat assistant on our website.
        """
        return text.strip()
    
    def _send_smtp_email(self, to_email, subject, html_content, text_content):
        """Send actual email via SMTP (for production)"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = to_email
            
            # Attach both text and HTML versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

# Create singleton instance
email_service = EmailService()
