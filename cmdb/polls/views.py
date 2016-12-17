
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# from django.views import generic
from django.utils import timezone

from django.template import loader
from .models import Host, Operate, Position, User
from .forms import NameForm

def index(request):
    host_list = Host.objects.order_by('hostname')[:5]
    context = {'host_list': host_list}
    return render(request, 'polls/index.html', context)

def detail(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    return render(request, 'polls/detail.html', {'host': host})

def results(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    return render(request, 'polls/results.html', {'host': host})


def search(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        print(request.POST)
        # print(result)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(name)
            result = Host.objects.filter(hostname__contains=name).values()
            print(result)
    else:
        form = NameForm()
        # result = Host.objects.get(hostname__contains=form)

    return render(request, 'polls/search.html', {'form': form})