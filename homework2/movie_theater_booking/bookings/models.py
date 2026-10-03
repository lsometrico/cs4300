from django.db import models

# Create your models here.

#models for the booking app: includes movie, seat and booking 

#movie model that displays information about it (namely: title, description, release date n duration)
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()

#model for the seating configuration 
class Seat(models.Model):
    seat_number = models.CharField(max_length=2) #seat number and row much like theaters nowaday
    booking_status = models.BooleanField()

#model for the booking of the seat itself
class Booking()