from django.core.management.base import BaseCommand
from django.utils import timezone

from mailer.models import Mailing
from mailer.services import send_emails


class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone.now()

        for mailing in Mailing.objects.filter(status__in=['created', 'started']):
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
