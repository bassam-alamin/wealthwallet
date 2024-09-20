import dataclasses
import logging
from dataclasses import dataclass
from typing import List

from decouple import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from wealthwallet.celery import app

from_email_env_variable = f"{config('EMAIL_ALIAS')}" \
                          f" <{settings.EMAIL_HOST_USER}>"


@dataclass
class EmailNotificationService:
    to: List[str]
    subject: str
    body: str
    template_html: str
    context: dict = dataclasses.field(default_factory=dict)
    reply_to: List = dataclasses.field(default_factory=lambda: [config("REPLY_TO_EMAIL")])

    def __post_init__(self):
        if not self.to:
            raise ValueError("Email must have a recipient")

        if not self.subject:
            raise ValueError("Email must have a subject")

        if not self.body:
            raise ValueError("Email must have a body")

    def get_cc_emails(self):
        try:
            cc_list = config("CC_EMAILS").split(",")
            sorted_list = list(cc_list)
            return sorted_list
        except Exception as err:
            logging.info(err)
            sorted_list = []
            return sorted_list

    def send_email(self):
        html_message = render_to_string(
            self.template_html,
            {'context': self.context}
        )
        from_email = from_email_env_variable
        cc_list = self.get_cc_emails()
        send_email = EmailMessage(
            self.subject,
            html_message,
            from_email,
            self.to,
            cc_list,
            reply_to=self.reply_to,
        )
        send_email.content_subtype = "html"
        print(send_email.send(fail_silently=False))


class EmailNotification:
    @staticmethod
    @app.task
    def send_welcome_email(data: dict):
        to = [data.get('email')]
        subject = "Welcome"
        body = "Welcome To our platform"
        template_html = "email_verify.html"
        context = {
            'firstName': data.get('first_name')
        }
        EmailNotificationService(
            to=to,
            subject=subject,
            body=body,
            template_html=template_html,
            context=context
        ).send_email()
        return True