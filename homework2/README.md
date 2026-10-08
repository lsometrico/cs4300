# CS4300 - Homework 2 - Movie Theater Booking (Django)
 
A movie theater booking application built with Python, Django, and Django REST Framework. Users can browse movies, book seats, and review their booking history, both through a REST API and through a Bootstrap-styled web interface that reads and writes the same data.
 
**Live site (Render):** https://YOUR-SERVICE-NAME.onrender.com
 
**Demo login:** username `demo`, password `demo12345` (a staff account with no permissions: it can book seats but cannot edit data).
 
> The site runs on Render's free tier, which sleeps when idle. The first visit can take about a minute to wake up.
 
## Features
 
- Browse available movies (no account needed)
- Book an available seat for a movie (login required)
- View your own booking history, newest first
- REST API for movies, seats, and bookings with the same rules as the web pages
- Double-booking protection: a seat can only be booked once, even if two people try at the same moment
- Deleting a booking frees its seat again

## Project Structure
 
```
homework2/
└── movie_theater_booking/
    ├── manage.py
    ├── requirements.txt
    ├── .coveragerc                  # coverage settings
    ├── movie_theater_booking/       # project settings and root URLs
    ├── bookings/                    # the app
    │   ├── models.py                # Movie, Seat, Booking (+ signal that frees a seat on delete)
    │   ├── services.py              # book_seat(): the one place booking rules live
    │   ├── serializers.py           # JSON conversion for the API
    │   ├── views.py                 # ViewSets (API) and page views (HTML)
    │   ├── urls.py                  # page routes and the /api/ router
    │   ├── admin.py
    │   ├── tests.py                 # unit + integration tests
    │   ├── management/commands/
    │   │   └── seed_demo.py         # fills an empty database with demo data
    │   └── templates/bookings/
    │       ├── base.html            # Bootstrap layout and navbar
    │       ├── movie_list.html
    │       ├── seat_booking.html
    │       └── booking_history.html
    └── features/                    # Behave (BDD) tests
        ├── booking.feature
        └── steps/booking_steps.py
```
 
## Data Model
 
| Model | Fields |
|---|---|
| `Movie` | title, description, release date, duration (minutes, at least 1) |
| `Seat` | seat number (unique), booking status |
| `Booking` | movie, seat, user, booking date (set automatically) |
 
## Web Pages
 
| URL | Page | Login required |
|---|---|---|
| `/` | Movie list | No |
| `/movies/<id>/book/` | Pick an available seat and book it | Yes |
| `/history/` | Your bookings | Yes |
 
## API Endpoints
 
Anyone can read; creating or changing data requires being logged in.
 
| Endpoint | Methods | Notes |
|---|---|---|
| `/api/movies/` | GET, POST, PUT, PATCH, DELETE | Full CRUD on movies |
| `/api/seats/` | GET, POST, PUT, PATCH, DELETE | `?available=true` shows only open seats |
| `/api/bookings/` | GET, POST, DELETE | Shows only your own bookings; POST needs just `movie` and `seat` (the user comes from your login) |
 
Bookings cannot be edited with PUT or PATCH. Cancel and rebook instead, so seat statuses stay correct.
 
## Setup (run locally)
 
From the `movie_theater_booking` folder (the one containing `manage.py`):
 
```
python -m venv myenv
myenv\Scripts\activate            # Windows
# source myenv/bin/activate      # Mac / Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo        
```
 
Then open http://127.0.0.1:8000/.
 
In the DevEdu environment, create the venv with `python3 -m venv myenv --system-site-packages`, then run the server with `python3 manage.py runserver 0.0.0.0:3000` and open it with the "app" button.
  
**Logging in:** the site uses Django's built-in login page, which only accepts staff accounts. Use the `demo` account above, or create your own with `python manage.py createsuperuser`.
 
## Running the Tests
 
```
python manage.py test                 # unit and integration tests (13 tests)
coverage run manage.py test           # run them with coverage
coverage report -m                    # coverage summary
python manage.py behave               # BDD scenarios (2 scenarios)
```
 
- **Unit tests:** models, the `book_seat()` service, the delete signal, and the demo-data command
- **Integration tests:** API status codes and JSON output, login rules, duplicate-booking rejection, and the HTML pages
- **BDD (Behave):** booking an available seat, and being refused a seat that is already taken
- **Coverage:** 100% of the `bookings` app (migrations, `tests.py`, and `apps.py` are excluded; see `.coveragerc`)
## Deployment (Render)
 
The app is deployed as a Render **Web Service** .Render's free tier does not keep the SQLite file between deploys, so the build runs `seed_demo` to recreate the demo movies, seats, and login each time and can be run multiple times 
 
## Design Notes
 
- **One booking rule:** both the API and the web form call `book_seat()` in `services.py`. It locks the seat row inside a database transaction (`select_for_update`), so two simultaneous requests cannot both take the same seat.
- **Users can't pick the user:** the booking serializer treats `user` as read-only and the view fills it from the logged-in account.
- **Seat cleanup:** a `post_delete` signal marks a seat available again whenever its booking is removed, whether through the API, the admin, or a cascade.
## Known Limitations
 
- Any logged-in user can create or edit movies and seats through the API (there is no separate admin-only permission).
- There is no sign-up page; accounts are created by an administrator. The login page is Django's admin login, so it only accepts staff accounts.
- Seats are shared across movies: booking a seat marks it taken for every showing, because the assignment's model has a single status per seat.
- SQLite data on Render's free tier is temporary and resets on every deploy.
 
