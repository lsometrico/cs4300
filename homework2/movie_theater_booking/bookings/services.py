#the booking logic so that both API and HTML can share info 
from django.db import transaction
from .models import Seat, Booking

class SeatUnavailable(Exception):
    """Raised when someone tries to book an already taken seat"""

def book_seat(user, movie, seat_id):
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(id=seat_id)
        if seat.booking_status:
            raise SeatUnavailable("This seat is already taken.")
        seat.booking_status = True
        seat.save()
        return Booking.objects.create(user=user, movie=movie, seat=seat)