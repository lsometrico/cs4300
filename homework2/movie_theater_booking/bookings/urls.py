from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from . import views
from .views import MovieViewSet, SeatViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # HTML pages
    path('', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/book/', views.book_seat_page, name='book_seat'),
    path('history/', views.booking_history, name='booking_history'),
    path('logout/', LogoutView.as_view(next_page='movie_list'), name='logout'),

    # JSON API (kept under /api/ so the two never collide)
    path('api/', include(router.urls)),
]