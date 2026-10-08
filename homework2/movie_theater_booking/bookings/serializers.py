#bookings app serializer to convert data into JSON/XML formats for REST framework
from rest_framework import serializers 
from .models import Movie, Seat, Booking

#movie serializer 
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','title', 'description', 'release_date', 'duration']

#seat serializer 
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id','seat_number', 'booking_status']    

#user serializer; the user is set from the log-in request not from the client 
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date']
        read_only_fields = ['booking_date']
