from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, FormView


class Index(TemplateView):
    template_name = "dashboard/index.html"


class Contact(TemplateView):
    template_name = "dashboard/contact.html"


class Login(LoginView):
    template_name = "dashboard/login.html"


class LoginRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return reverse_lazy("admin:index")
            elif self.request.user.is_forecaster:
                return reverse_lazy("forecaster:dashboard")
            elif self.request.user.is_client:
                return reverse_lazy("client:dashboard")
        else:
            return reverse_lazy("dashboard:login")


class PasswordReset(PasswordResetView):
    email_template_name = "dashboard/reset/password_reset_email.html"
    subject_template_name = "dashboard/reset/password_reset_subject.txt"
    success_url = reverse_lazy("dashboard:password_reset_done")
    template_name = "dashboard/reset/password_reset_form.html"


class PasswordResetDone(PasswordResetDoneView):
    template_name = "dashboard/reset/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy("dashboard:password_reset_complete")
    template_name = "dashboard/reset/password_reset_confirm.html"


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "dashboard/reset/password_reset_complete.html"
