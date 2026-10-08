#bookings app serializer to convert data into JSON/XML formats for REST framework
from rest_framework import serializers 
from .models import Movie, Seat, Booking

#movie serializer 
class MovieSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.username')
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
    class Meta: 
        model = Booking 
        fields = ['id','movie', 'seat', 'user', 'booking_date']
    
    #will reject already taken seats using the validation error   
    def validate_seat(self, seat):
        if seat.booking_status:
            raise serializers.ValidationError('This seat is already booked. ')
        return seat 
