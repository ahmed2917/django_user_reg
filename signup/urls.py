from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'signup'

urlpatterns = [
    path('login/',views.SigninView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',views.UserCreate.as_view()),
    path('get/',views.UserList.as_view()),    
    path('get/<int:pk>',views.UserUpdate.as_view()),


]
