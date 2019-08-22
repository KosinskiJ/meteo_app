from django.contrib.auth.mixins import AccessMixin
from django.http import Http404


class ClientRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_client:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ForecasterRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_forecaster:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
