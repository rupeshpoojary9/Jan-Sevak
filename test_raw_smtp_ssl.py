import smtplib
import os
import ssl

host = "smtp.titan.email"
port = 465
user = "helpdesk@jansevakindia.in"
password = os.getenv('EMAIL_HOST_PASSWORD')

print(f"Connecting to {host}:{port} (SSL)...")
try:
    # 1. Connect with SSL
    server = smtplib.SMTP_SSL(host, port)
    server.set_debuglevel(1)
    
    # 2. EHLO
    print("Sending EHLO...")
    server.ehlo()
    
    # 3. Login
    print("Logging in...")
    server.login(user, password)
    print("✅ Login Successful!")
    
    # 4. Send Mail
    print("Sending email...")
    msg = f"Subject: Raw SMTP SSL Test\n\nThis is a test from raw python script (SSL)."
    server.sendmail(user, "poojary.rupesh12@gmail.com", msg)
    print("✅ Email Sent!")
    
    server.quit()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
