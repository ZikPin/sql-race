DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS submission;

CREATE TABLE IF NOT EXISTS Team (
    team_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE
);
        
CREATE TABLE IF NOT EXISTS Submission (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id       INTEGER NOT NULL,
    question_id   INTEGER NOT NULL,
    submitted_sql TEXT NOT NULL,
    is_correct    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);