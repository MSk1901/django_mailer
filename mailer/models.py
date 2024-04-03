from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):

    name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='почта')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.name}, e-mail: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):

    FREQUENCY = {
        0: 'разово',
        1: 'ежедневно',
        2: 'еженедельно',
        3: 'ежемесячно'
    }

    STATUSES = {
        'created': 'создана',
        'started': 'запущена',
        'finished': 'завершена'
    }

    start_time = models.DateTimeField(verbose_name='время начала')
    end_time = models.DateTimeField(verbose_name='время окончания', default=None, **NULLABLE)
    frequency = models.SmallIntegerField(choices=FREQUENCY, default=0, verbose_name='частота')
    status = models.CharField(choices=STATUSES, default='created', verbose_name='статус')
    recipients = models.ManyToManyField(Client, verbose_name='получатели', related_name='mailing')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.start_time}: {self.frequency}, {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                'deactivate',
                'Can deactivate mailing'
            ),
        ]


class Message(models.Model):

    subject = models.CharField(max_length=100, verbose_name='тема')
    body = models.TextField(verbose_name='тело')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class MailingLog(models.Model):

    STATUSES = {
        'success': 'успешно',
        'error': 'ошибка',
    }

    last_try = models.DateTimeField(verbose_name='время последней попытки')
    status = models.CharField(choices=STATUSES, verbose_name='статус')
    response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.last_try} - {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
