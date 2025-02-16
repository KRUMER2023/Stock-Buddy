import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    

    sender_email = "KRUMER2023@gmail.com"  
    sender_password = "vmdd wrae llig chrk" 
    subject = "Your OTP for Verification"
    
    # Email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    body = f"Your OTP for email verification is: {otp}"
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in to your email account
            server.sendmail(sender_email, email, message.as_string())  # Send the email
            print(f"OTP sent successfully to {email}")
            return otp
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

def verify_otp(sent_otp):
    user_otp = input("Enter the OTP sent to your email: ")
    if user_otp == sent_otp:
        print("Email verified successfully!")
    else:
        print("Invalid OTP. Verification failed.")


# if __name__ == "__main__":
#     user_email = input("Enter your email address: ")
#     sent_otp = send_otp(user_email)
#     if sent_otp:
#         verify_otp(sent_otp)
