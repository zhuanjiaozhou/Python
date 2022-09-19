from email import message
from django.contrib import admin
from  jobs.models import Job, Resume
from interview.models import Candidate
from datetime import datetime
from django.contrib import messages
from django.utils.html import format_html
# Register your models here.

class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'create_date', 'modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'create_date', 'modified_date')

    def save_model(self, request,  obj,  form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Job, JobAdmin)

def enter_interviewer_process(modeladmin, request, queryset):
    candidates_names = ""
    for resume in queryset:
        candidate = Candidate()
        # 把obj 对象中的所有属性拷贝到candidate对象中:
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date =datetime.now()
        candidates_names = candidate.username + "," + candidates_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已经成功进入面试流程' % (candidates_names))

enter_interviewer_process.short_description = u'进入面试流程'

class ReusumeAdmin(admin.ModelAdmin):

    actions = (enter_interviewer_process, )

    def image_tag(self, obj):              
        if obj.picture:
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'image_tag',  'major', 'created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date')

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience","project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Resume, ReusumeAdmin)