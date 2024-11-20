from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.organisation import DisplayOrganisationView
from .views.event import EventViewSet
from .views.sponsorship import AddAcceptedView,DisplaySponsorsEventView,DisplayUserCompanyView,UpdateDeleteSponsorView
from .views.company import CompanyViewSet
from .views.poc import POCViewSet
from .views.leaderboard_views import LeaderboardView,StatusPieChartView
from .views.ai import EmailGeneratorView,LinkedInGeneratorView

event_router=DefaultRouter()
event_router.register(r'event',EventViewSet,basename='event')
urlpatterns = event_router.urls

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
urlpatterns += router.urls

router = DefaultRouter()
router.register(r'poc', POCViewSet, basename='poc')
urlpatterns += router.urls


urlpatterns += [
    
    path('organisation/',DisplayOrganisationView.as_view(),name="display organisation"),
    path('addsponsor/',AddAcceptedView.as_view()),
    path('sponsors/',DisplaySponsorsEventView.as_view(), name='display_sponsor_event'),
    path('sponsor/<int:sponsor_id>/',UpdateDeleteSponsorView.as_view(), name='update_sponsor'),
    path('usercompany/',DisplayUserCompanyView.as_view(), name='display_user_sponsors'),
    path('leaderboard/',LeaderboardView.as_view(),name="leaderboard"),
    path('piechart/',StatusPieChartView.as_view(),name="status_pie_chart"),
    path('generateemail/',EmailGeneratorView.as_view(),name="generate_email"),
    path('generatelinkedin/',LinkedInGeneratorView.as_view(),name="generate_linkedin")  
    
]