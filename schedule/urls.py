from django.urls import path
from . import views


app_name = 'schedule'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('schedule-list', views.schedule_index, name="schedule_list"),
    path('schedule-detail/<int:pk>/', views.ScheduleDetailView.as_view(), name="schedule_detail"),
    path('schedule-create/', views.ScheduleCreateView.as_view(), name="schedule_create"),
    path('schedule-update/<int:pk>/', views.ScheduleUpdateView.as_view(), name="schedule_update"),
    path('schedule-delete/<int:pk>/', views.ScheduleDeleteView.as_view(), name="schedule_delete"),
    path('reaction-create/<int:pk>/', views.ReactionCreateView.as_view(), name="reaction_create"),
    path('reaction-update/<int:pk>/', views.ReactionUpdateView.as_view(), name="reaction_update"),
]