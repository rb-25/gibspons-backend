from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('registeruser/', UserRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('createorg/',CreateOrganisationView.as_view()),
    path('joinorg/',JoinOrganisationView.as_view()),
    path('changerole/',ChangeRoleView.as_view()),
    path('deleteuser/',DeleteUserView.as_view()),
]