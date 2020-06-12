from django.urls import path, include
from . import views







urlpatterns = [
    # path('api/', include(router.urls)),
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('get_post_list/', views.GetPostListView.as_view(), name='get_post_list'),
    path('get_post_detail/', views.GetPostDetailView.as_view(), name='get_post_detail'),
    path('delete_post/', views.DeletePost.as_view(), name='delete_post'),
    path('update_post/', views.UpdatePost.as_view(), name='update_post'),
    path('get_feed/', views.GetFeed.as_view(), name='get_feed'),
    # path('get_others_post_detail/', views.GetSelfPostDetailView.as_view(), name='get_post'),
    # path('get_others_post_list/', views.GetSelfPostDetailView.as_view(), name='get_post'),
   

]
