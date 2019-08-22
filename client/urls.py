from django.conf.urls import url

from client.views import LatestForecastsListView, ArchiveListView, DashboardTemplateView, ForecastDetailView, \
    ArchiveAllOrdersListView

app_name = "client"
urlpatterns = [
    url("^$", DashboardTemplateView.as_view(), name="dashboard"),
    url("^latest/$", LatestForecastsListView.as_view(), name="latest_forecasts"),
    url("^archive/$", ArchiveAllOrdersListView.as_view(), name="archive_all_orders"),
    url("^archive/(?P<pk>\d+)/$", ArchiveListView.as_view(), name="archive"),
    url("^forecast/(?P<pk>\d+)/$", ForecastDetailView.as_view(), name="forecast_details"),
]
