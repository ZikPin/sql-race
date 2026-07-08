Project Overview
Flask web app with two views — participant and admin. Participants submit SQL queries, the backend runs them read-only against a pre-loaded SQLite DB and compares result sets against expected answers. Scores update live on the admin scoreboard.

```
Folder Structure
sql-race/
├── app.py                  # Flask app, all routes and logic
├── seed.py                 # run once: creates and populates competition.db
├── init_db.py              # run once: creates app.db (teams, submissions)
├── questions.json          # competition questions, points, expected outputs
├── competition.db          # read-only: schema + seed data
├── app.db                  # writable: teams, scores, submissions
├── templates/
│   ├── base.html           # shared layout, Bootstrap CDN link
│   ├── index.html          # participant view
│   └── admin.html          # scoreboard
├── static/
│   └── style.css           # minimal custom styles
├── requirements.txt
└── .gitignore
```

Libraries
bashpip install flask
That's the only install. Everything else is stdlib:

sqlite3 — built into Python, runs queries against both DBs
json — reads questions.json
hashlib or just a hardcoded string — admin password check

Bootstrap via CDN in base.html — no install.