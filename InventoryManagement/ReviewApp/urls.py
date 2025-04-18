from django.urls import path
from . import views

urlpatterns = [
     path('', views.submit_and_list_reviews, name='submit_and_list_reviews'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
