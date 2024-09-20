from django.urls import path
from knox.views import LogoutAllView, LogoutView
from apps.auth_app.views import LoginView, UserViewSet

urlpatterns = [
    path('user/login', LoginView.as_view(), name='auth_user_login_create'),
    path('user/logout', LogoutView.as_view(), name='auth_user_logout_create'),
    path('users', UserViewSet.as_view(
        {'get': 'list','post': 'create'}
    ), name='auth_users_management'),
    path('users/<id>', UserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update',
         }), name='auth_users_cms')
]
