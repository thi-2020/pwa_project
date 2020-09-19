from django.urls import path, include
from posts import views








urlpatterns = [



    #post
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('update_post/', views.UpdatePost.as_view(), name='update_post'),
    path('delete_post/', views.DeletePost.as_view(), name='delete_post'),
    path('get_post/', views.GetPost.as_view(), name='get_post'),

    #feed
    path('self_time_line/', views.SelfTimeline.as_view(), name='self_time_line'),
    path('others_time_line/', views.OthersTimeLine.as_view(), name='others_time_line'),
    path('news_feed/', views.NewsFeed.as_view(), name='news_feed'),



    #like

]
