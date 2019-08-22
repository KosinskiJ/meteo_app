from django.conf.urls import url

from dashboard.views import Index, Login, LoginRedirect, PasswordReset, PasswordResetDone, PasswordResetConfirm, \
    PasswordResetComplete, Contact

app_name = "dashboard"
urlpatterns = [
    url("^$", Index.as_view(), name="index"),
    url("^contact/$", Contact.as_view(), name="contact"),

    # login
    url("^login/$", Login.as_view(), name="login"),
    url("^login-redirect/$", LoginRedirect.as_view(), name="login_redirect"),

    # reset password
    url(r'^password-reset/$', PasswordReset.as_view(), name='password_reset'),
    url(r'^password-reset/done/$', PasswordResetDone.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetComplete.as_view(), name='password_reset_complete'),
]
