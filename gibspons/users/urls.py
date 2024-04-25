from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView,LoginView,LogoutView,CreateOrganisationView,JoinOrganisationView,DeleteUserView,ChangeRoleView,UpdateDisplayUserView,ApproveView, CheckView,DisplayAllUsersView,ResetPasswordView,VerifyResetPasswordOTPView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('check', CheckView.as_view(),name="check"),
    path('register/', RegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name="logout"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password"),
    path("verify_reset_password_otp/",VerifyResetPasswordOTPView.as_view(), name="verify_reset_password_otp"),
    path('user/',UpdateDisplayUserView.as_view(),name="update_user"),
    path('user/<int:user_id>',DeleteUserView.as_view(),name="delete_user"),
    path('displayall/',DisplayAllUsersView.as_view(),name="display_all_users"),
    path('approve/',ApproveView.as_view(),name="approve_user"),
    path('changerole/',ChangeRoleView.as_view(),name="change_role"),
    path('createorg/',CreateOrganisationView.as_view(),name="create_organisation"),
    path('joinorg/',JoinOrganisationView.as_view(),name="join_organisation"),

]