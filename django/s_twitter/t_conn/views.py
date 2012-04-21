# Create your views here.
from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('hello t_conn test')

