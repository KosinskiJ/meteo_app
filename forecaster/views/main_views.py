import datetime

from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from dashboard.mixins import ForecasterRequiredMixin
from dashboard.models import Client, ClientForecastTypeOrder, SynopticSituation
from forecaster import services


class Dashboard(ForecasterRequiredMixin, ListView):
    template_name = "forecaster/dashboard.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = Client.objects.filter(clientforecasttypeorder__forecaster=self.request.user).distinct()
        return queryset


class ClientDetails(ForecasterRequiredMixin, TemplateView):
    template_name = "forecaster/client_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['client'] = Client.objects.get(pk=self.kwargs['client_pk'])
        return context


class ForecastsSchedule(ForecasterRequiredMixin, ListView):
    template_name = "forecaster/forecasts_schedule.html"
    context_object_name = "client_orders"

    def get_queryset(self):
        queryset = ClientForecastTypeOrder.objects.filter(client_id=self.kwargs['client_pk'],
                                                          forecaster=self.request.user.forecaster,
                                                          expire_date__gte=datetime.datetime.now(), )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['client'] = Client.objects.get(pk=self.kwargs['client_pk'])
        context['24h_dates'] = services.generate_next_five_dates('24')
        context['48h_dates'] = services.generate_next_five_dates('48')

        return context


class ForecastsHistory(ForecasterRequiredMixin, ListView):
    template_name = "forecaster/forecasts_history.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(id=self.kwargs['client_pk'])
        return context

    def get_queryset(self):
        queryset = ClientForecastTypeOrder.objects.filter(client_id=self.kwargs['client_pk'],
                                                          forecaster=self.request.user.forecaster, )
        return queryset


class SynopticSituationCreateView(ForecasterRequiredMixin, CreateView):
    template_name = "forecaster/synoptic_situation_form.html"
    model = SynopticSituation
    pk_url_kwarg = "synopt"
    fields = ['begin_date', 'finish_date', 'description', 'created_by', ]

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'created_by': self.request.user.forecaster,
            'begin_date': (datetime.datetime.now()).replace(hour=7, minute=0, second=0, microsecond=0),
            'finish_date': (datetime.datetime.now()).replace(hour=7, minute=0, second=0,
                                                             microsecond=0) + datetime.timedelta(days=1),

        })
        return initial

    def get_success_url(self):
        return reverse("forecaster:dashboard")


class SynopticSituationUpdateView(ForecasterRequiredMixin, UpdateView):
    template_name = "forecaster/synoptic_situation_form.html"
    model = SynopticSituation
    pk_url_kwarg = "synopt"
    fields = ['begin_date', 'finish_date', 'description', 'modified_by', ]

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'modified_by': self.request.user.forecaster,
        })

        return initial

    def get_success_url(self):
        return reverse("forecaster:dashboard")


class SynopticSituationListView(ForecasterRequiredMixin, ListView):
    template_name = "forecaster/synoptic_situation_list.html"
    model = SynopticSituation
    queryset = SynopticSituation.objects.all().order_by('-id')
    context_object_name = "synoptic_situations"
    paginate_by = 5
