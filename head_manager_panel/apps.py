from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_activation_email

register_worker = Signal(providing_args=['instance'])


def worker_activation_dispatcher(sender, **kwargs):
    send_activation_email(kwargs['instance'])


register_worker.connect(worker_activation_dispatcher)


class HeadManagerPanelConfig(AppConfig):
    name = 'head_manager_panel'
