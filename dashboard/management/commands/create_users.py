from django.core.management import BaseCommand

from dashboard.models import User, Client, Forecaster, MasterForecaster


class Command(BaseCommand):
    """Auto adding test values to database. Can be used in terminal: python manage.py create_users
    """

    def handle(self, **options):
        admin = User(username="admin", email="admi@client1.com", is_staff=True, is_superuser=True)
        admin.set_password("roottoor")
        admin.save()

        client = Client(username="client1", email="client1@client1.com", is_client=True)
        client.set_password("roottoor")
        client.save()

        forecaster = Forecaster(username="forecaster1", email="forecaster1@forecaster1.com", is_forecaster=True)
        forecaster.set_password("roottoor")
        forecaster.save()

        mforecaster = MasterForecaster(username="mforecaster1", email="mforecaster1@mforecaster1.com",
                                       is_forecaster=True)
        mforecaster.set_password("roottoor")
        mforecaster.save()