import sqlite3
from faker import Faker
import random


# Faker
fake = Faker('de_DE')


# SEEDING ROOMS
def seed_rooms(conn, n=50) -> list[int]:
    buildings = [f"{random.choice(['S', 'L'])}{random.randint(1,3)}{random.randint(0,9)}{random.randint(0,9)}" 
                 for i in range(20)]
    
    rooms = []
    for i in range(1, n + 1):
        rooms.append((
            i,                          # room_id
            random.choice([0, 1]),      # has_projector
            random.randint(20, 200),    # capacity
            random.choice(buildings),   # building e.g. S101, L203
            random.randint(1, 50)       # room_number
        ))
    
    conn.executemany(
        "INSERT INTO room (room_id, has_projector, capacity, building, room_number) VALUES (?, ?, ?, ?, ?)",
        rooms
    )
    
    return [r[0] for r in rooms]


# SEEDING OFFICE_HOURS
def seed_office_hours(conn) -> list[int]:
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    slots = [
        ('08:00', '09:30'),
        ('09:30', '11:00'),
        ('11:00', '12:30'),
        ('12:30', '14:00'),
        ('14:00', '15:30'),
        ('15:30', '17:00'),
    ]

    office_hours = []
    i = 1
    for day in days:
        for start, end in slots:
            office_hours.append((i, day, start, end))
            i += 1

    conn.executemany(
        "INSERT INTO office_hours (office_hour_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
        office_hours
    )

    return [oh[0] for oh in office_hours]


# SEEDING DEPARTMENTS
def seed_departments(conn, room_ids: list[int]) -> list[int]:
    departments_raw = [
        (1,  "Rechts- und Wirtschaftswissenschaften"),
        (2,  "Gesellschafts- und Geschichtswissenschaften"),
        (3,  "Humanwissenschaften"),
        (4,  "Mathematik"),
        (5,  "Physik"),
        (7,  "Chemie"),
        (10, "Biologie"),
        (11, "Material- und Geowissenschaften"),
        (13, "Bau- und Umweltingenieurwissenschaften"),
        (15, "Architektur"),
        (16, "Maschinenbau"),
        (18, "Elektrotechnik und Informationstechnik"),
        (20, "Informatik"),
    ]

    assigned_rooms = random.sample(room_ids, len(departments_raw))

    departments = [
        (dept_id, name, room)
        for (dept_id, name), room in zip(departments_raw, assigned_rooms)
    ]

    conn.executemany(
        "INSERT INTO department (department_id, name, office_location) VALUES (?, ?, ?)",
        departments
    )

    return [d[0] for d in departments]


# SEEDING STUDENTS
def seed_students(conn, department_ids: list[int], n=500) -> list[int]:
    students = []
    for i in range(1, n + 1):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=35)
        enrollment_date = fake.date_between(start_date='-6y', end_date='today')
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@stud.tu-darmstadt.de"

        students.append((
            i,
            first_name,
            last_name,
            email,
            enrollment_date.strftime('%Y-%m-%d'),
            birth_date.strftime('%Y-%m-%d'),
            random.choice(department_ids)
        ))

    conn.executemany(
        "INSERT INTO student (student_id, first_name, last_name, email, enrollment_date, birth_date, department_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        students
    )

    return [s[0] for s in students]


