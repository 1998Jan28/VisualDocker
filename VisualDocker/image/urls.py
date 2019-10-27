from django.urls import path
from . import views

app_name = 'image'   # 命名空间

urlpatterns = [
    path('',views.index,name="index"),
]