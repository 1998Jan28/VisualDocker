from django.urls import path
from . import views

app_name = 'network'   # 命名空间

urlpatterns = [
    path('list/',views.networkList,name="networkList"),
    path('info/',views.networkInfo,name="networkInfo"),
]