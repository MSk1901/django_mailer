from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):

    name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='почта')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.name}, e-mail: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
