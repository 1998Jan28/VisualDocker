from django.urls import path
from . import views

app_name = 'image'   # 命名空间

urlpatterns = [
    path('',views.index,name="index"),
    path('list/',views.imageList,name="imageList"),
    path('info/',views.imageInfo,name="imageInfo"),
    path('pull/', views.imagePull, name="imagePull"),
    path('remove/', views.imageRemove, name="imageRemove"),
]