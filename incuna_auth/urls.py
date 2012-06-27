from django import forms
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView


class IncunaAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_('Email'), max_length=320)


urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'authentication_form': IncunaAuthenticationForm}, name='auth_login'),
    url(r'^logout/$', 'logout', {'template_name': 'registration/logout.html'}, name='auth_logout'),
    # Change password (when logged in)
    url(r'^password/change/$', 'password_change', name='auth_password_change'),
    url(r'^password/change/done/$', 'password_change_done', name='password_change_done'),
    # Reset password (when not logged in via unique email link)
    url(r'^password/reset/$', 'password_reset', name='auth_password_reset'),
    url(r'^password/reset/done/$', 'password_reset_done', name='auth_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete', name='auth_password_reset_complete'),
    url(r'^sso/$', RedirectView.as_view(url=reverse_lazy('admin:admin_sso_openiduser_start')), name='sso_login'),
)

