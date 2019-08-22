from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminView

from dashboard.forms import UserCreationForm
from .models import User, WeatherForecast, SynopticWarning, \
    SynopticWarningCriteria, SynopticSituation, Province, City, Client, Forecaster, \
    MasterForecaster, ClientForecastTypeOrder, OneDayForecast, TwoDayForecast


class UserAdmin(UserAdminView):
    add_form = UserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',),
            
        }),
    )


class ClientAdmin(UserAdmin):
    model = Forecaster

    fieldsets = UserAdmin.fieldsets + (
        (None,
         {'fields': ('is_client', 'cities')},
         ),
    )


class ForecasterAdmin(UserAdmin):
    model = Forecaster

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('clients', 'is_forecaster')}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Forecaster, ForecasterAdmin)
admin.site.register(MasterForecaster, ForecasterAdmin)
admin.site.register(WeatherForecast)
admin.site.register(SynopticWarning)
admin.site.register(SynopticWarningCriteria)
admin.site.register(SynopticSituation)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(OneDayForecast)
admin.site.register(TwoDayForecast)
admin.site.register(ClientForecastTypeOrder)
