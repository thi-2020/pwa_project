from django.urls import path, include
from posts import views








urlpatterns = [
    path('own_post/<int:pk>/', views.OwnPostView.as_view(), name='own-post'),
    path('others_post/<int:pk>/', views.OtherPostView.as_view(), name='others-post'),




    

]
