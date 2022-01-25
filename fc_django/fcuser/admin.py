from django.contrib import admin
from .models import Fcuser
# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display= ('email',)

    # 목록 제목명 바꾸기할때 사용
    def changelist_view(self,request,extra_context=None):
        # 우리가 원하는 작업후 돌려놓기
        extra_context ={ 'title' : '사용자 목록'}
        return super().changelist_view(request, extra_context)
        
    # 상세 해당 물품 수정할때 나오는 제목 바꿀때 사용
    def changeform_view(self,request, object_id=None, form_url='',extra_context=None):
        fcuser = Fcuser.objects.get(pk=object_id)
        extra_context ={ 'title' : f'{fcuser.email} 수정'}
        return super().changeform_view(request, object_id, form_url,extra_context)

admin.site.register(Fcuser,FcuserAdmin)

#커스텀마이징
admin.site.site_header= "관리자 홈페이지"
admin.site.index_title = '어드민관리'
admin.site.site_title = '개발중'