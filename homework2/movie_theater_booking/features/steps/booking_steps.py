"""Step definitions for features/booking.feature (uses Django's test client)."""
from datetime import date

from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse

from bookings.models import Movie, Seat
from bookings.services import book_seat


@given('a movie "{title}" with seats "{first}" and "{second}"')
def step_movie_and_seats(context, title, first, second):
    Movie.objects.create(title=title, description='Test.',
                         release_date=date(2024, 3, 1), duration=120)
    Seat.objects.create(seat_number=first)
    Seat.objects.create(seat_number=second)


@given('I am logged in as "{name}"')
def step_login(context, name):
    context.user = get_user_model().objects.create_user(name, password='pw12345')
    context.test.client.login(username=name, password='pw12345')


@given('I have booked seat "{seat}" for "{title}"')
def step_already_booked(context, seat, title):
    book_seat(context.user, Movie.objects.get(title=title),
              Seat.objects.get(seat_number=seat).id)


@when('I book seat "{seat}" for "{title}"')
def step_book(context, seat, title):
    movie = Movie.objects.get(title=title)
    context.response = context.test.client.post(
        reverse('book_seat', args=[movie.id]),
        {'seat': Seat.objects.get(seat_number=seat).id}, follow=True)


@then('I see "{text}"')
def step_see(context, text):
    assert text in context.response.content.decode(), f'Expected {text!r} on the page'


@then('seat "{seat}" is no longer offered for "{title}"')
def step_not_offered(context, seat, title):
    movie = Movie.objects.get(title=title)
    seat_id = Seat.objects.get(seat_number=seat).id
    page = context.test.client.get(reverse('book_seat', args=[movie.id])).content.decode()
    assert f'value="{seat_id}"' not in page, f'Seat {seat} is still offered'