from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response 

from .models import Movie, Seat, Booking 
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from .services import book_seat, SeatUnavailable
# Create your views here.

#movie view for the set. On Movies, this is the full CRUD stuff 
class MovieViewSet(viewsets.ModelViewSet):
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

#display the seat availablity, with the ability to filter thru available seats 
class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all().order_by('seat_number')
    serializer_class = SeatSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('available') == 'true':
                qs = qs.filter(booking_status=False)
        return qs
            
            
#make sure that users can onl see their own bookings and also create new ones 
#also lock up the seat once someone takes it 

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    
    def get_queryset(self):
            if not self.request.user.is_authenticated:
                return Booking.objects.none()
            return Booking.objects.filter(user=self.request.user).order_by('-booking_date')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = book_seat(
                request.user,
                serializer.validated_data['movie'],
                serializer.validated_data['seat'].id,
            )
        except SeatUnavailable as e:
            return Response({'seat': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)
    
# ---------------------------------------------------------------
# Template (HTML) views. These render pages instead of JSON, but
# they use the same models and the same book_seat() service as the API.
# ---------------------------------------------------------------

def movie_list(request):
    """Show every movie, each with a button to book a seat."""
    movies = Movie.objects.all().order_by('title')
    return render(request, 'bookings/movie_list.html', {'movies': movies})


@login_required
def book_seat_page(request, movie_id):
    """Show available seats for a movie and handle the booking form."""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        try:
            book_seat(request.user, movie, request.POST.get('seat'))
        except SeatUnavailable as e:
            messages.error(request, str(e))
        except (Seat.DoesNotExist, ValueError):
            messages.error(request, 'Please choose a valid seat.')
        else:
            messages.success(request, f'Seat booked for {movie.title}!')
            return redirect('booking_history')

    seats = Seat.objects.filter(booking_status=False).order_by('seat_number')
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})


@login_required
def booking_history(request):
    """Show only the logged-in user's bookings, newest first."""
    bookings = (Booking.objects.filter(user=request.user)
                .select_related('movie', 'seat')
                .order_by('-booking_date'))
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

    