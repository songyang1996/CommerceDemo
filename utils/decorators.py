from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def login_required(view_func):
    '''判断登录装饰器'''
    def wrapper(request, *viewargs, **viewkwargs):
        if request.session.has_key('islogin'):
            return view_func(request, *viewargs, **viewkwargs)
        else:
            return redirect(reverse('user:login'))
    return wrapper
