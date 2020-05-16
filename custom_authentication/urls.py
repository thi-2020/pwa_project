from django.urls import path, include
from . import views







urlpatterns = [
    # path('api/', include(router.urls)),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   

]
