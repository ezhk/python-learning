from django.apps import AppConfig


class OrderappConfig(AppConfig):
    name = 'orderapp'

    def ready(self):
        import orderapp.signals
