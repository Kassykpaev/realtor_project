from os.path import splitext
from django.template.loader import render_to_string
from django.core.signing import Signer
from realtor_project.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_email(worker):
    if not ALLOWED_HOSTS:
        host = 'http://localhost:8000'
    else:
        host = f'http://{ALLOWED_HOSTS[0]}'

    context = {
        'host': host,
        'sign': signer.sign(worker.username),
        'worker': worker,
    }

    theme = render_to_string('email/theme.txt', context)

    body = render_to_string('email/body.txt', context)

    worker.email_user(theme, body)
