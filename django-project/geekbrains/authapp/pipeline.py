from social_core.exceptions import AuthException


def save_profile(backend, user, response, *args, **kwargs):
    userpic_key = None
    if backend.name == 'google-oauth2':
        userpic_key = 'picture'
    elif backend.name == 'vk-oauth2':
        userpic_key = 'user_photo'
    if userpic_key and \
            not user.shopuserextended.udpate_userpic(response.get(userpic_key)):
        raise AuthException("Cannot update userpic")
