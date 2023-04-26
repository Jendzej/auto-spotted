import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = int(os.getenv("SMTP_PORT", "465"))
password_smtp = os.getenv("SMTP_PASSWORD", "vbajevbzcrvouesz")
email = os.getenv("SMTP_MAIL", "auto.spotted.zset@gmail.com")
receiver_email = "jedrzej.runowicz@gmail.com"

context = ssl.create_default_context()

message_to_send = MIMEMultipart("alternative")
message_to_send["Subject"] = "Auto Spotted Raport"
message_to_send["From"] = email
message_to_send["To"] = receiver_email
text = """\
        Robimy testy"""
html = """\
        <html>
          <body>
            <h1>Testy są robione</h1>
            <i>Faza testowa mailera</i>
          </body>
        </html>
        """

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message_to_send.attach(part1)
message_to_send.attach(part2)


def send_mail(message, sender, password, receiver):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())


send_mail(message_to_send, email, password_smtp, receiver_email)
