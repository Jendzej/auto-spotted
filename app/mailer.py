import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

port = int(os.getenv("SMTP_PORT", "465"))

context = ssl.create_default_context()


def report_added_post(message):
    message_to_send = MIMEMultipart("alternative")
    message_to_send["Subject"] = "Auto Spotted Report - Successfully added post"
    message_to_send["From"] = os.getenv("SMTP_MAIL")
    message_to_send["To"] = os.getenv("ADMIN_MAIL")
    text = f"""\
            Successfully added post
            Auto Spotted ZSET
            '{message}'
            """
    html = f"""\
            <html>
              <body style="background-color: #d1e3ff; padding: 3px;">
                <h1 style="background-color: white; border: 1px solid green; padding: 3px;">Successfully added post</h1>
                <i style="color: grey; font-size: 10px;">Auto Spotted ZSET</i>
                <p style="padding: 10px;">{message}</p>
              </body>
            </html>
            """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message_to_send.attach(part1)
    message_to_send.attach(part2)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(os.getenv("SMTP_MAIL"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_MAIL"), os.getenv("ADMIN_MAIL"), message_to_send.as_string())


def report_error(message):
    message_to_send = MIMEMultipart("alternative")
    message_to_send["Subject"] = "Auto Spotted Report - Successfully added post"
    message_to_send["From"] = os.getenv("SMTP_MAIL")
    message_to_send["To"] = os.getenv("ADMIN_MAIL")
    text = f"""\
                Some error occurred while creating a post...
                Auto Spotted ZSET
                Error message:
                '{message}'
                """
    html = f"""\
            <html>
              <body style="background-color: #d1e3ff;">
                <h1 style="background-color: white; border: 1px solid red;">Some error occurred...</h1>
                <i style="color: grey; font-size: 10px;">Auto Spotted ZSET</i>
                <h3>Error message:</h3>
                <p style="padding: 10px; color: #520a12;">{message}</p>
              </body>
            </html>
            """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message_to_send.attach(part1)
    message_to_send.attach(part2)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(os.getenv("SMTP_MAIL"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_MAIL"), os.getenv("ADMIN_MAIL"), message_to_send.as_string())
