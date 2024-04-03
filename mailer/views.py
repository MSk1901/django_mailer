from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, TemplateView
from django.urls import reverse, reverse_lazy

from blog.models import BlogPost
from mailer.forms import MailingForm, MessageForm, ClientForm
from mailer.models import Mailing, Client, MailingLog


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(name='manager').exists():
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=user)


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()
        context['messages'] = mailing.message_set.all()
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'message_form' not in context:
            message_form = MessageForm()
            context['message_form'] = message_form
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        message_form = MessageForm(self.request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.mailing = self.object
            message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailer:mailing', kwargs={'pk': self.object.pk})


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'message_form' not in context:
            if self.request.method == 'POST':
                message_form = MessageForm(self.request.POST, instance=self.object)
            else:
                mailing = self.get_object()
                messages = mailing.message_set.all()
                message_form = MessageForm(instance=messages.first()) if messages.exists() else MessageForm()
            context['message_form'] = message_form
        return context

    def form_valid(self, form):
        self.object = form.save()
        messages = self.object.message_set.all()
        if messages.exists():
            message_form = MessageForm(self.request.POST, instance=messages.first())
        else:
            message_form = MessageForm(self.request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.mailing = self.object
            message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailer:mailing', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailer:mailing_list')


class MailingDeactivateView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        mailing = Mailing.objects.get(pk=self.kwargs['pk'])
        mailing.status = 'finished'
        mailing.save()
        return reverse_lazy('mailer:mailing_list')


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    success_url = reverse_lazy('mailer:clients_list')
    form_class = ClientForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    success_url = reverse_lazy('mailer:clients_list')
    form_class = ClientForm


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailer:clients_list')


class MailingLogListView(ListView):
    model = MailingLog

    def get_queryset(self):
        mailing_pk = self.kwargs['pk']
        return MailingLog.objects.filter(mailing_id=mailing_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = Mailing.objects.get(pk=self.kwargs['pk'])
        context['mailing'] = mailing
        return context


class MainView(TemplateView):
    template_name = 'mailer/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.all().count()
        context['active_mailings'] = Mailing.objects.filter(status__in=['created', 'started']).count()
        context['unique_clients'] = Client.objects.filter(mailing__isnull=False).distinct().count()

        blog_posts = BlogPost.objects.all().order_by('?')[:3] if BlogPost.objects.count() >= 3 \
            else BlogPost.objects.all()

        for post in blog_posts:
            post.view_count += 1
            post.save()

        context['blog_posts'] = blog_posts
        return context
