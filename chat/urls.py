from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/chat/' ,views.room, name='room'),
    #path('<int:pk>/<str:room_name>/', views.room, name='room'),
]
