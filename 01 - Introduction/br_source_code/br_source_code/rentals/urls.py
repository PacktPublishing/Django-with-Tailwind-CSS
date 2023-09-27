from django.urls import path
from .views import (
    search_book_view, 
    BookRentalHistoryView, 
    UpdateRentalStatusView,
    CreateNewRentalView,
    SelectDownloadRentalsView
)

app_name = 'rentals'

urlpatterns = [
    path('', search_book_view, name='main'),
    path('<str:book_id>/', BookRentalHistoryView.as_view(), name="detail"),
    path('<str:book_id>/new/', CreateNewRentalView.as_view(), name="new"),
    path('<str:book_id>/download/', SelectDownloadRentalsView.as_view(), name="download"),
    path('<str:book_id>/<pk>/', UpdateRentalStatusView.as_view(), name="update"),
]
