from asyncio.log import logger
import encodings
from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from interview.models import Candidate

import logging
import csv
from datetime import datetime


logger = logging.getLogger(__name__)

exporttabale_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer', 'second_result', 'second_interviewer', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer')

def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type = 'text/csv')
    response.charset = 'utf-8-sig' if "Windows" in request.headers.get('User-Agent') else 'utf-8'

    field_list = exporttabale_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-cadidates-list-%s.csv' %(datetime.now().strftime('%Y-%m-%D-%H-%M-%S'),)
    ### 写入表头
    writer =  csv.writer(response)
    writer.writerow(
        [ queryset.model._meta.get_field(f).verbose_name.title() for f in field_list ],
    )

    for obj in queryset:
        ### 单行记录，写入csv文件
        csv_line_valuse = []
        for field in field_list:
            field_object =  queryset.model._meta.get_field(field)
            field_value =   field_object.value_from_object(obj)
            csv_line_valuse.append(field_value)
        writer.writerow(csv_line_valuse)
    
    logger.info("%s exported %s candidate records" % (request.user, len(queryset) ))

    return response

export_model_as_csv.short_description = u'导出为CSV文件'

## 候选人管理
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'create_date', 'modified_date')

    actions = (export_model_as_csv,)

    list_display = ('username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor')

    
    ## 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user', 'last_editor')

    #查询字段
    search_fields = ['username', 'phone', 'email', 'bachelor_school'] 
    
    ordering = ('hr_result', 'second_result', 'first_result')

    ##指定可编辑字段
    ###list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user','second_interviewer_user',)
        return ()
    
    ## 覆盖父类方法
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)
        # return super().get_changelist_instance(request)

    ## 设置为只读
    ### readonly_fields = ('first_interviewer_user', 'second_interviewer_user',)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names        

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s " % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    # 分组显示
    fieldsets = (
        (None, {'fields': ("userid", ("username","city","phone"),("email","apply_position","born_address"),("gender","candidate_remark"),("bachelor_school","master_school","doctor_school"),("major","degree"),("test_score_of_general_ability","paper_score"),"last_editor",)}),
        ('第一轮面试记录', {'fields': (("first_score"),("first_learning_ability","first_professional_competency"),"first_advantage","first_disadvantage","first_result","first_recommend_position","first_interviewer_user","first_remark",)}),
        ('第二轮面试记录', {'fields': (("second_score"),("second_learning_ability","second_professional_competency"),("second_pursue_of_excellence","second_communication_ability","second_pressure_socre"),"second_advantage","second_disadvantage","second_result","second_recommend_position","second_interviewer_user","second_remark",)}),
        ('第三轮面试记录', {'fields': ("hr_score",("hr_responsibility","hr_communication_ability","hr_logic_ability"),("hr_poentail","hr_stability"),"hr_advantage","hr_disadvantage","hr_result","hr_interviewer_user","hr_remark",)}),
    )


admin.site.register(Candidate, CandidateAdmin)