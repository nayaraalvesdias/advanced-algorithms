import json
import random

student_quantity = 5000
professor_quantity = 300
room_quantity = 50
slots = room_quantity * 4 * 5
groups = []

students = []
professors = []
rooms = []

discipline_id = 0
timeslot_id = 0

def generate_professors():
    for i in range(professor_quantity):
        professor = {
            'id': "P" + str(i),
            'capacity': random.randint(1, 7),
            'used_capacity': 0
        }
        professors.append(professor)
    professor_json_str = json.dumps(professors, indent=4)
    with open("../data/professor.json", "w") as f:
        f.write(professor_json_str)


def get_professor():
    available_professors = [
        professor
        for professor in professors
        if professor['used_capacity'] < professor['capacity']
    ]

    if not available_professors:
        return None

    professor = random.choice(available_professors)

    professor['used_capacity'] += 1
    # add preference time for teacher
    professor_json_str = json.dumps(professors, indent=4)

    with open("../data/professor.json", "w") as f:
        f.write(professor_json_str)

    return professor

def generate_rooms():
    for x in range(room_quantity):
        random_capacity = random.randint(10, 25)

        room_id = "R" + str(x)
        room = {
            'id': room_id,
            'capacity': random_capacity,
            "time_slots": [
                {
                    "day": "Monday",
                    "times": get_time_slot("MON", random_capacity, room_id)
                },
                {
                    "day": "Tuesday",
                    "times": get_time_slot("TUE", random_capacity, room_id)
                },
                {
                    "day": "Wednesday",
                    "times": get_time_slot("WED", random_capacity, room_id)
                },
                {
                    "day": "Thursday",
                    "times": get_time_slot("THUR", random_capacity, room_id)
                },
                {
                    "day": "Friday",
                    "times": get_time_slot("FRI", random_capacity, room_id)
                }
            ]
        }
        rooms.append(room)

    room_json_str = json.dumps(rooms, indent=4)
    with open("../data/room.json", "w") as f:
        f.write(room_json_str)

def get_time_slot(weekday: str, room_capacity: int, room: str) -> list[dict[str, str | bool | int]]:
    return [
        {"id": weekday + "-" + str(1), "start": "07:00", "end": "10:00", "is_available": True,
         "capacity": room_capacity, "room": room},
        {"id": weekday + "-" + str(2), "start": "10:00", "end": "13:00", "is_available": True,
         "capacity": room_capacity, "room": room},
        {"id": weekday + "-" + str(3), "start": "13:00", "end": "16:00", "is_available": True,
         "capacity": room_capacity, "room": room},
        {"id": weekday + "-" + str(4), "start": "16:00", "end": "19:00", "is_available": True,
         "capacity": room_capacity, "room": room}
    ]

def create_discipline(capacity: int):
    global discipline_id
    discipline_quantity = random.randint(2, 3)
    disciplines = []

    for x in range(discipline_quantity):
        professor = get_professor()
        discipline = {
            'id': "D" + str(discipline_id),
            'professor': professor,
            'capacity': capacity,
            'slot': None
        }
        discipline_id += 1
        disciplines.append(discipline)
    return disciplines

def generate_group():
    i = 1
    all_group_capacity = 0
    while all_group_capacity <= student_quantity:
        student_random_capacity = random.randint(5, 20)
        all_group_capacity += student_random_capacity

        discipline = create_discipline(student_random_capacity)
        group = {
            'id': "G" + str(i),
            'capacity': student_random_capacity,
            'discipline_quantity': len(discipline),
            'disciplines': discipline
        }

        groups.append(group)

        # student file
        for s in range(student_random_capacity):
            students.append({
                'id': "S" + str(s),
                'group': group
            })

        i += 1

    group_json_str = json.dumps(groups, indent=4)
    student_json_str = json.dumps(students, indent=4)

    with open("../data/group.json", "w") as f:
        f.write(group_json_str)

    with open("../data/student.json", "w") as f:
        f.write(student_json_str)

equal = True
while equal:
    generate_professors()
    generate_rooms()
    generate_group()

    total_disciplines = sum(
        group["discipline_quantity"]
        for group in groups
    )

    print(total_disciplines)
    if total_disciplines == slots:
        equal = False
    else:
        discipline_id = 0
        rooms = []
        professors = []
        groups = []

print("completed")
