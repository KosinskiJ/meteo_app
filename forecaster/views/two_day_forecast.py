import datetime
import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from dashboard.mixins import ForecasterRequiredMixin
from dashboard.models import ClientForecastTypeOrder, Client, TwoDayForecast
from forecaster.forms import WeatherForecastForm, TwoDayForecastForm
from forecaster.weather_api.darksky_api import get_generalized_darksky_forecast


class TwoDayForecastView(ForecasterRequiredMixin, CreateView):
    template_name = "forecaster/two_day.html"
    form_class = TwoDayForecastForm
    client = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.client

        if self.request.POST:
            context['wf1_form'] = WeatherForecastForm(self.request.POST, prefix="wf1", )
            context['wf2_form'] = WeatherForecastForm(self.request.POST, prefix="wf2", )
            context['wf3_form'] = WeatherForecastForm(self.request.POST, prefix="wf3", )
            context['wf4_form'] = WeatherForecastForm(self.request.POST, prefix="wf4", )
        else:

            day = datetime.datetime.strptime(self.kwargs['begin_date'],
                                             "%Y-%m-%d").date()

            context['wf1_form'] = WeatherForecastForm(prefix="wf1", initial={
                'begin_date': self.kwargs['begin_date'] + " 06:00",
                'finish_date': self.kwargs['begin_date'] + " 18:00",
                'day_night': "D",
            }, )
            context['wf2_form'] = WeatherForecastForm(prefix="wf2", initial={
                'begin_date': self.kwargs['begin_date'] + " 18:00",
                'finish_date': str((day + datetime.timedelta(days=1))) + " 06:00",
                'day_night': "N",
            }, )
            context['wf3_form'] = WeatherForecastForm(prefix="wf3", initial={
                'begin_date': str((day + datetime.timedelta(days=1))) + " 06:00",
                'finish_date': str((day + datetime.timedelta(days=1))) + " 18:00",
                'day_night': "D",
            }, )
            context['wf4_form'] = WeatherForecastForm(prefix="wf4", initial={
                'begin_date': str((day + datetime.timedelta(days=1))) + " 18:00",
                'finish_date': str((day + datetime.timedelta(days=2))) + " 06:00",
                'day_night': "N",
            })

        return context

    def get_success_url(self):
        return reverse("forecaster:client_details",
                       kwargs={'client_pk': self.kwargs['client_pk'], })

    def form_valid(self, form):
        context = self.get_context_data()
        wf1 = context['wf1_form']
        wf2 = context['wf2_form']
        wf3 = context['wf3_form']
        wf4 = context['wf4_form']

        if wf1.is_valid() and wf2.is_valid() and wf3.is_valid() and wf4.is_valid():
            self.object = form.save(commit=False)
            wf1.save()
            wf2.save()
            wf3.save()
            wf4.save()
            self.object.weather_forecast1 = wf1.instance
            self.object.weather_forecast2 = wf2.instance
            self.object.weather_forecast3 = wf3.instance
            self.object.weather_forecast4 = wf4.instance
            self.object.save()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        self.client = Client.objects.get(id=self.kwargs['client_pk'])

        initial = super().get_initial()
        initial.update({
            'client': self.client,
            'created_by': self.request.user.forecaster,
            'forecast_type_order': ClientForecastTypeOrder.objects.get(pk=self.kwargs['order_pk']),
            'count': self.kwargs['wf_count'],
        })
        return initial


class TwoDayForecastEdit(ForecasterRequiredMixin, UpdateView):
    template_name = "forecaster/two_day.html"
    form_class = TwoDayForecastForm
    client = None

    def get_object(self, queryset=None):
        queryset = TwoDayForecast.objects.get(pk=self.kwargs['two_day_pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.client

        if self.request.POST:
            context['wf1_form'] = WeatherForecastForm(self.request.POST, prefix="wf1", )
            context['wf2_form'] = WeatherForecastForm(self.request.POST, prefix="wf2", )
            context['wf3_form'] = WeatherForecastForm(self.request.POST, prefix="wf3", )
            context['wf4_form'] = WeatherForecastForm(self.request.POST, prefix="wf4", )
        else:
            context['wf1_form'] = WeatherForecastForm(prefix="wf1", instance=self.get_object().weather_forecast1)
            context['wf2_form'] = WeatherForecastForm(prefix="wf2", instance=self.get_object().weather_forecast2)
            context['wf3_form'] = WeatherForecastForm(prefix="wf3", instance=self.get_object().weather_forecast3)
            context['wf4_form'] = WeatherForecastForm(prefix="wf4", instance=self.get_object().weather_forecast4)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        wf1 = context['wf1_form']
        wf2 = context['wf2_form']
        wf3 = context['wf3_form']
        wf4 = context['wf4_form']

        if wf1.is_valid() and wf2.is_valid() and wf3.is_valid() and wf4.is_valid():
            self.object = form.save(commit=False)
            wf1.save()
            wf2.save()
            wf3.save()
            wf4.save()
            self.object.weather_forecast1 = wf1.instance
            self.object.weather_forecast2 = wf2.instance
            self.object.weather_forecast3 = wf3.instance
            self.object.weather_forecast4 = wf4.instance
            self.object.save()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        self.client = Client.objects.get(id=self.kwargs['client_pk'])
        initial = super().get_initial()
        initial.update({
            'client': Client.objects.get(id=self.kwargs['client_pk']),
            'modified_by': self.request.user.forecaster,
        })
        return initial

    def get_success_url(self):
        return reverse("forecaster:client_details",
                       kwargs={'client_pk': self.kwargs['client_pk'], })


def ajax_call_two_day(request):
    if request.is_ajax():
        begin_date_wf1 = datetime.datetime.strptime(request.POST.getlist('begin_date_wf1')[0],
                                                    '%Y-%m-%d %H:%M').timestamp()
        begin_date_wf2 = datetime.datetime.strptime(request.POST.getlist('begin_date_wf2')[0],
                                                    '%Y-%m-%d %H:%M').timestamp()

        begin_date_wf3 = datetime.datetime.strptime(request.POST.getlist('begin_date_wf3')[0],
                                                    '%Y-%m-%d %H:%M').timestamp()

        begin_date_wf4 = datetime.datetime.strptime(request.POST.getlist('begin_date_wf4')[0],
                                                    '%Y-%m-%d %H:%M').timestamp()

        wf1 = json.dumps(get_generalized_darksky_forecast(begin_date_wf1, request.POST.getlist('latitude')[0],
                                                          request.POST.getlist('longitude')[0]))
        wf2 = json.dumps(get_generalized_darksky_forecast(begin_date_wf2, request.POST.getlist('latitude')[0],
                                                          request.POST.getlist('longitude')[0]))
        wf3 = json.dumps(get_generalized_darksky_forecast(begin_date_wf3, request.POST.getlist('latitude')[0],
                                                          request.POST.getlist('longitude')[0]))
        wf4 = json.dumps(get_generalized_darksky_forecast(begin_date_wf4, request.POST.getlist('latitude')[0],
                                                          request.POST.getlist('longitude')[0]))

        wfs_json = {'wf1': wf1,
                    'wf2': wf2,
                    'wf3': wf3,
                    'wf4': wf4,
                    }

    return HttpResponse(
        json.dumps(wfs_json),
        content_type="application/json",
    )
