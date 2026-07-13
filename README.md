# SQL Race

A lightweight web platform for running team-based SQL query competitions. Teams translate English problem descriptions into SQL, submit their queries, and get instant feedback. An admin scoreboard updates live throughout the event.

## Stack

- **Backend:** Python, Flask
- **Database:** SQLite (two separate databases)
- **Templating:** Jinja2
- **Styling:** Custom CSS (dark theme, no framework)
- **Deployment:** Render


## Project Structure

```
sql-race/
├── instance/               # Generated at runtime, gitignored
│   ├── app.db              # App state: teams and submissions
│   └── contest.db          # Competition data: schema + seed data
├── src/
│   ├── __init__.py         # App factory (create_app)
│   ├── db.py               # DB connections, CLI init commands
│   ├── auth.py             # Blueprint: registration and session
│   ├── contest.py          # Blueprint: questions, submission checker
│   ├── admin.py            # Blueprint: scoreboard
│   ├── seed.py             # One-time seeding script for contest.db
│   ├── app_schema.sql      # Schema for app.db
│   ├── contest_schema.sql  # Schema for contest.db
│   ├── questions.json      # Competition questions, scores, answer queries
│   ├── templates/
│   │   ├── base.html
│   │   ├── register.html
│   │   ├── questions.html
│   │   └── admin.html
│   │   └── scores.html
│   └── static/
│       └── style.css
├── .env                    # Local environment variables (gitignored)
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```


## Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key
ADMIN_PASSWORD=your_admin_password
```

- `SECRET_KEY` — used by Flask to sign session cookies. Use any long random string in production.
- `ADMIN_PASSWORD` — password to access the live scoreboard at `/admin/login`.

On Render, set these in the **Environment** tab of your service dashboard instead of a `.env` file.


## Local Setup

```bash
# Clone the repo
git clone https://github.com/your-username/sql-race.git
cd sql-race

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize both databases (creates tables and seeds contest.db)
flask --app src init-db

# Run the development server
flask --app src run --debug
```

The app will be available at `http://127.0.0.1:5000`.


## Questions

Competition questions are defined in `src/questions.json`. Each entry has the following structure:

```json
{
    "id": 1,
    "difficulty": "easy",
    "score": 1,
    "question": "Find the first name and last name of all students.",
    "answer_query": "SELECT first_name, last_name FROM student"
}
```

- `answer_query` is run against `contest.db` at submission time and the result is compared against the participant's query output.
- Results are compared as sorted sets, so column order matters but row order does not.


## Admin Scoreboard

Navigate to `/admin/login` and enter the `ADMIN_PASSWORD`. The scoreboard shows all teams, their total score, and which questions they have solved. It auto-refreshes every 5 seconds.

This URL is not linked anywhere in the participant UI — share it only with event organizers.


## Deployment (Render)

1. Push the repo to GitHub
2. Create a new **Web Service** on [Render](https://render.com) and connect the repo
3. Set the following in the Render dashboard under **Environment**:
   - `SECRET_KEY`
   - `ADMIN_PASSWORD`
4. Set the build and start commands:
   - **Build command:** `pip install -r requirements.txt && flask --app src init-db`
   - **Start command:** `gunicorn "src:create_app()"`

> **Note:** `gunicorn` is not compatible with Windows. For local development, use `flask --app src run --debug` instead.

> **Warning:** Every new deploy re-runs `init-db`, which resets `app.db`. Avoid deploying during an active competition.