import logging
from urllib.parse import urlencode, urlunparse

from social_core.exceptions import AuthException

logger = logging.getLogger(__name__)


def save_profile(backend, user, response, *args, **kwargs):
    userpic_key, user_about_url = None, None
    if backend.name == 'google-oauth2':
        userpic_key = 'picture'
    elif backend.name == 'vk-oauth2':
        userpic_key = 'user_photo'

        user_about_requested_fields = ('bdate',)
        user_about_url = urlunparse(
            ('https',  # scheme
             'api.vk.com',  # netloc
             '/method/users.get',  # path
             None,  # params
             urlencode({
                 'fields': ','.join(user_about_requested_fields),
                 'access_token': response.get('access_token', None),
                 'version': '5.95',
             }),  # query
             None  # fragment
             )
        )

    if userpic_key and \
            not user.shopuserextended.udpate_userpic(response.get(userpic_key)):
        raise AuthException("Cannot update userpic")

    if user_about_url:
        age_status = user.validate_age(user_about_url)
        if age_status is None:
            logger.error(f"Cannot define age by URL {user_about_url}")
        elif not age_status:
            raise AuthException("Age must be more than 17")
