from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# from django.views import generic
from django.utils import timezone

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.template import loader
from .models import Host, Operate, Position, User
from .forms import NameForm


def index(request):
    # host_list = Host.objects.order_by('hostname')[:5]
    host_list = Host.objects.order_by('hostname')
    paginator = Paginator(host_list, 1)

    page = request.GET.get('page')
    try:
        host = paginator.page(page)
    except PageNotAnInteger:
        host = paginator.page(1)
    except EmptyPage:
        host = paginator.page(page.num_pages)
    context = {'host_list': host}
    return render(request, 'polls/index.html', context)


def detail(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    return render(request, 'polls/detail.html', {'host': host})


def results(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    return render(request, 'polls/results.html', {'host': host})


def search_form(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
    else:
        form = NameForm()
    return render(request, 'polls/search_form.html', {'form': form})


def search(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            results = Host.objects.filter(hostname__contains=name).values()
        else:
            requests = Host.objects.all()[:5]
    else:
        name = request.GET.get('name')
        results = Host.objects.filter(hostname__contains=name).values()

    paginator = Paginator(results, 1)
    page = request.GET.get('page')
    # print(page)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(page.num_pages)
    context = {'result_list': result, 'name': name}
    return render(request, 'polls/search.html', context)
