from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .permission import LoginPermissionMiddlewareMixin, UrlPermissionMiddleware
from .utils import compile_urls


def check_request_has_user():
    """
    Check that LoginRequiredMiddleware isn't being used without its dependency,
    django.contrib.auth.middleware.AuthenticationMiddleware.
    """
    middlewares = settings.MIDDLEWARE_CLASSES

    if 'django.contrib.auth.middleware.AuthenticationMiddleware' in middlewares:
        return

    raise ImproperlyConfigured(
        (
            "MIDDLEWARE_CLASSES does not contain AuthenticationMiddleware."
            "LoginRequiredMiddleware requires authentication middleware to be"
            "installed. Ensure that your MIDDLEWARE_CLASSES setting includes"
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ),
    )


class LoginRequiredMiddleware(LoginPermissionMiddlewareMixin, UrlPermissionMiddleware):
    """
    Middleware that requires a user to be authenticated to view any page in
    LOGIN_PROTECTED_URLS other than LOGIN_URL. Exemptions to this requirement
    can optionally be specified in settings via a list of regular expressions
    in LOGIN_EXEMPT_URLS (which you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.

    Will default to protecting everything if LOGIN_PROTECTED_URLS is not in
    settings.

    Original code from:
    http://onecreativeblog.com/post/59051248/django-login-required-middleware

    This version has been modified to allow us to define areas of the site to
    password protect instead of protecting everything under /.
    """
    login_exempt_urls = [settings.LOGIN_URL, settings.LOGOUT_URL]
    login_exempt_urls += getattr(settings, 'LOGIN_EXEMPT_URLS', [])
    login_protected_urls = getattr(settings, 'LOGIN_PROTECTED_URLS', [r'^'])

    EXEMPT_URLS = compile_urls(login_exempt_urls)
    PROTECTED_URLS = compile_urls(login_protected_urls)

    SEND_MESSAGE = getattr(settings, 'LOGIN_REQUIRED_SEND_MESSAGE', True)

    def __init__(self, check=True):
        super(LoginRequiredMiddleware, self).__init__()
        if check:
            check_request_has_user()

    def get_exempt_url_patterns(self):
        return self.EXEMPT_URLS

    def get_protected_url_patterns(self):
        return self.PROTECTED_URLS

    def get_access_denied_message(self):
        if not self.SEND_MESSAGE:
            return ''

        return super(LoginRequiredMiddleware, self).get_access_denied_message()
