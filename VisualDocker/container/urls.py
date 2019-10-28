from django.urls import path
from . import views

app_name = 'container'   # 命名空间

urlpatterns = [
    path('',views.index,name="index"),
    path('list/',views.containerList,name="containerList"),
    path('info/',views.containerInfo,name="containerInfo"),
    path('run/',views.containerRun,name="containerRun"),
    path('start/',views.containerStart,name="containerStart"),
    path('stop/',views.containerStop,name="containerStop"),
    path('reload/',views.containerReload,name="containerReload"),
]