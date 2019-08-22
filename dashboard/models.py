from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel


class Province(models.Model):
    PROVINCE_NAME_CHOICES = (
        ("02", "dolnośląskie"),
        ("04", "kujawsko-pomorskie"),
        ("06", "lubelskie"),
        ("08", "lubuskie"),
        ("10", "łódzkie"),
        ("12", "małopolskie"),
        ("14", "mazowieckie"),
        ("16", "opolskie"),
        ("18", "podkarpackie"),
        ("20", "podlaskie"),
        ("22", "pomorskie"),
        ("24", "śląskie"),
        ("26", "świętokrzyskie"),
        ("28", "warmińsko-mazurskie"),
        ("30", "wielkopolskie"),
        ("32", "zachodniopomorskie"),
    )
    name = models.CharField(choices=PROVINCE_NAME_CHOICES,
                            verbose_name="Nazwa",
                            max_length=2)

    def __str__(self):
        return f"Wojewodztwo: {self.get_name_display()}"

    def save(self, *args, **kwargs):
        if Province.objects.filter(name=self.name):
            raise ValueError("This province is already in the database.")
        super(Province, self).save(*args, **kwargs)


class City(models.Model):
    name = models.TextField(max_length=100,
                            verbose_name="Nazwa")
    longitude = models.DecimalField(validators=[MaxValueValidator(180),
                                                MinValueValidator(-180)],
                                    decimal_places=10,
                                    max_digits=13,
                                    verbose_name="Długość geograficzna")

    latitude = models.DecimalField(validators=[MaxValueValidator(90),
                                               MinValueValidator(-90)],
                                   decimal_places=10,
                                   max_digits=12,
                                   verbose_name="Szerokość geograficzna")

    province = models.ForeignKey(Province,
                                 verbose_name="Województwo")

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Adres email",
        max_length=255,
        unique=True,
    )

    is_client = models.BooleanField(default=False, blank=False)
    is_forecaster = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.username


class Client(User):
    cities = models.ManyToManyField('City')

    class Meta:
        verbose_name = "Client"


class Forecaster(User):
    class Meta:
        verbose_name = "Forecaster"


class MasterForecaster(Forecaster):
    class Meta:
        verbose_name = "Master forecaster"


class SynopticSituation(models.Model):
    begin_date = models.DateTimeField(verbose_name="Data rozpoczęcia")
    finish_date = models.DateTimeField(verbose_name="Data zakończenia")
    description = models.TextField(max_length=300,
                                   verbose_name="Opis")

    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name="Data wykonania")
    modification_date = models.DateTimeField(auto_now=True,
                                             verbose_name="Data modyfikacji")

    created_by = models.ForeignKey(Forecaster,
                                   related_name="synopticsituation_created_by",
                                   verbose_name="Wykonano przez")

    modified_by = models.ForeignKey(Forecaster,
                                    related_name="synopticsituation_modified_by",
                                    verbose_name="Zmodyfikowano przez",
                                    blank=True, null=True)

    def __str__(self):
        return f"Sytuacja synoptyczna na okres od: {str(self.begin_date)} do:{str(self.finish_date)}"


class SynopticWarningCriteria(models.Model):
    name = models.CharField(max_length=70,
                            verbose_name="Nazwa")

    LOW = 0
    MEDIUM = 1
    HIGH = 2

    DANGER_LEVEL_CHOICES = (
        (LOW, "NISKI"),
        (MEDIUM, "ŚREDNI"),
        (HIGH, "WYSOKI"),
    )
    danger_level = models.IntegerField(choices=DANGER_LEVEL_CHOICES,
                                       verbose_name="Poziom zagrożenia",
                                       default=MEDIUM)

    criteria = models.TextField(max_length=255,
                                verbose_name="Kryterium")

    effects = models.TextField(max_length=255,
                               verbose_name="Efekty")

    details = models.TextField(max_length=255,
                               verbose_name="Szczegóły")

    def __str__(self):
        return f"Kryterium: {self.name}, poziom zagrożenia: {self.get_danger_level_display()}"


class SynopticWarning(models.Model):
    begin_date = models.DateTimeField(verbose_name="Data rozpoczęcia",
                                      blank=True,
                                      null=True)

    finish_date = models.DateTimeField(verbose_name="Data zakończenia",
                                       blank=True,
                                       null=True)

    description = models.TextField(verbose_name="Opis",
                                   blank=True,
                                   null=True)

    creation_date = models.DateTimeField(verbose_name="Data wykonania",
                                         auto_now_add=True)

    modification_date = models.DateTimeField(verbose_name="Data modyfikacji",
                                             auto_now=True)

    synoptic_warning_criteria = models.ForeignKey(SynopticWarningCriteria)

    def __str__(self):
        return f"Ostrzeżenie pogodowe an okres {self.begin_date} - {self.finish_date}"


