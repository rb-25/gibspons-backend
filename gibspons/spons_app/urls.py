from django.urls import path
from .views.organisation import DisplayOrganisationView
from .views.event import CreateEventView, UpdateDeleteEventView,DisplayEventView
from .views.sponsorship import AddAcceptedView,DisplaySponsorsEventView,DisplayUserCompanyView,UpdateDeleteSponsorView
from .views.company import CreateDisplayCompanyView,UpdateDeleteCompanyView
from .views.poc import CreateDisplayPOCView,UpdateDeletePOCView
from .views.leaderboard_views import LeaderboardView,StatusPieChartView
from .views.ai import EmailGeneratorView,LinkedInGeneratorView


urlpatterns = [
    
    path('organisation/',DisplayOrganisationView.as_view(),name="display organisation"),
    path('event/display/',DisplayEventView.as_view(), name='display_event'),    
    path('event/', CreateEventView.as_view(), name='create_event'),
    path('event/<int:event_id>/',UpdateDeleteEventView.as_view(), name='update_delete_event'), 
    path('company/', CreateDisplayCompanyView.as_view(), name='create_company'),
    path('company/<int:company_id>/',UpdateDeleteCompanyView.as_view(), name='update_delete_company'),
    path('poc/', CreateDisplayPOCView.as_view(), name='create_display_poc'),
    path('poc/<int:POC_id>/',UpdateDeletePOCView.as_view(), name='update_delete_poc'), 
    path('addsponsor/',AddAcceptedView.as_view()),
    path('sponsors/',DisplaySponsorsEventView.as_view(), name='display_sponsor_event'),
    path('sponsor/<int:sponsor_id>/',UpdateDeleteSponsorView.as_view(), name='update_sponsor'),
    path('usercompany/',DisplayUserCompanyView.as_view(), name='display_user_sponsors'),
    path('leaderboard/',LeaderboardView.as_view(),name="leaderboard"),
    path('piechart/',StatusPieChartView.as_view(),name="status_pie_chart"),
    path('generateemail/',EmailGeneratorView.as_view(),name="generate_email"),
    path('generatelinkedin/',LinkedInGeneratorView.as_view(),name="generate_linkedin")  
    
]