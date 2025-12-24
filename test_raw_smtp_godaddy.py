import smtplib
import os
import ssl

host = "smtpout.secureserver.net"
port = 465
user = os.getenv('EMAIL_HOST_USER')
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
    print(f"Logging in as {user}...")
    server.login(user, password)
    print("✅ Login Successful!")
    
    # 4. Send Mail
    print("Sending email...")
    # RFC 5322 Compliant Message
    msg = f"From: {user}\r\nTo: poojary.rupesh12@gmail.com\r\nSubject: GoDaddy SMTP Test\r\n\r\nThis is a test from raw python script (GoDaddy) with proper headers."
    server.sendmail(user, "poojary.rupesh12@gmail.com", msg)
    print("✅ Email Sent!")
    
    server.quit()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
