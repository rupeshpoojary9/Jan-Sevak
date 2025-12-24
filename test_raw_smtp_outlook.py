import smtplib
import os
import ssl

host = "smtp.office365.com"
port = 587
user = os.getenv('EMAIL_HOST_USER')
password = os.getenv('EMAIL_HOST_PASSWORD')

print(f"Connecting to {host}:{port}...")
try:
    # 1. Connect
    server = smtplib.SMTP(host, port)
    server.set_debuglevel(1)
    
    # 2. EHLO
    print("Sending EHLO...")
    server.ehlo()
    
    # 3. STARTTLS
    print("Starting TLS...")
    context = ssl.create_default_context()
    server.starttls(context=context)
    
    # 4. EHLO again
    print("Sending EHLO (encrypted)...")
    server.ehlo()
    
    # 5. Login
    print(f"Logging in as {user}...")
    server.login(user, password)
    print("✅ Login Successful!")
    
    # 6. Send Mail
    print("Sending email...")
    msg = f"Subject: Outlook SMTP Test\n\nThis is a test from raw python script (Outlook)."
    server.sendmail(user, "poojary.rupesh12@gmail.com", msg)
    print("✅ Email Sent!")
    
    server.quit()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
