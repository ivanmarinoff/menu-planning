from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect

UserModel = get_user_model()


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')  # Use reverse lookup for login URL

    def dispatch(self, request, *args, **kwargs):
        # Allow access if the user is a superuser
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Check if the user is authenticated and matches the expected pk
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Allow access if pk is not in the URL kwargs (some views may not require pk checking)
        if 'pk' not in kwargs:
            return super().dispatch(request, *args, **kwargs)

        # Restrict access if the user's pk does not match
        if request.user.pk != kwargs.get('pk'):
            raise Http404("You don't have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect(self.login_url)

    def get_user(self, request, *args, **kwargs):
        # Override this method to customize how the user associated with the request is obtained
        return request.user


class ErrorRedirectMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('landing'))
