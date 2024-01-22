from django.urls import path
from spons_app.views.admin_views import *
from spons_app.views.user_views import *

urlpatterns = [
    path('createevent/', CreateEventView.as_view()),
    path('deleteevent/',DeleteEventView.as_view()),
    path('updateevent/<int:event_id>/',UpdateEventView.as_view()),
    path('createcompany/', CreateCompanyView.as_view()),
    path('deletecompany/',DeleteCompanyView.as_view()),
    path('updatecompany/<int:company_id>/',UpdateCompanyView.as_view()),
    path('createpoc/', CreatePOCView.as_view()),
    path('deletepoc/',DeletePOCView.as_view()),
    path('updatepoc/<int:POC_id>/',UpdatePOCView.as_view()),
    path('addmoney/',AddMoneyView.as_view()),
    path('displaymoney/',DisplayMoney.as_view())
]