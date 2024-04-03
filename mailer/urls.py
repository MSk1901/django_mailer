from django.urls import path
from django.views.decorators.cache import cache_page

from mailer.apps import MailerConfig
from mailer.views import MailingListView, MailingDetailView, MailingUpdateView, MailingCreateView, MailingDeleteView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView, MailingLogListView, \
    MailingDeactivateView, MainView

app_name = MailerConfig.name

urlpatterns = [
    path('mailings/', MailingListView.as_view(),  name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(),  name='mailing'),
    path('create/', MailingCreateView.as_view(),  name='create'),
    path('update/<int:pk>', MailingUpdateView.as_view(),  name='update'),
    path('delete/<int:pk>', MailingDeleteView.as_view(),  name='delete'),
    path('deactivate/<int:pk>', MailingDeactivateView.as_view(),  name='deactivate'),

    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/<int:pk>', ClientDetailView.as_view(), name='client'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('<int:pk>/logs', MailingLogListView.as_view(),  name='mailing_logs'),

    path('', cache_page(60)(MainView.as_view()),  name='main'),
]
