from datetime import datetime, timedelta

from django.views.generic import ListView, TemplateView, DetailView

from dashboard.mixins import ClientRequiredMixin
from dashboard.models import ClientForecastTypeOrder, ForecastType, SynopticSituation


class DashboardTemplateView(ClientRequiredMixin, TemplateView):
    template_name = "client/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_at_7am = (datetime.now()).replace(hour=7, minute=0, second=0, microsecond=0)

        try:
            synoptic_situation = SynopticSituation.objects.filter(begin_date=today_at_7am,
                                                                  finish_date=today_at_7am + timedelta(days=1), ).last()
        except SynopticSituation.DoesNotExist:
            synoptic_situation = None

        context['synoptic_situation'] = synoptic_situation
        return context


class LatestForecastsListView(ClientRequiredMixin, ListView):
    template_name = "client/latest_forecasts.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = ClientForecastTypeOrder.objects \
            .filter(client=self.request.user.client, forecasttype__status="A").distinct() \
            .prefetch_related("forecasttype_set")
        return queryset


class ArchiveListView(ClientRequiredMixin, ListView):
    template_name = "client/archive.html"
    context_object_name = "forecasts"
    paginate_by = 10

    def get_queryset(self):
        queryset = ForecastType.objects.filter(forecast_type_order_id=self.kwargs['pk'], status="H").order_by(
            "-count")
        return queryset


class ArchiveAllOrdersListView(ClientRequiredMixin, ListView):
    template_name = "client/archive_all_orders.html"
    model = ClientForecastTypeOrder
    context_object_name = "orders"

    def get_queryset(self):
        queryset = ClientForecastTypeOrder.objects.filter(client=self.request.user.client)
        return queryset


class ForecastDetailView(ClientRequiredMixin, DetailView):
    template_name = "client/forecast_details.html"
    model = ForecastType
    context_object_name = "forecast"
