from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from functools import wraps


def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_doctor:
            messages.error(request, "You are not a Doctor and you are unauthorized to view this page")
            return HttpResponseRedirect(reverse('login'))
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view