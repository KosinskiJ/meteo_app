from django.conf.urls import url

from forecaster.views.one_day_forecast import OneDayForecastEdit, OneDayForecastView, ajax_call_one_day
from forecaster.views.two_day_forecast import ajax_call_two_day, TwoDayForecastView, TwoDayForecastEdit
from forecaster.views.main_views import Dashboard, ClientDetails, ForecastsSchedule, ForecastsHistory, \
    SynopticSituationListView, SynopticSituationUpdateView, SynopticSituationCreateView

app_name = "forecaster"

urlpatterns = [
    url("^$", Dashboard.as_view(), name="dashboard"),
    url(r'^clients/(?P<client_pk>\d+)/$', ClientDetails.as_view(), name="client_details"),
    url(r'^clients/(?P<client_pk>\d+)/forecasts-schedule/$', ForecastsSchedule.as_view(), name="forecasts_schedule"),
    url(r'^clients/(?P<client_pk>\d+)/forecasts-history/$', ForecastsHistory.as_view(), name="forecasts_history"),
    url(r'^synoptic-situations/$', SynopticSituationListView.as_view(), name="synoptic_situation"),
    url(r'^synoptic-situation-create/$', SynopticSituationCreateView.as_view(),
        name="synoptic_situation_create"),
    url(r'^synoptic-situation/(?P<synopt>\d+)/edit/$', SynopticSituationUpdateView.as_view(),
        name="synoptic_situation_edit"),

    # forecasts
    url(
        r'^clients/(?P<client_pk>\d+)/one-day-create/(?P<order_pk>\d+)/(?P<wf_count>\d+)/(?P<location>\w+\s{0,1}\w+)/'
        r'(?P<latitude>\d+\.\d+)/(?P<longitude>\d+\.\d+)/(?P<begin_date>([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])))/$',
        OneDayForecastView.as_view(),
        name="one_day"),
    url(r'^clients/(?P<client_pk>\d+)/one-day-edit/(?P<one_day_pk>\d+)/$', OneDayForecastEdit.as_view(),
        name="one_day_edit"),

    url(
        r'^clients/(?P<client_pk>\d+)/two-day-create/(?P<order_pk>\d+)/(?P<wf_count>\d+)/(?P<location>\w+\s{0,1}\w+)/'
        r'(?P<latitude>\d+\.\d+)/(?P<longitude>\d+\.\d+)/(?P<begin_date>([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])))/$',
        TwoDayForecastView.as_view(),
        name="two_day"),
    url(r'^clients/(?P<client_pk>\d+)/two-day-edit/(?P<two_day_pk>\d+)/$', TwoDayForecastEdit.as_view(),
        name="two_day_edit"),

    url(r'ajax/one_day_forecast/$', ajax_call_one_day, name="one_day_forecast_ajax"),
    url(r'ajax/two_day_forecast/$', ajax_call_two_day, name="two_day_forecast_ajax"),
]
