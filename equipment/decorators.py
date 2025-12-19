from functools import wraps
from django.contrib.auth.decorators import user_passes_test


def login_required_no_next(view_func=None, login_url="/baza/"):
    """
    Jak login_required, ale bez parametru ?next=...
    (redirect_field_name=None => Django nie doklei querystringa).
    """
    decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=None,
    )

    if view_func is None:
        return decorator

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        return decorator(view_func)(request, *args, **kwargs)

    return _wrapped
