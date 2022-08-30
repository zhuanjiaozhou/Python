from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
from django.http import Http404

from jobs.models import Job
from jobs.models import Cities, JobTypes

def joblist(request):
    job_list =  Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {'job_list':job_list}

    for job in job_list:
        print(job.job_type)
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]
    
    return HttpResponse(template.render(context))


def detail(requset,job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except job.DoseNotExist:
        raise Http404("Job dode not exist")

    return render(requset, 'job.html', {'job':job} )