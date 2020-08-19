from django.urls import path, include
from accounts import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt







urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='account-create'),
    path('send_invitation/', views.SendInvitation.as_view(), name='send_invitation'),
    path('get_invitations_left/', views.InvitationLeft.as_view(), name='get_invitations_left'),
    path('check_invitation/', views.CheckInvitation.as_view(), name='check_invitation'),
    path('testemail/', views.testemail, name='testemail'),
    path('deleteconnection/', views.deleteconnection, name='testemail'),


    #friendship
    path('friend/requests/', views.GetFriendRequestList.as_view(), name='get_friend_requests_list'),
    path('friend/mutual_connections/', views.GetMutualConnectionList.as_view(), name='mutual_connections'),
    path('friend/all_friends/', views.GetAllFriendsList.as_view(), name='all_friends'),
    
    

]
