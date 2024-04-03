from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, EmailConfirmationSentView, \
    UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView, UserListView, UserBlockView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    path('list', UserListView.as_view(), name='list'),
    path('block/<int:pk>', UserBlockView.as_view(), name='block'),

]
