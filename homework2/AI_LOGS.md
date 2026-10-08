# AI Usage Log

Course policy: any use of AI (for ideas, text, code or anything else) must be cited in your README, saying which tool, what it was used for, and how you used the output. Keep this log as you go, then copy the summary into your README.

> 📖 Book: "Record where you used AI and how you verified it", §13.2.10.

## Summary (paste into README)

- **Tool:** Claude (Anthropic), used through the claude.ai chat interface. Model: Claude Sonnet 5.5
- **Used for:** Explaining the Django structure and assignment requirements; drafting settings, serializers, ViewSets, URL routing, the `book_seat()` service, the Bootstrap templates and page views, the unit/integration/Behave tests, the `seed_demo` command, and the Render deployment settings; reviewing my pushed GitHub commits for bugs; diagnosing error messages; drafting the README and this log.
- **How I used the output:** Claude was used to understand the inner workings of Django in more vague concepts (such as the implemenation of settings in order to prep a website deployment). Code was reviewed before, and tested multiple times before committing on git. I ran the app and the full test suite myself before each commit, and tested the API by hand in the browsable API.

## Log

| Date | Feature / task | What I asked Claude | What I kept, changed or rejected |
|---|---|---|---|
| Oct 6 | Project settings | How to configure `settings.py` for the app, DRF, DevEdu, and Render | Changed: I chose `python-decouple`'s `config()` instead of `os.environ` as I was more familiar during the main project setup. Verified with `manage.py check` |
| Oct 6 | Git cleanup | How to untrack `__pycache__` and `db.sqlite3` that were accidentally committed | Kept: `git rm --cached`.Verified with `git status` and on GitHub |
| Oct 6 | Migrations | Why `makemigrations` said "No changes detected" | Kept: committing the existing `0001_initial.py`. Verified the file on GitHub |
| Oct 7 | Serializers, ViewSets, API routes | How to build the API for movies, seats, and bookings | Kept: the overall structure. Changed: I typed it into my own files. Claude's review of my commits found four mistakes in my copy (a misspelled `booking_status`, a misplaced `return qs`, `Booking.objects.none` missing `()`, and a missing read-only `user` field). I fixed each and re-tested by hand |
| Oct 7 | Booking rules, seat release, method restrictions | Fixes for feedback from the class server (read-only user, freeing a seat on delete, shared booking logic) | Kept: `services.py` with `book_seat()`, the `post_delete` signal, and a method restriction. Changed: I reworded error messages and fixed my `https_method_names` typo to `http_method_names` after Claude's check caught it |
| Oct 7 | Tests | How to write unit, integration, and Behave tests with 80% coverage| Rejected: the longer 69-test version that was about 500 lines of code.  Changed: Test suite was compacted to 12 tests, and set up Behave myself after fixing a misnamed `booking.features` file. Verified: `manage.py test`, `coverage report`, `manage.py behave` |
| Oct 7 | Render preparation | How to prepare `requirements.txt`, static files, and the Render build and start commands | Kept: WhiteNoise middleware, `STATIC_ROOT`, build and start commands. Changed: regenerated `requirements.txt` as ASCII. Claude rehearsed the build in a clean environment; I will verify on the live site |
| Oct 7-8 | Demo-data command | How to keep Render's database from being empty | Kept: the `seed_demo` command and its test. Changed: I chose my own movies and fixed a leading-zero date, a wrong import, and my movie list. The test now reads its expected counts from the command |
| Oct 8 | README and this log | Draft a README and fill in this log | Changed: I replaced the Render URL placeholder and edited the text to match my work |