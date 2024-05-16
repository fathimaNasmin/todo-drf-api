from django.urls import path
# from .views import UserLoginAPIView
from todo.views import UserRegisterAPIView, CreateTokenView, UserProfileView
# from .views import UserLogoutAPIView

app_name = 'todo'

urlpatterns = [
    path("user/register/", UserRegisterAPIView.as_view(), name="register"),
    path("user/login/", CreateTokenView.as_view(), name="login"),
    path("user/profile/", UserProfileView.as_view(), name="profile"),
]