from django.contrib.auth import views as auth_views
from django.urls import include, path

from account import views

urlpatterns = [
    # path('sign-in/', views.user_signin, name='sign_in'),
    # sign in/out urls
    # path("sign-in/", auth_views.LoginView.as_view(), name="sign_in"),
    # path("sign-out/", auth_views.LogoutView.as_view(), name="sign_out"),
    # # password change urls
    # path("password-change/",
    #      auth_views.PasswordChangeView.as_view(),
    #      name="password_change"),
    # path("password-change/done/",
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name="password_change_done"),
    # reset password urls
    # path("password-reset/",
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path("password-reset/done/",
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path("password-reset/<uidb64>/<token>/",
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path("password-reset/complete/",
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
    path("", include("django.contrib.auth.urls")),
    # dashboard url
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
]
