from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail


def send_verify_mail(user):
    if not user.email:
        raise RuntimeError(f'user {user.username} has not any email address')

    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key':   user.activationkey_set.values_list(
                                'activation_key', flat=True
                            ).first(),
    })

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале\n' + \
              f'{settings.DOMAIN_NAME} перейдите по ссылке:\n' + \
              f'{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message,
                     settings.EMAIL_HOST_USER,
                     [user.email],
                     fail_silently=False)
