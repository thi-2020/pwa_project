from django.urls import path, include
from posts import views








urlpatterns = [



    #post
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('update_post/', views.UpdatePost.as_view(), name='update_post'),
    path('delete_post/', views.DeletePost.as_view(), name='delete_post'),
    path('get_post/', views.GetPost.as_view(), name='get_post'),
    path('update_comments_status_on_post/', views.UpdatePostCommentSettings.as_view(), name='update_status'),

    #feed
    path('self_time_line/', views.SelfTimeline.as_view(), name='self_time_line'),
    path('others_time_line/', views.OthersTimeLine.as_view(), name='others_time_line'),
    path('news_feed/', views.NewsFeed.as_view(), name='news_feed'),


    #like
    path('likes/like_a_post/', views.LikePost.as_view(), name='like_a_post'),
    path('likes/unlike_a_post/', views.UnlikePost.as_view(), name='unlike_a_post'),
    path('likes/list_of_likes_on_post/', views.LikesList.as_view(), name='list of likes on post'),

    #comment
    path('comments/create_comment/', views.CreateComment.as_view(), name='create_comment'),
    path('comments/update_comment/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/delete_comment/', views.DeleteComment.as_view(), name='delete_comment'),
    path('comments/list_of_comments_on_post/', views.CommentsList.as_view(), name='list of comments on post'),
    

]
