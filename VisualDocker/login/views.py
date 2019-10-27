from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

# Create your views here.

def index(request):
    return render(request,'login/index.html')


def login(request):
    return JsonResponse({'msg':'success','ip':request.GET['ip'],'port':request.GET['port']})