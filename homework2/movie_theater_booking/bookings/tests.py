"""Compact tests for the bookings app. Run with: python manage.py test"""
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Movie, Seat, Booking
from .services import book_seat, SeatUnavailable
from django.core.management import call_command
from bookings.management.commands.seed_demo import MOVIES, ROWS, SEATS_PER_ROW


User = get_user_model()


def make_data():
    """One user, one movie, two open seats."""
    user = User.objects.create_user('alice', password='pw12345')
    movie = Movie.objects.create(title='Dune', description='Sand.',
                                 release_date=date(2024, 3, 1), duration=155)
    seats = [Seat.objects.create(seat_number=n) for n in ('A1', 'A2')]
    return user, movie, seats


# Unit tests: models and the booking service going over different functionalities on the booking system 
class UnitTests(TestCase):
    def setUp(self):
        self.user, self.movie, (self.a1, self.a2) = make_data()

    def test_str_methods(self):
        booking = Booking.objects.create(user=self.user, movie=self.movie, seat=self.a1)
        self.assertEqual(str(self.movie), 'Dune')
        self.assertEqual(str(self.a1), 'A1')
        self.assertEqual(str(booking), 'alice - Dune - A1')

#make sure that the movie duration is a positive integer
    def test_movie_duration_positive(self):
        self.movie.duration = 0
        with self.assertRaises(ValidationError):
            self.movie.full_clean()

#test to check if the seat accepts duplicates and assert that it is unavailable
    def test_book_seat_duplicates(self):
        book_seat(self.user, self.movie, self.a1.id)
        self.a1.refresh_from_db()
        self.assertTrue(self.a1.booking_status)
        with self.assertRaises(SeatUnavailable):
            book_seat(self.user, self.movie, self.a1.id)
        self.assertEqual(Booking.objects.count(), 1)
#test for the seat becoming free upon deleting a booking 
    def test_deleting_booking_free(self):
        first = book_seat(self.user, self.movie, self.a1.id)
        book_seat(self.user, self.movie, self.a2.id)
        first.delete()
        self.a1.refresh_from_db()
        self.a2.refresh_from_db()
        self.assertFalse(self.a1.booking_status)
        self.assertTrue(self.a2.booking_status)


# Integration tests on the RESTful API by testing the status codes and make sure they match 
class APITests(APITestCase):
    #set up a test username for these parameters 
    def setUp(self):
        self.user, self.movie, (self.a1, self.a2) = make_data()
        self.bob = User.objects.create_user('bob', password='pw12345')
        
#CRUD requires a login to change
    def test_movies_login_to_change(self):
        payload = {'title': 'Arrival', 'description': 'Aliens.',
                   'release_date': '2016-11-11', 'duration': 116}
        self.assertEqual(self.client.get('/api/movies/').status_code, 200)
        self.assertEqual(self.client.post('/api/movies/', payload).status_code, 403)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/movies/', payload).status_code, 201)
        url = f'/api/movies/{self.movie.id}/'
        self.assertEqual(self.client.patch(url, {'title': 'New'}).status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)

#check if the seats can be filtered into available only
    def test_available_only(self):
        book_seat(self.user, self.movie, self.a1.id)
        self.assertEqual(len(self.client.get('/api/seats/').json()), 2)
        open_seats = self.client.get('/api/seats/?available=true').json()
        self.assertEqual([s['seat_number'] for s in open_seats], ['A2'])

#the whole booking workflow is tested here
    def test_booking_workflow(self):
        data = {'movie': self.movie.id, 'seat': self.a1.id}
        # anonymous users can't book and see no history
        self.assertEqual(self.client.post('/api/bookings/', data).status_code, 403)
        self.assertEqual(self.client.get('/api/bookings/').json(), [])
        # booking works, uses the logged-in user, and takes the seat
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['user'], 'alice')
        self.a1.refresh_from_db()
        self.assertTrue(self.a1.booking_status)
        # the same seat can't be booked twice, even by someone else
        self.assertEqual(self.client.post('/api/bookings/', data).status_code, 400)
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.post('/api/bookings/', data).status_code, 400)
        self.assertEqual(self.client.get('/api/bookings/').json(), [])
        # bookings can't be edited, and deleting frees the seat
        self.client.force_authenticate(self.user)
        url = f"/api/bookings/{response.json()['id']}/"
        self.assertEqual(self.client.patch(url, {'seat': self.a2.id}).status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.a1.refresh_from_db()
        self.assertFalse(self.a1.booking_status)


#Integration tests on the HTML pages themselves 
class PageTests(TestCase):
    def setUp(self):
        self.user, self.movie, (self.a1, self.a2) = make_data()
        self.book_url = reverse('book_seat', args=[self.movie.id])

    def test_movie_list_is_public(self):
        response = self.client.get(reverse('movie_list'))
        self.assertContains(response, 'Dune')
        self.assertContains(response, self.book_url)

    def test_booking_and_history__login(self):
        for url in (self.book_url, reverse('booking_history')):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/admin/login/', response.url)

    def test_booking_through_form(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.get(self.book_url), f'value="{self.a1.id}"')
        response = self.client.post(self.book_url, {'seat': self.a1.id}, follow=True)
        self.assertContains(response, 'Seat booked for Dune!')
        self.assertContains(self.client.get(reverse('booking_history')), 'A1')
        # the booked seat is no longer offered, and re-posting it shows an error
        self.assertNotContains(self.client.get(self.book_url), f'value="{self.a1.id}"')
        self.assertContains(self.client.post(self.book_url, {'seat': self.a1.id}), 'already taken')
        
#test if the form rejects a missing or unknown seat for the movie 
    def test_form_rejects_missing_or_unknown_seats(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.post(self.book_url, {}), 'valid seat')
        self.assertContains(self.client.post(self.book_url, {'seat': 9999}), 'valid seat')
        self.assertEqual(Booking.objects.count(), 0)
        self.assertEqual(self.client.get(reverse('book_seat', args=[999])).status_code, 404)
        
#check that the logout automatically returns to the movie list 
    def test_logout_returns(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('movie_list'))

class SeedTests(TestCase):
    def test_seed_demo_creates_data_and_is_repeatable(self):
        call_command('seed_demo')
        call_command('seed_demo')  # running twice must not duplicate anything
        self.assertEqual(Movie.objects.count(), len(MOVIES))
        self.assertEqual(Seat.objects.count(), len(ROWS) * SEATS_PER_ROW)
        self.assertTrue(User.objects.get(username='demo').is_staff)