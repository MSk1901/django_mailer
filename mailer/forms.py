from django import forms

from mailer.models import Mailing, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['placeholder'] = 'дд.мм.гггг чч:мм:сс'


class MailingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Фильтрация клиентов по пользователю
            self.fields['recipients'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Mailing
        exclude = ('status', 'owner')


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('mailing',)


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)