# SEEDING PROFESSORS
def seed_professors(conn, department_ids: list[int], n=50) -> list[int]:
    professors = []
    for i in range(1, n + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@tu-darmstadt.de"
        hire_date = fake.date_between(start_date='-30y', end_date='-1y')

        professors.append((
            i,
            hire_date.strftime('%Y-%m-%d'),
            email,
            first_name,
            last_name,
            random.choice(department_ids)
        ))

    conn.executemany(
        "INSERT INTO professor (professor_id, hire_date, email, first_name, last_name, department_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        professors
    )

    return [p[0] for p in professors]


# SEEDING COURSES
def seed_courses(conn, department_ids: list[int], n_per_department=20) -> list[int]:
    prefixes = [
        "Introduction to", "Advanced", "Fundamentals of", "Applied",
        "Theoretical", "Practical", "Seminar:", "Topics in"
    ]
    topics = [
        "Algorithms", "Database Systems", "Machine Learning", "Linear Algebra",
        "Statistics", "Software Engineering", "Computer Networks", "Calculus",
        "Data Structures", "Operating Systems", "Artificial Intelligence",
        "Discrete Mathematics", "Programming Paradigms", "Cryptography",
        "Signal Processing", "Quantum Computing", "Numerical Methods",
        "Computer Architecture", "Distributed Systems", "Graph Theory"
    ]
    levels = ['Bachelor', 'Bachelor', 'Bachelor', 'Master', 'Master', 'Doctorate']

    courses = []
    i = 1
    for dept_id in department_ids:
        for _ in range(n_per_department):
            title = f"{random.choice(prefixes)} {random.choice(topics)}"
            courses.append((
                i,
                title,
                random.choice(levels),
                random.randint(4, 15),
                dept_id
            ))
            i += 1

    conn.executemany(
        "INSERT INTO course (course_id, title, level, credits, department_id) VALUES (?, ?, ?, ?, ?)",
        courses
    )

    return [c[0] for c in courses]


# SEEDING ENROLLMENTS
def seed_enrollments(conn, student_ids: list[int], course_ids: list[int]) -> list[int]:
    semesters = [
        'WS2020/21', 'SS2021', 'WS2021/22', 'SS2022',
        'WS2022/23', 'SS2023', 'WS2023/24', 'SS2024'
    ]
    grades = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]

    enrollments = []
    seen = set()
    i = 1

    for student_id in student_ids:
        n_enrollments = random.randint(5, 10)
        attempts = 0
        added = 0

        while added < n_enrollments and attempts < 50:
            course_id = random.choice(course_ids)
            semester = random.choice(semesters)
            key = (student_id, course_id, semester)

            if key not in seen:
                seen.add(key)
                grade = random.choice(grades) if random.random() > 0.1 else None
                enrollments.append((i, semester, grade, student_id, course_id))
                i += 1
                added += 1

            attempts += 1

    conn.executemany(
        "INSERT INTO enrollment (enrollment_id, semester, grade, student_id, course_id) VALUES (?, ?, ?, ?, ?)",
        enrollments
    )

    return [e[0] for e in enrollments]


# SEEDING SUBMISSIONS
def seed_submissions(conn, enrollment_ids: list[int]) -> None:
    submission_types = [
        'draft_paper', 'exposé', 'calculation_task',
        'programming_task', 'literature_review', 'presentation'
    ]
    grades = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]

    submissions = []

    for enrollment_id in enrollment_ids:
        if random.random() > 0.4:  # 60% chance of having submissions
            n_submissions = random.randint(1, 3)
            for submission_id in range(1, n_submissions + 1):
                grade = random.choice(grades) if random.random() > 0.1 else None
                feedback = fake.sentence(nb_words=10) if random.random() > 0.4 else None
                submitted_at = fake.date_between(start_date='-4y', end_date='today').strftime('%Y-%m-%d')

                submissions.append((
                    enrollment_id,
                    submission_id,
                    grade,
                    submitted_at,
                    random.choice(submission_types),
                    feedback
                ))

    conn.executemany(
        "INSERT INTO submission (enrollment_id, submission_id, grade, submitted_at, submission_type, feedback) VALUES (?, ?, ?, ?, ?, ?)",
        submissions
    )


# SEEDING PROFESSOR OFFICE HOURS
def seed_professor_has_office_hours(conn, professor_ids: list[int], office_hour_ids: list[int], room_ids: list[int]) -> None:
    assignments = []
    seen = set()

    for professor_id in professor_ids:
        n_office_hours = random.randint(1, 3)
        available = [oh for oh in office_hour_ids if (professor_id, oh) not in seen]
        chosen = random.sample(available, min(n_office_hours, len(available)))

        for office_hour_id in chosen:
            seen.add((professor_id, office_hour_id))
            assignments.append((
                professor_id,
                office_hour_id,
                random.choice(room_ids)
            ))

    conn.executemany(
        "INSERT INTO professor_has_office_hours (professor_id, office_hour_id, room_id) VALUES (?, ?, ?)",
        assignments
    )


# SEEDING PROFESSOR TEACHES COURSES
def seed_professor_teaches_course(conn, professor_ids: list[int], course_ids: list[int]) -> None:
    assignments = []
    seen = set()

    for course_id in course_ids:
        available = list(professor_ids)

        # assign exactly one lecturer
        lecturer = random.choice(available)
        seen.add((lecturer, course_id))
        assignments.append((lecturer, course_id))
        available.remove(lecturer)

        # assign 1-3 assistants
        n_assistants = random.randint(1, 3)
        assistants = random.sample(available, min(n_assistants, len(available)))
        for professor_id in assistants:
            if (professor_id, course_id) not in seen:
                seen.add((professor_id, course_id))
                assignments.append((professor_id, course_id))

    conn.executemany(
        "INSERT INTO professor_teaches_course (professor_id, course_id) VALUES (?, ?)",
        assignments
    )


