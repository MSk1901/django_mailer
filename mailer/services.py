import os
from smtplib import SMTPException

from django.core.mail import send_mail
from django.utils import timezone

from mailer.models import MailingLog, Mailing


def send_emails(mailing):
    message = mailing.message_set.first()

    if not message:
        MailingLog.objects.create(
            last_try=timezone.now(),
            status='error',
            response="Нет сообщений для отправки",
            mailing=mailing,
        )
    else:
        recipients = [recipient.email for recipient in mailing.recipients.all()]
        email_from = os.getenv('EMAIL_HOST_USER')

        try:
            send_mail(
                message.subject,
                message.body,
                email_from,
                recipients,
                fail_silently=False
            )
            MailingLog.objects.create(
                last_try=timezone.now(),
                status='success',
                response='ОК',
                mailing=mailing,
            )

        except SMTPException as e:
            MailingLog.objects.create(
                last_try=timezone.now(),
                status='error',
                response=str(e),
                mailing=mailing,
            )


def periodic_mailing(frequency: int):

    now = timezone.now()

    for mailing in Mailing.objects.filter(frequency=frequency).filter(status__in=['created', 'started']):
        if now >= mailing.start_time:
            if not mailing.end_time or now < mailing.end_time:
                if mailing.frequency == 0:
                    mailing.status = 'finished'
                else:
                    mailing.status = 'started'
                mailing.save()
                send_emails(mailing)

            else:
                mailing.status = 'finished'
                mailing.save()
