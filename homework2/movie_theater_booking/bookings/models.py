from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
# Create your models here.

#models for the booking app: includes movie, seat and booking 

#movie model that displays information about it (namely: title, description, release date n duration)
#since int can accept 0, we want to make sure there is at least 1 minute of run time 
#https://docs.djangoproject.com/en/6.1/ref/models/fields/
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration (in minutes)"
    )

    def __str__(self):
        return self.title

#model for the seating configuration 
class Seat(models.Model):
    seat_number = models.CharField(max_length=3, unique=True) #seat number and row much like theaters nowaday; no duplicates
    booking_status = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number

#model for the booking of the seat itself
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.seat}"
    