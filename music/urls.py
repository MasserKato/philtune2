from django.urls import path
from . import views


app_name = 'music'
urlpatterns = [
    path('music-list', views.MusicListView.as_view(), name="music_list"),
    path('music-detail/<int:pk>/', views.MusicDetailView.as_view(), name="music_detail"),
    path('music-create/<int:pk>/', views.MusicCreateView.as_view(), name="music_create"),
    path('music-update/<int:pk>/', views.MusicUpdateView.as_view(), name="music_update"),
    path('music-delete/<int:pk>/', views.MusicDeleteView.as_view(), name="music_delete"),
    path('stage-create/<int:pk>/', views.StageCreateView.as_view(), name="stage_create"),
    path('stage-update/<int:pk>/', views.StageUpdateView.as_view(), name="stage_update"),
    path('stage-delete/<int:pk>/', views.StageDeleteView.as_view(), name="stage_delete"),
    path('concert-create/<int:pk>/', views.ConcertCreateView.as_view(), name="concert_create"),
    path('concert-update/<int:pk>/', views.ConcertUpdateView.as_view(), name="concert_update"),
    path('concert-delete/<int:pk>/', views.ConcertDeleteView.as_view(), name="concert_delete"),
    path('term-create/', views.TermCreateView.as_view(), name="term_create"),
    path('term-update/<int:pk>/', views.TermUpdateView.as_view(), name="term_update"),
    path('term-delete/<int:pk>/', views.TermDeleteView.as_view(), name="term_delete"),
]