#! /usr/bin/env python

__author__ = 'Josef Ludvicek <josef.ludvicek.cz@gmail.com>'

from email.mime.text import MIMEText

import smtplib
import subprocess

LOGIN = 'user@email.com'
PASS = 'emailPass'
SMTP_URL = 'smtp.server.com'
SMTP_PORT = 465
RECIPIENT = 'some.recipient@email.com'

TEMPLATE = '''
Raspberry joined network:
---------------------------------------------------------------------
%s
---------------------------------------------------------------------
'''


def get_ip_string():
    """
    Get IPv4 device address from ifconfig command.

    :return: string result of ifconfig willed into TEMPLATE
    """
    p = subprocess.Popen('ifconfig', shell=True, stdout=subprocess.PIPE)
    data = p.communicate()[0]
    return TEMPLATE % data


class Client(object):
    def __init__(self, email, password, url, port):
        self.email = email
        self.password = password
        self.server = url
        self.port = port
        session = smtplib.SMTP_SSL(self.server, self.port, timeout=10)
        session.ehlo()
        # session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_mail(self, recipient, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = recipient

        self.session.sendmail(
            self.email,
            recipient,
            msg.as_string())

    def quit(self):
        self.session.quit()


try:
    client = Client(LOGIN, PASS, SMTP_URL, SMTP_PORT)
    client.send_mail(RECIPIENT, 'Raspberry Pi joined network', get_ip_string())

except Exception, e:
    print "Failed to send email"
    print e
    exit(1)
