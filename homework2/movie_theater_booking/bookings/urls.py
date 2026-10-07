from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet

#back end of the urls , API builds the routing so it passes to movie_theater_booking/urls.py
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('api/', include(router.urls)),
]