from django.urls import path, include
from accounts import views







urlpatterns = [
    # path('api/', include(router.urls)),
    path('test/', views.index.as_view()),
    path('createuser/', views.UserCreate.as_view(), name='account-create'),
    path('send_invitation/', views.SendInvitation.as_view(), name='send_invitation'),
    path('check_invitation/', views.CheckInvitation.as_view(), name='check_invitation'),
    path('create_test_user/', views.create_test_user),

]
