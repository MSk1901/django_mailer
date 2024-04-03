from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.models import Group

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, RedirectView

from config import settings
from users.forms import UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_verified:
            messages.error(self.request, 'Ваш адрес электронной почты не подтвержден.')
            return self.form_invalid(form)

        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        send_mail(
            'Подтвердите свой электронный адрес',
            f'''Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: 
            http://127.0.0.1:8000{activation_url}''',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class UserListView(ListView):
    model = User

    def get_queryset(self):
        managers_group = Group.objects.get(name='manager')
        return User.objects.exclude(groups=managers_group)


class UserBlockView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.is_active = False
        user.save()
        return reverse_lazy('users:list')