class WeatherForecast(models.Model):
    begin_date = models.DateTimeField(verbose_name="Data rozpoczęcia",
                                      blank=True, null=True)
    finish_date = models.DateTimeField(verbose_name="Data zakończenia",
                                       blank=True, null=True)

    DAY_NIGHT_CHOICES = (
        ("D", "Dzień"),
        ("N", "Noc"),
    )

    day_night = models.CharField(
        max_length=1,
        choices=DAY_NIGHT_CHOICES,
        default='D',
        verbose_name="Dzień/noc"
    )

    synoptic_warning = models.ManyToManyField(SynopticWarning, blank=True,
                                              verbose_name="Ostrzeżenie synoptyczne")
    description = models.TextField(max_length=300, blank=True, null=True,
                                   verbose_name="Opis")
    clouds = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                 verbose_name="Zachmurzenie")
    rainfall = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                   verbose_name="Opad deszczu")
    snowfall = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                   verbose_name="Opad śniegu")
    air_temp = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                   verbose_name="Temperatura powietrza")
    dewpoint_temp = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                        verbose_name="Temperatura punktu rosy")
    pressure = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                   verbose_name="Ciśnienie")
    humidity = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                   verbose_name="Wilgotność")
    wind_speed = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                     verbose_name="Prędkość wiatru")
    wind_gusts = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2,
                                     verbose_name="Porywy wiatru")

    WIND_DIRECTION_CHOICES = (
        ("N", "Północny"),
        ("NE", "Północno- wschodni"),
        ("E", "Wschodni"),
        ("SE", "Południowo- wschodni"),
        ("S", "Południowy"),
        ("SW", "Południowy- zachodni"),
        ("W", "Zachodni"),
        ("NW", "Północno- zachodni"),
    )

    wind_direction = models.CharField(
        max_length=2,
        choices=WIND_DIRECTION_CHOICES,
        default='N',
        blank=True,
        null=True,
        verbose_name="Kierunek wiatru"
    )

    sar_image = models.URLField(blank=True,
                                null=True,
                                verbose_name="Aktualne zdjęcie satelitarne")

    def __str__(self):
        return f"Prognoza pogody na okres {self.begin_date} - {self.finish_date}"


class ClientForecastTypeOrder(models.Model):
    forecaster = models.ManyToManyField(Forecaster, verbose_name="Odpowiedzialni meteorolodzy")
    client = models.ForeignKey(Client, verbose_name="Klient")
    city = models.ForeignKey(City, verbose_name="Miasto prognozy")
    begin_date = models.DateTimeField(verbose_name="Data rozpoczęcia")
    expire_date = models.DateTimeField(verbose_name="Data wygaśnięcia")

    @property
    def forecast_days(self):
        return (self.expire_date - self.begin_date).days

    FORECAST_TYPE_CHOICES = (
        ("24", "24h"),
        ("48", "48h")
    )

    forecast_type_choice = models.CharField(max_length=2, choices=FORECAST_TYPE_CHOICES)

    def __str__(self):
        return f"Klient: {self.client}, miasto: {self.city}, " \
               f"typ: {self.get_forecast_type_choice_display()}, data wygaśnięcia: {self.expire_date}"


class ForecastType(PolymorphicModel):
    created_by = models.ForeignKey(Forecaster, verbose_name="Wykonawca",
                                   related_name="created_by",
                                   )
    modified_by = models.ForeignKey(Forecaster, verbose_name="Zmodyfikował",
                                    related_name="modified_by",
                                    null=True,
                                    blank=True,
                                    )

    creation_date = models.DateTimeField(verbose_name="Data wykonania",
                                         auto_now_add=True, )
    modification_date = models.DateTimeField(verbose_name="Data modyfikacji",
                                             null=True,
                                             blank=True,
                                             auto_now=True, )

    count = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                        verbose_name="Numer prognozy", )

    STATUS_CHOICES = (
        ("D", "Draft"),
        ("A", "Aktywne"),
        ("H", "Archiwum"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="D")
    forecast_type_order = models.ForeignKey("ClientForecastTypeOrder", verbose_name="Zamowienie klienta")

    class Meta:
        unique_together = ('forecast_type_order', 'count',)


class OneDayForecast(ForecastType):
    weather_forecast1 = models.OneToOneField('WeatherForecast',
                                             related_name="wf1",
                                             verbose_name="Prognoza na dzień #1", )
    weather_forecast2 = models.OneToOneField('WeatherForecast',
                                             related_name="wf2",
                                             verbose_name="Prognoza na noc #1", )

    def get_type_string(self):
        return "OneDayForecast"

    def __str__(self):
        return f"Prognoza 24-godzinna: {self.forecast_type_order.client}, " \
               f"{self.count}/{self.forecast_type_order.forecast_days}, {self.forecast_type_order.city}"


class TwoDayForecast(ForecastType):
    weather_forecast1 = models.OneToOneField('WeatherForecast',
                                             related_name="wf1_48",
                                             verbose_name="Prognoza na dzień #1", )
    weather_forecast2 = models.OneToOneField('WeatherForecast',
                                             related_name="wf2_48",
                                             verbose_name="Prognoza na noc #1", )

    weather_forecast3 = models.OneToOneField('WeatherForecast',
                                             related_name="wf3_48",
                                             verbose_name="Prognoza na dzień #2", )
    weather_forecast4 = models.OneToOneField('WeatherForecast',
                                             related_name="wf4_48",
                                             verbose_name="Prognoza na noc #2", )

    def get_type_string(self):
        return "TwoDayForecast"

    def __str__(self):
        return f"Prognoza 48-godzinna: {self.forecast_type_order.client}, " \
               f"{self.count}/{self.forecast_type_order.forecast_days}, {self.forecast_type_order.city}"
