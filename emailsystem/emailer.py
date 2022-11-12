import email.message
import smtplib
from typing import Tuple


class EmailSystem:
    def __init__(
        self, sender="ifelaw2439@gmail.com", sender_pass="hezoqsvehtlpfhqt"
    ) -> None:
        self.sender = sender
        self.sender_pass = sender_pass
        self.gmail_code = 587

    def send_via_gmail(self, recipients, message) -> None:
        server = smtplib.SMTP("smtp.gmail.com", self.gmail_code)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sender, self.sender_pass)
        server.sendmail(from_addr=self.sender, to_addrs=recipients, msg=message)
        server.quit()

    def send_email(
        self,
        recipients=["ifelaw2439@gmail.com"],
        subject="Automated Email",
        message_html="<p>This is a sample email sent from Python</p>",
    ) -> Tuple:
        recipients = recipients
        msg = email.message.Message()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = ", ".join(recipients)
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(message_html)

        try:
            self.send_via_gmail(recipients=recipients, message=msg.as_string())
            return ("Success", 200)
        except Exception as e:
            print(e)
            return ("Error Ocurred: Email sending failed", 404)
