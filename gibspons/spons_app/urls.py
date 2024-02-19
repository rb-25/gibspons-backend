from django.urls import path
from .views.admin_views import CreateEventView, UpdateDeleteEventView,AddSponsorView
from .views.user_views import CreateDisplayCompanyView,UpdateDeleteCompanyView,CreateDisplayPOCView,UpdateDeletePOCView,DisplaySponsorsEventView,DisplayEventView
from .views.leaderboard_views import LeaderboardView,StatusPieChartView
from .views.ai_views import EmailGeneratorView,LinkedInGeneratorView


urlpatterns = [
    
    path('event/display/',DisplayEventView.as_view(), name='display_event'),    
    path('event/', CreateEventView.as_view(), name='create_event'),
    path('event/<int:event_id>/',UpdateDeleteEventView.as_view(), name='update_delete_event'), 
    path('company/', CreateDisplayCompanyView.as_view(), name='create_company'),
    path('company/<int:company_id>/',UpdateDeleteCompanyView.as_view(), name='update_delete_company'),
    path('poc/', CreateDisplayPOCView.as_view(), name='create_display_poc'),
    path('poc/<int:POC_id>/',UpdateDeletePOCView.as_view(), name='update_delete_poc'),   
    path('addsponsor/',AddSponsorView.as_view()),
    path('sponsors/',DisplaySponsorsEventView.as_view(), name='display_sponsor_event'),
    path('leaderboard/',LeaderboardView.as_view(),name="leaderboard"),
    path('piechart/',StatusPieChartView.as_view(),name="status_pie_chart"),
    path('generateemail/',EmailGeneratorView.as_view(),name="generate_email"),
    path('generatelinkedin/',LinkedInGeneratorView.as_view(),name="generate_linkedin")  
    
]