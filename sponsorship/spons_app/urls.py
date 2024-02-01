from django.urls import path
from .views.admin_views import CreateEventView, DeleteEventView, UpdateEventView,AddMoneyView
from .views.user_views import CreateCompanyView,DeleteCompanyView,UpdateCompanyView,CreatePOCView,DeletePOCView,UpdatePOCView,DisplaySponsorsView

urlpatterns = [    
    path('event/create/', CreateEventView.as_view()),
    path('event/delete/',DeleteEventView.as_view()),
    path('event/update/<int:event_id>/',UpdateEventView.as_view()),
    path('company/create/', CreateCompanyView.as_view()),
    path('company/delete/',DeleteCompanyView.as_view()),
    path('company/update/<int:company_id>/',UpdateCompanyView.as_view()),
    path('poc/create/', CreatePOCView.as_view()),
    path('poc/delete/',DeletePOCView.as_view()),
    path('poc/update/<int:POC_id>/',UpdatePOCView.as_view()),
    path('addmoney/',AddMoneyView.as_view()),
    path('sponsors/display',DisplaySponsorsView.as_view())
]