from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView,LoginView,LogoutView,CreateOrganisationView,JoinOrganisationView,DeleteUserView,ChangeRoleView,UpdateDisplayUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name="logout"),    
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('changerole/',ChangeRoleView.as_view(),name="change_role"),
    path('user/',UpdateDisplayUserView.as_view(),name="update_user"),
    path('user/<int:user_id>',DeleteUserView.as_view(),name="delete_user"),
    path('createorg/',CreateOrganisationView.as_view(),name="create_organisation"),
    path('joinorg/',JoinOrganisationView.as_view(),name="join_organisation"),

]