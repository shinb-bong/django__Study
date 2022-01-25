from .models import Fcuser
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm,LoginForm

# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email' : request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    # 추후 작업이기 때문에 여기로 뺄 수 있다.
    # 이것을 리팩토링이라 부르며 원래 이것은 forms.py 에서 작업했으나 여기서 타당검사
    # 이것을 하게되었을때 중복으로 생성될수 있으니
    # 원래 forms자리에서는 없는걸 예외처리해야한다. 
    def form_valid(self,form):
        fcuser = Fcuser(
            email = form.data.get('email') ,
            password = make_password(form.data.get('password')),
            level = 'user'
        )
        fcuser.save()

        return super().form_valid(form)

    

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self,form):
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')



