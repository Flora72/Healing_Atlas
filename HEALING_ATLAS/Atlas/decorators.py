from django.shortcuts import redirect
from functools import wraps

def basic_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.membership in ['basic', 'premium']:
            return view_func(request, *args, **kwargs)
        return redirect('upgrade_prompt')  
    return _wrapped_view
