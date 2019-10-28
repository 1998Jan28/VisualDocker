from django.urls import path
from . import views

app_name = 'login'   # 命名空间

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name="login"),
    path('clientInfo/',views.getClientInfo,name="getClientInfo"),
]