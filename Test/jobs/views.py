from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# Create your views here.
from django.http import Http404

from jobs.models import Job, Resume
from jobs.forms import ResumeForm
from jobs.models import Cities, JobTypes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
import html

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.contrib.auth.models import Group, User
import logging

logger = logging.getLogger(__name__)

# 这个 URL 仅允许有 创建用户权限的用户访问
@permission_required('auth.user_add')
def create_hr_user(request):
    if request.method == "GET":
        return render(request, 'create_hr.html', {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        hr_group = Group.objects.get(name='hr') 
        user = User(is_superuser=False, username=username, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user.groups.add(hr_group)

        messages.add_message(request, messages.INFO, 'user created %s' % username)
        return render(request, 'create_hr.html')
    return render(request, 'create_hr.html')

def joblist(request):
    job_list =  Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {'job_list':job_list}

    for job in job_list:
        print(job.job_type)
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]
    
    return render(request, 'joblist.html', context)

def detail(requset,job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        logger.info('job info fetched form database jobid:%s' % job_id)
    except job.DoseNotExist:
        raise Http404("Job dode not exist")

    return render(requset, 'job.html', {'job': job} )

class ResumeDetailView(DetailView):
    """简历详情页"""
    model = Resume
    template_name = 'resume_detail.html'

def detail_resume(request, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br>  introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        return HttpResponse(html.escape(content))
    except Resume.DoesNotExist:
        raise Http404("resume does not exist")

class ResumeCreateView(LoginRequiredMixin, CreateView):
    """ 简历职位页面 """
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone", "email", "apply_position", "gender", "bachelor_school", "master_school", "major", "degree", "picture", "attachment", "candidate_introduction","work_experience", "project_experience"]


    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    # 从URL请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 建立和当前用户关联
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())