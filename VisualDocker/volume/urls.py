from django.urls import path
from . import views

app_name = 'volume'   # 命名空间

urlpatterns = [
    path('list/',views.volumeList,name="volumeList"),
    path('info/',views.volumeInfo,name="volumeInfo"),
]