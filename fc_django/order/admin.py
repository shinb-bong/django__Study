from django.db.models import Q
import datetime
# 최근활동을 남기고싶음
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Order
from django.db import transaction
from django.utils.html import format_html
from django.urls import path
# Register your models here.

# 체크한 모델들이 queryset에 들어옴 // 또한 환불을 하면 재고를 돌려줘야함.
def refund(modeladmin,request,queryset):
    with transaction.atomic():
        # 조회하는것부터 transaction 안에 넣어준다.
        qs = queryset.filter(~Q(status='환불'))

        ct =  ContentType.objects.get_for_model(queryset.model)
        for obj in qs:
            obj.product.stock += obj.quantity
            obj.product.save()
            
            # 활동 남기기
            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,
                change_message='주문 환불'
            )
            
        qs.update(status='환불')

#함수니깐 이름 변경
refund.short_description ='환불로 변경'
class OrderAdmin(admin.ModelAdmin):
    # 필터 걸기
    list_filter=('status',)
    # 색상 넣기, 버튼추가
    list_display = ('fcuser', 'product','styled_status','action')
    change_list_template = 'admin/order_change_list.html'

    # 환불 기능 만들기
    actions = [
        refund
    ]

    #버튼 추가 
    def action(self, obj):
        if obj.status != '환불':
            return format_html(f'<input type="button" value= "환불" onclick="order_refund_submit({obj.id})" class = "btn btn-primary btn-sm" >')



    # 색상 넣기 함수 만들기
    def styled_status(self,obj):
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>')
        if obj.status == '결제완료':
            return format_html(f'<span style="color:green">{obj.status}</span> ')
        return obj.status

    styled_status.short_description = '상태'

    # 상세 제목명 바꾸기
    def changelist_view(self,request,extra_context=None):
        # 우리가 원하는 작업후 돌려놓기
        extra_context ={ 'title' : '주문 목록'}

        if request.method == 'POST':

            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)

                ct =  ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()
                    
                    # 활동 남기기
                    LogEntry.objects.log_action(
                        user_id = request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='주문 환불',
                        action_flag=CHANGE,
                        change_message='주문 환불'
                    )
                    
                qs.update(status='환불')
            


        return super().changelist_view(request, extra_context)

    def changeform_view(self,request, object_id=None, form_url='',extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context ={ 'title' : f"'{order.fcuser.email}'의 '{order.product.name}' 수정"}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        
        return super().changeform_view(request, object_id, form_url,extra_context)

    # 새로운 사용자 메뉴 만들기
    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/',self.date_view),   
        ]
        return date_urls + urls

    def date_view(self,request):
        # 최근 일주일 데이터 가지고오기
        week_date = datetime.datetime.now() - datetime.timedelta(days =7 )
        week_data = Order.objects.filter(register_date__gte = week_date)
        data = Order.objects.filter(register_date__lt = week_date)

        context = dict(
            self.admin_site.each_context(request),
            week_data = week_data,
            data=data
        )
        return TemplateResponse(request,'admin/order_date_view.html',context)
admin.site.register(Order, OrderAdmin)
