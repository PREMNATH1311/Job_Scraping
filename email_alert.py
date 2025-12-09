import os
import smtplib
from email.message import EmailMessage


def sent_email(count):
    msg=EmailMessage()
    msg['Subject']="Job Scraper Update"
    msg["From"]=os.getenv("EMAIL_USER")
    msg["To"]=os.getenv("EMAIL_TO")
    
    msg.set_content(f"{count} New jobs were added to te database. ")
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"))
        smtp.send_message(msg=msg)