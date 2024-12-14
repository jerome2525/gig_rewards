from django.urls import path
from .views import RegisterView, LoginView, FetchAxieDataView, GetAxieDataView, AxieContractView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration endpoint
    path('login/', LoginView.as_view(), name='login'),          # User login endpoint
]

urlpatterns += [
    path('fetch-axie-data/', FetchAxieDataView.as_view(), name='fetch-axie-data'),  # Endpoint to fetch Axie data
]

urlpatterns += [
    path('get-axie-data/', GetAxieDataView.as_view(), name='get-axie-data'),  # Endpoint to get stored Axie data
]

urlpatterns += [
    path('get-smart-contract-data/', AxieContractView.as_view(), name='get-smart-contract-data'),  # Endpoint to get smart contract data
]