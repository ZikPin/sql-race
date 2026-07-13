DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS submission;

CREATE TABLE IF NOT EXISTS team (
    team_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    joined_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS submission (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id       INTEGER NOT NULL,
    question_id   INTEGER NOT NULL,
    submitted_sql TEXT NOT NULL,
    submitted_at  TEXT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);