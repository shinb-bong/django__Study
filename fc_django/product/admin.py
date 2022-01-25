from django.contrib import admin
from .models import Product
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma
# Register your models here.


class ProductAdmin(admin.ModelAdmin) :
    list_display = ('name', 'price_format','styled_stock')

    # intcomma (humanize)를 admin에서도 templates처럼 사용가능
    def price_format(self,obj):
        price = intcomma(obj.price)
        return f'{price} 원'

    def styled_stock(self,obj):
        stock = obj.stock
        if obj.stock <= 50:
            stock = intcomma(stock)
            return format_html(f'<b><span style="color:red">{stock} 개</span></b>')
        return f'{intcomma(stock)} 개'

    price_format.short_description = '가격'
    styled_stock.short_description = '재고'
    # 상세 제목명 바꾸기
    def changelist_view(self,request,extra_context=None):
        # 우리가 원하는 작업후 돌려놓기
        extra_context ={ 'title' : '상품 목록'}
        return super().changelist_view(request, extra_context)

    def changeform_view(self,request, object_id=None, form_url='',extra_context=None):
        product = Product.objects.get(pk=object_id)
        extra_context ={ 'title' : f'{product.name} 수정'}
        return super().changeform_view(request, object_id, form_url,extra_context)



admin.site.register(Product,ProductAdmin)