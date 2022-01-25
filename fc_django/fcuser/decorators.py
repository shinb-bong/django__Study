from django.shortcuts import redirect
from .models import Fcuser

def login_required(function):
    def wrap(request, *args,**kwargs):
        user = request.session.get('user')
        if user is None or not user :
            return redirect('/login/')
        return function(request, *args,**kwargs)
    return wrap


def admin_required(function) :
    def wrap(request, *args,**kwargs):
        user = request.session.get('user')
        if user is None or not user :
            return redirect('/login/')

        # 유저 정보를 가지고와야 어드민 확인가능
        user = Fcuser.objects.get(email = user)
        if user.level != 'admin':
            return redirect('/')
        return function(request, *args,**kwargs)
    return wrap