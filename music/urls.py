from django.urls import path
from . import views


app_name = 'music'
urlpatterns = [
    path('music-list', views.music_index, name="music_list"),
    path('music-detail/<int:pk>/', views.MusicDetailView.as_view(), name="music_detail"),
    path('music-create/', views.MusicCreateView.as_view(), name="music_create"),
    path('music-update/<int:pk>/', views.MusicUpdateView.as_view(), name="music_update"),
    path('music-delete/<int:pk>/', views.MusicDeleteView.as_view(), name="music_delete"),
    path('stage-create/<int:pk>/', views.StageCreateView.as_view(), name="stage_create"),
    path('stage-update/<int:pk>/', views.StageUpdateView.as_view(), name="stage_update"),
]