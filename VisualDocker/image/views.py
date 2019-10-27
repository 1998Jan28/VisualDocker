from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

# Create your views here.

def index(request):
    return render(request,'image/imageList.html')