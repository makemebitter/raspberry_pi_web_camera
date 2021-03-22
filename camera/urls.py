from django.urls import path
from . import views
urlpatterns = [
    path('', views.video_feed, name='camera'),
    # path('stop/', views.video_stop, name='camera_stop'),
    # path('start/', views.video_start, name='camera_start'),
]