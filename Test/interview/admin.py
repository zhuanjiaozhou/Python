from asyncio.log import logger
import encodings
from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils.safestring import mark_safe
# from interview.dingtalk import send
from .tasks import send_dingtalkmessage

# Register your models here.
from interview.models import Candidate
from interview.candidate_fieldset import default_fieldsets, default_fieldsets_first, default_fieldsets_second
from interview import dingtalk

import logging
import csv
from datetime import datetime

from jobs.models import Resume


logger = logging.getLogger(__name__)

exporttabale_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                       'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')

#通知一面面试官
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    print(queryset)
    for obj in  queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
        #dingtalk.send("候选人 %s 进入面试环节， 亲爱的面试官， 请准备好面试: %s" % (candidates, interviewers))
    send_dingtalkmessage.delay("候选人 %s 进入面试环节， 亲爱的面试官， 请准备好面试: %s" % (candidates, interviewers))
    messages.add_message(request, messages.INFO, '已经成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'

def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response.charset = 'utf-8-sig' if "Windows" in request.headers.get(
        'User-Agent') else 'utf-8'

    field_list = exporttabale_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-cadidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%D-%H-%M-%S'),)
    ### 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title()
         for f in field_list],
    )

    for obj in queryset:
        ### 单行记录，写入csv文件
        csv_line_valuse = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_valuse.append(field_value)
        writer.writerow(csv_line_valuse)

    logger.error("%s exported %s candidate records" %
                (request.user, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions =('export',)

## 候选人管理
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'create_date', 'modified_date')

    actions = (export_model_as_csv, notify_interviewer,)

    ### 当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        print(opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    list_display = ('username', 'city', 'bachelor_school', 'get_resume','first_score', 'first_result', 'first_interviewer_user',
                    'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor')

    ## 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user',
                   'second_interviewer_user', 'hr_interviewer_user', 'last_editor')

    #查询字段
    search_fields = ['username', 'phone', 'email', 'bachelor_school']

    ordering = ('hr_result', 'second_result', 'first_result')

    def get_resume(selg, obj):
        if not obj.phone:
            return ""
        resumes =  Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a>' % (resumes[0].id, "查看简历"))
        return ""
    get_resume.short_description = u'查看简历'

    ##指定可编辑字段
    ###list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    ## 覆盖父类方法
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)
    
    # 拿到分组数据
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    ## 设置数据权限: 对于非管理员， 非HR, 获取自己是一面面试官或者二面面试官的候选人集合:
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    ## 设置为只读
    ### readonly_fields = ('first_interviewer_user', 'second_interviewer_user',)
    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s " %
                        request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    #一面面试官仅填写一面反馈， 二面面试官仅填写二面反馈
    def get_fieldsets(self, request, obj):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets


admin.site.register(Candidate, CandidateAdmin)
