from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('login/', view=views.login_view, name='login'),
    # path('logout/', view=views.logout_view, name='logout' ),

    path('register/', view=views.user_creation_view, name="register"),
    path('profile/edit/', view = views.user_edit_view, name='user_edit'),


    path('login/', view=auth_views.LoginView.as_view(), name="login"),
    path('logout/', view=auth_views.LogoutView.as_view(), name="logout"),
    path('dashboard/', view=views.dashboard, name="dashboard"),
    
    # Password change password 
    path('password-change/', view=auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password-change/done/', view=auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    # Reset Password
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-link/sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]