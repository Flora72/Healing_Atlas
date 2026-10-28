from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def premium_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.membership == 'premium':
            return view_func(request, *args, **kwargs)

        messages.warning(
            request,
            "This feature is available to Premium members. Please upgrade."
        )
        return redirect('upgrade_prompt')

    return _wrapped_view
