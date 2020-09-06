from django.urls import path, include
from accounts import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt







urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='account-create'),

    #invitation
    path('send_invitation/', views.SendInvitation.as_view(), name='send_invitation'),
    path('get_invitations_left/', views.InvitationLeft.as_view(), name='get_invitations_left'),
    path('check_invitation/', views.CheckInvitation.as_view(), name='check_invitation'),
    path('testemail/', views.testemail, name='testemail'),
    path('deleteconnection/', views.deleteconnection, name='testemail'),


    #friendship
    path('friend/requests/', views.GetReceivedFriendRequestList.as_view(), name='get_received_friend_requests_list'),
    path('friend/mutual_connections/', views.GetMutualConnectionList.as_view(), name='mutual_connections'),
    path('friend/all_friends/', views.GetAllFriendsList.as_view(), name='all_friends'),
    path('friend/handle_request/', views.HandleFriendRequest.as_view(), name='handle_request'),
    path('friend/send_request/', views.SendFriendRequest.as_view(), name='send_request'),

    #search
    path('search/', views.SearchBarResults.as_view(), name='search'),
    
    #profile_api
    path('get_profile_info/',views.GetProfileInfo.as_view(), name='get_profile_info'),
    path('get_other_profile_info/',views.GetOtherProfileInfo.as_view(), name='get_other_profile_info'),

]
