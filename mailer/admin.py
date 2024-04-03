from django.contrib import admin

from mailer.models import Client, Mailing, Message, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    search_fields = ('name', 'email',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'status')
    list_filter = ('message',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', )
    search_fields = ('subject', 'body',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status', 'response', )
    search_fields = ('status', 'response',)
