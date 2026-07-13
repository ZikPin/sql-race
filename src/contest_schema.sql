-- Dropping Entity Tables
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS submission;
DROP TABLE IF EXISTS office_hours;
DROP TABLE IF EXISTS room;

-- Dropping Relations Tables
DROP TABLE IF EXISTS professor_has_office_hours;
DROP TABLE IF EXISTS class_session;
DROP TABLE IF EXISTS professor_teaches_course;
DROP TABLE IF EXISTS course_has_prerequisites;

-- Creating the tables
CREATE TABLE room (
    room_id       INTEGER PRIMARY KEY,
    has_projector INTEGER NOT NULL,
    capacity      INTEGER NOT NULL,
    building      TEXT NOT NULL,
    room_number   INTEGER NOT NULL
);

CREATE TABLE office_hours (
    office_hour_id INTEGER PRIMARY KEY,
    day_of_week    TEXT NOT NULL,
    start_time     TEXT NOT NULL,
    end_time       TEXT NOT NULL,
);

CREATE TABLE department (
    department_id   INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    office_location INTEGER NOT NULL,
    FOREIGN KEY (office_location) REFERENCES room(room_id)
);

CREATE TABLE student (
    student_id      INTEGER PRIMARY KEY,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT NOT NULL,
    enrollment_date TEXT NOT NULL,
    birth_date      TEXT NOT NULL,
    department_id   INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE professor (
    professor_id  INTEGER PRIMARY KEY,
    hire_date     TEXT NOT NULL,
    email         TEXT NOT NULL,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE course (
    course_id     INTEGER PRIMARY KEY,
    title         TEXT NOT NULL,
    level         TEXT NOT NULL,
    credits       INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE enrollment (
    enrollment_id INTEGER NOT NULL PRIMARY KEY,
    semester      TEXT NOT NULL,
    grade         REAL,
    student_id    INTEGER NOT NULL,
    course_id     INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE submission (
    enrollment_id   INTEGER NOT NULL,
    submission_id   INTEGER NOT NULL,
    grade           REAL,
    submitted_at    TEXT NOT NULL,
    submission_type TEXT NOT NULL,
    feedback        TEXT,
    PRIMARY KEY (enrollment_id, submission_id),
    FOREIGN KEY (enrollment_id) REFERENCES enrollment(enrollment_id)
);

CREATE TABLE professor_has_office_hours (
    professor_id   INTEGER NOT NULL,
    office_hour_id INTEGER NOT NULL,
    room_id        INTEGER NOT NULL,
    PRIMARY KEY (professor_id, office_hour_id),
    FOREIGN KEY (professor_id) REFERENCES professor(professor_id),
    FOREIGN KEY (office_hour_id) REFERENCES office_hours(office_hour_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE class_session (
    professor_id     INTEGER NOT NULL,
    course_id        INTEGER NOT NULL,
    office_hour_id   INTEGER NOT NULL,
    room_id          INTEGER NOT NULL,
    type             TEXT NOT NULL,
    PRIMARY KEY (professor_id, course_id, office_hour_id, type)
    FOREIGN KEY (professor_id) REFERENCES professor(professor_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE professor_teaches_course (
    professor_id INTEGER NOT NULL,
    course_id    INTEGER NOT NULL,
    PRIMARY KEY (professor_id, course_id),
    FOREIGN KEY (professor_id) REFERENCES professor(professor_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE course_has_prerequisites (
    course_id       INTEGER NOT NULL,
    prerequisite_id INTEGER NOT NULL,
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (prerequisite_id) REFERENCES course(course_id)
);