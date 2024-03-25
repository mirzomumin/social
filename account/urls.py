from django.contrib.auth import views as auth_views
from django.urls import path

from account import views

urlpatterns = [
    # path('sign-in/', views.user_signin, name='sign_in'),
    path("sign-in/", auth_views.LoginView.as_view(), name="sign_in"),
    path("sign-out/", auth_views.LogoutView.as_view(), name="sign_out"),
    path("", views.dashboard, name="dashboard"),
]
