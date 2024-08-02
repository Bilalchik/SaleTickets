from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('event_detail/<int:pk>/', views.event_detail_view, name='detail'),
    path('profile', views.user_profile_view, name='profile'),
    path('event_list/', views.event_list_view, name='list'),
    path('event_create/', views.event_create_view, name='create'),
    path('test_list/', views.EventListView.as_view()),
    path('test-detail/<int:pk>/', views.EventDetailView.as_view())
]
