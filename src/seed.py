import sqlite3
import faker as fake
import random


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

# then at the bottom:
if __name__ == "__main__":
    conn = sqlite3.connect("competition.db")
    conn.execute("PRAGMA foreign_keys = ON")
    
    room_ids = seed_rooms(conn)
    
    conn.commit()
    conn.close()