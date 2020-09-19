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
   


    #connections
    path('connection/requests/', views.GetReceivedConnectionRequestList.as_view(), name='get_received_connection_requests_list'),
    path('connection/mutual_connections/', views.GetMutualConnectionList.as_view(), name='mutual_connections'),
    path('connection/all_connections/', views.GetAllConnectionsList.as_view(), name='all_connections'),
    path('connection/others_all_connections/', views.GetOthersAllConnectionsList.as_view(), name='others_all_connections'),
    path('connection/handle_request/', views.HandleConnectionRequest.as_view(), name='handle_request'),
    path('connection/send_request/', views.SendConnectionRequest.as_view(), name='send_request'),
    path('connection/delete_connection/', views.DeleteConnection.as_view(), name='delete_connection'),
    path('connection/sent_requests_list/', views.GetSentConnectionRequestList.as_view(), name='sent_requests_list'),
    #todeliver
    
    path('connection/withdraw_request/', views.WithdrawRequest.as_view(), name='withdraw_request'),
    

    

    #followers

    path('follow/follwers_list/', views.GetAllFollowersList.as_view(), name='get_received_friend_requests_list'),
    path('follow/follwing_list/', views.GetAllFollowingList.as_view(), name='mutual_connections'),
    path('friend/follow_person/', views.GetAllConnectionsList.as_view(), name='all_friends'),
    path('friend/unfollow_person/', views.HandleConnectionRequest.as_view(), name='handle_request'),
    path('friend/remove_a_follower/', views.HandleConnectionRequest.as_view(), name='handle_request'),



    #search
    path('search/', views.SearchBarResults.as_view(), name='search'),
    
    #profile_api
    path('profile/get_profile_info/',views.GetProfileInfo.as_view(), name='get_profile_info'),
    path('profile/get_other_profile_info/',views.GetOtherProfileInfo.as_view(), name='get_other_profile_info'),
            
    path('profile/update_profile_photo/',views.UpdateProfilePhoto.as_view(), name='update_profile_photo'),
    path('profile/delete_profile_photo/',views.DeleteProfilePhoto.as_view(), name='delete_profile_photo'),
    path('profile/update_cover_photo/',views.UpdateCoverPhoto.as_view(), name='update_cover_photo'),
    path('profile/delete_cover_photo/',views.DeleteCoverPhoto.as_view(), name='delete_cover_photo'),

    # to do
    path('profile/update_profile_info/',views.UpdateProfilePhoto.as_view(), name='get_other_profile_info'),


    #settings
    path('settings/visibility_options/',views.VisibilitySettingsOptionsList.as_view()),
    path('settings/get_visibility_settings/',views.VisibilitySettingsGet.as_view()),
    path('settings/update_visibility_settings/',views.VisibilitySettingsUpdate.as_view()),
    path('settings/update_visibilty_settings_table/',views.update_visibilty_settings),
]
