from dataclasses import fields
from pyexpat import model
from unicodedata import name
from django.urls import re_path as url
from django.urls import path
from jobs import views
from django.conf import settings


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    # 职位列表
    # url(r"^joblist", views.joblist, name="joblist"),
    path("joblist/", views.joblist, name="joblist"),

    # 管理员创建 HR 账号的 页面:
    path('create_hr_user/', views.create_hr_user, name='create_hr_user'),

    # 职位详情
    # url(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),
    path('job/<int:job_id>/', views.detail, name='detail'),

    #提交简历
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>', views.ResumeDetailView.as_view(), name='resume-detail'),

    path('sentry-debug/', trigger_error),

    # 首页自动跳转到 职位列表
    #url(r"^$", views.joblist, name="name"),
    path("", views.joblist, name="name"),
]

if settings.DEBUG :
    # 有 XSS 漏洞的视图页面，
    urlpatterns += [path('detail_resume/<int:resume_id>', views.detail_resume, name='detail_resume'),]