#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
import getpass


class ArgmentError(Exception):
    pass


class GmailSender:

    @staticmethod
    def _parse(fn):
        login, password = None, None
        with open(fn) as fp:
            for l in fp:
                l = l.rstrip()
                if ":" in l:
                    i = l.index(":")
                    a = l[:i].rstrip()
                    b = l[i + 1:].lstrip()
                    if a.lower() == "login":
                        login = b
                    elif a.lower() == "password":
                        password = b
        return login, password

    def __init__(self, login=None, password=None, authfile="gmail_auth"):
        """ Either (login,password) or authfile should be specified."""
        if login is None:
            login, password = self._parse(authfile)
        self._login, self._password = login, password

    def send(self, to_addr, subject, body, from_addr=None, ):
        """if from_addr is not specified, login is used as from-address."""
        if from_addr is None:
            from_addr = self._login
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp.ehlo()
        smtp.login(self._login, self._password)
        smtp.mail(self._login)
        smtp.rcpt(to_addr)
        smtp.data(msg.as_string())
        smtp.quit()


def main():
    print "Login:",
    login = raw_input()
    password = getpass.getpass()
    print "To:",
    to_addr = raw_input()
    print "Suject:",
    subject = raw_input()
    print "Message:"
    message = raw_input()
    sender = GmailSender(login=login, password=password)
    sender.send(to_addr, subject, message)

if __name__ == '__main__':
    main()
