from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'), 
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('search-flights/', views.search_flights, name='search_flights'),
]
