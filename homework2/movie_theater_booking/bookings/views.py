from django.shortcuts import render
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
    https_method_names = ['get', 'post', 'delete', 'head', 'options']
    
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
        

    