import sqlite3
import faker as fake
import random


def seed_rooms(conn, n=100) -> list[int]:
    rooms = []
    for i in range(1, n + 1):
        rooms.append((
            i,                                    # room_id
            fake.random_int(20, 200),             # capacity
            random.choice([0, 1]),                # has_projector
            fake.random_element(['S1', 'S2', 'S3', 'HMZ', 'Piloty'])  # building
        ))
    
    conn.executemany(
        "INSERT INTO room VALUES (?, ?, ?, ?)",
        rooms
    )
    
    return [r[0] for r in rooms]  # return just the IDs → [1, 2, 3, ..., 20]


# TODO fix departments seeding (more than 3 departments)
def seed_departments(conn, room_ids, n=20) -> list[int]:
    departments = []
    for i in range(1, n + 1):
        departments.append((
            i,                                              # department_id
            fake.random_element(['Informatik', 'Mathematik', 'Physik']),  # name
            fake.random_element(['FB 18', 'FB 04', 'FB 05']),             # faculty
            random.choice(room_ids)                         # office_location — must be a real room_id
        ))
    
    conn.executemany(
        "INSERT INTO department VALUES (?, ?, ?, ?)",
        departments
    )
    
    return [d[0] for d in departments]


# TODO make sure the number is appropriate
def seed_office_hourse(conn, n=200) -> list[int]:
    ...


def seed_students(conn, department_ids, n=400) -> list[int]:
    ...


def seed_professors(conn, department_ids, n=90) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_enrollments(conn, student_ids, n=1000) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_courses(conn, department_ids, enrollment_ids, n=200) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_submissions(conn, enrollment_ids, n=200) -> list[int]:
    ...


# TODO make sure the number is appropriate
# Some 60 Profs have 2 times a week, 30 will have 1 times a week
def seed_professor_office_hours(conn, professor_ids, office_hours_ids, room_ids, n=150) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_class_sessions(conn, professor_ids, course_ids, room_ids, n=200) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_professor_teaches_courses(conn, professor_ids, course_ids, n=200) -> list[int]:
    ...


# TODO make sure the number is appropriate
def seed_course_prerequisites(conn, course_ids, prerequisite_ids, n=200) -> list[int]:
    ...


# then at the bottom:
if __name__ == "__main__":
    conn = sqlite3.connect("competition.db")
    conn.execute("PRAGMA foreign_keys = ON")
    
    room_ids = seed_rooms(conn)
    department_ids = seed_departments(conn, room_ids)
    student_ids = seed_students(conn, department_ids)
    ...
    
    conn.commit()
    conn.close()