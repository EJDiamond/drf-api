from follower import views
from django.urls import path

urlpatterns = [
    path('follower/', views.FollowerList.as_view()),
    path('follower/<int:pk>/', views.FollowerDetail.as_view()),
]