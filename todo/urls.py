from django.urls import path, include

from rest_framework.routers import DefaultRouter

from todo.views import UserRegisterAPIView, CreateTokenView, UserProfileView, TaskViewSet


app_name = 'todo'

router = DefaultRouter()
router.register('task', TaskViewSet)

urlpatterns = [
    path("user/register/", UserRegisterAPIView.as_view(), name="register"),
    path("user/login/", CreateTokenView.as_view(), name="login"),
    path("user/profile/", UserProfileView.as_view(), name="profile"),
    
    path("", include(router.urls)),    
]