
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from fcuser.decorators import login_required
from .models import Order
from django.db import transaction
from product.models import Product
from fcuser.models import Fcuser

# Create your views here.
@method_decorator(login_required, name ='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/'+str(form.data.get('product')))

    # 어떤 인자값을 줘서 Form을 만들껀지 결정
    def get_form_kwargs(self,**kwrags): 
        kw = super().get_form_kwargs(**kwrags)
        kw.update({
            'request': self.request    
        })
        return kw

    def form_valid(self,form):
    # transaction -> 주문이 들어가면서 상품의 재고도 조절하는 기능을 만들거임
        # 이 기능은 동시 다발적으로 이루어지며 하나라도 안되면 오류를 띄움
        with transaction.atomic():
            prod =Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity =form.data.get( 'quantity'),
                product= prod, #pk가 입력받은 물건일때
                fcuser = Fcuser.objects.get(email=self.requset.session.get('user'))

            )
            order.save()
            prod.stock -=int(form.data.get('quantity'))
            prod.save()

        return super().form_valid(form)


@method_decorator(login_required, name ='dispatch')
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    # 이렇게 하면 다른사람이 주문한것 까지 다보인다 그러므로 개인화할려면
    # 현재 로그인한 사용자의 queryset만 가져온다.

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
        return queryset
    
        

