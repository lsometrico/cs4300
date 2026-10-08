#temporary dbsqlite database to work with 
#render is just gonna nuke it anyway since db.sqlite3 is untracked in the repository 
#so we use this to test that the live site always has something to work with 
from datetime import date
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand 
from bookings.models import Movie, Seat

MOVIES = [
    ('Resident Evil', 'A city where the residents are evil or something idk i havent played the games', date(2026, 9, 18), 155),
    ('Synecdoche: New York', 'Some dude decides to make a massive play and then it ends up becoming his reality', date(2008, 10, 24), 175),
    ('Slumdog Millionare', 'A boy recounts his life story as he gets close to winning the million dollar prize on a game show', date(2008, 8, 30), 120),
    ('Justice: Live at Accor Arena','Relive the largest show in the duos history at a sold-out Accor Arena in Paris', date(2024, 6, 12), 114)
]
ROWS = 'ABCDEFG'
SEATS_PER_ROW = 10

class Command(BaseCommand):
    help = 'Create demo movies, seats and a demo user if they do not exist yet.'

    def handle(self, *args, **options):
        for title, description, release_date, duration in MOVIES:
            Movie.objects.get_or_create(title=title, defaults={
                'description': description,
                'release_date': release_date,
                'duration': duration,
            })
        for row in ROWS:
            for number in range(1, SEATS_PER_ROW + 1):
                Seat.objects.get_or_create(seat_number=f'{row}{number}')

        # The site's login page is Django's admin login, which only lets staff in.
        # This account has no permissions, so it can book seats but not edit data.
        user, created = get_user_model().objects.get_or_create(
            username='demo', defaults={'is_staff': True})
        if created:
            user.set_password('demo12345')
            user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Demo data ready: {Movie.objects.count()} movies, {Seat.objects.count()} seats.'))