# SEEDING CLASS SESSIONS
def seed_class_sessions(conn, office_hour_ids: list[int], room_ids: list[int]) -> None:
    session_types = ['Lecture', 'Übungsgruppe']
    assignments = []
    seen = set()

    # fetch existing professor-course pairs from DB
    pairs = conn.execute(
        "SELECT professor_id, course_id FROM professor_teaches_course"
    ).fetchall()

    for professor_id, course_id in pairs:
        # always one lecture
        office_hour_id = random.choice(office_hour_ids)
        key = (professor_id, course_id, office_hour_id, 'Lecture')
        if key not in seen:
            seen.add(key)
            assignments.append((professor_id, course_id, office_hour_id, random.choice(room_ids), 'Lecture'))

        # 50% chance of second lecture at different time
        if random.random() > 0.5:
            office_hour_id = random.choice(office_hour_ids)
            key = (professor_id, course_id, office_hour_id, 'Lecture')
            if key not in seen:
                seen.add(key)
                assignments.append((professor_id, course_id, office_hour_id, random.choice(room_ids), 'Lecture'))

        # 1-2 practice sessions
        n_practice = random.randint(1, 2)
        for _ in range(n_practice):
            office_hour_id = random.choice(office_hour_ids)
            key = (professor_id, course_id, office_hour_id, 'Übungsgruppe')
            if key not in seen:
                seen.add(key)
                assignments.append((professor_id, course_id, office_hour_id, random.choice(room_ids), 'Übungsgruppe'))

    conn.executemany(
        "INSERT INTO class_session (professor_id, course_id, office_hour_id, room_id, type) VALUES (?, ?, ?, ?, ?)",
        assignments
    )


# SEEDING PREREQUISITES
def seed_course_has_prerequisites(conn, course_ids: list[int]) -> None:
    prerequisites = []
    seen = set()

    for course_id in course_ids:
        # 60% chance a course has any prerequisites
        if random.random() > 0.4:
            n_prerequisites = random.randint(1, 3)
            available = [c for c in course_ids if c != course_id]
            chosen = random.sample(available, min(n_prerequisites, len(available)))

            for prerequisite_id in chosen:
                key = (course_id, prerequisite_id)
                if key not in seen:
                    seen.add(key)
                    prerequisites.append((course_id, prerequisite_id))

    conn.executemany(
        "INSERT INTO course_has_prerequisites (course_id, prerequisite_id) VALUES (?, ?)",
        prerequisites
    )


# then at the bottom:
if __name__ == "__main__":
    import os

    db_path = os.path.join(os.path.dirname(__file__), 'competition.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'contest_schema.sql')

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    # apply schema
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())

    print("Schema applied.")

    room_ids = seed_rooms(conn, n=30)
    print(f"Seeded {len(room_ids)} rooms.")

    office_hour_ids = seed_office_hours(conn)
    print(f"Seeded {len(office_hour_ids)} office hours.")

    department_ids = seed_departments(conn, room_ids)
    print(f"Seeded {len(department_ids)} departments.")

    student_ids = seed_students(conn, department_ids, n=500)
    print(f"Seeded {len(student_ids)} students.")

    professor_ids = seed_professors(conn, department_ids, n=50)
    print(f"Seeded {len(professor_ids)} professors.")

    course_ids = seed_courses(conn, department_ids, n_per_department=20)
    print(f"Seeded {len(course_ids)} courses.")

    enrollment_ids = seed_enrollments(conn, student_ids, course_ids)
    print(f"Seeded {len(enrollment_ids)} enrollments.")

    seed_submissions(conn, enrollment_ids)
    print("Seeded submissions.")

    seed_professor_has_office_hours(conn, professor_ids, office_hour_ids, room_ids)
    print("Seeded professor office hours.")

    seed_professor_teaches_course(conn, professor_ids, course_ids)
    print("Seeded professor teaches course.")

    seed_class_sessions(conn, office_hour_ids, room_ids)
    print("Seeded class sessions.")

    seed_course_has_prerequisites(conn, course_ids)
    print("Seeded course prerequisites.")

    conn.commit()
    conn.close()
    print("Done. competition.db is ready.")