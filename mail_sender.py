from typing import List

from config import ConfigLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import jinja2


class MailSender:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.jinja = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    def _new_mail(self, subject: str):
        multipart = MIMEMultipart()
        multipart['From'] = formataddr(('Notification service', self.config.mail_from))
        multipart['To'] = self.config.mail_to
        multipart['Subject'] = subject
        return multipart

    def _init_smtp(self):
        self.smtp = smtplib.SMTP(self.config.mail_host, self.config.mail_port)
        self.smtp.starttls()
        self.smtp.login(self.config.mail_username, self.config.mail_password)

    def _finalize_smtp(self):
        self.smtp.quit()

    def send_mail(self, message: str, subject: str = 'Notification'):
        multipart = self._new_mail(subject)

        multipart.attach(MIMEText(message, 'plain'))
        self._init_smtp()
        self.smtp.send_message(multipart)
        self._finalize_smtp()

    def send_mail_html(self, html_message: str, subject: str = 'Notification'):
        multipart = self._new_mail(subject)

        multipart.attach(MIMEText(html_message, 'html'))
        self._init_smtp()
        self.smtp.send_message(multipart)
        self._finalize_smtp()

    def mail_update(self, new_files: List[str], updated_files: List[str]):
        template = self.jinja.get_template('email.html.jinja')
        text = template.render(new_files=new_files, updated_files=updated_files)
        self.send_mail_html(text, "PFERD Sync Notification")