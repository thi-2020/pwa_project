from django.urls import path, include
from accounts import views







urlpatterns = [
    # path('api/', include(router.urls)),
    path('test/', views.index.as_view()),
    path('createuser/', views.UserCreate.as_view(), name='account-create'),

]
