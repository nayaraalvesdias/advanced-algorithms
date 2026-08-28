import json
import random

# Group A (Year 1 Computer Science)
#     │
#     ├── Intro to Math
#     ├── Intro to Programming
#     └── Computer Systems

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
    #add preference time for teacher
    professor_json_str = json.dumps(professors, indent=4)

    with open("../data/professor.json", "w") as f:
        f.write(professor_json_str)

    return professor


def generate_rooms():
    for x in range(room_quantity):
        random_capacity = random.randint(5, 25)


        room = {
            'id': "R" + str(x),
            'capacity': random_capacity,
            "time_slots": [
                {
                    "day": "Monday",
                    "times": get_time_slot("MON")
                },
                {
                    "day": "Tuesday",
                    "times": get_time_slot("TUE")
                },
                {
                    "day": "Wednesday",
                    "times": get_time_slot("WED")
                },
                {
                    "day": "Thursday",
                    "times": get_time_slot("THUR")
                },
                {
                    "day": "Friday",
                    "times": get_time_slot("FRI")
                }
            ]
        }
        rooms.append(room)

    room_json_str = json.dumps(rooms, indent=4)
    with open("../data/room.json", "w") as f:
        f.write(room_json_str)


def get_time_slot(weekday: str) -> list[dict[str, str | bool]]:
    available_time = [
        {"id": weekday + "-" + str(1), "start": "07:00", "end": "10:00", "is_available": True},
        {"id": weekday + "-" + str(2), "start": "10:00", "end": "13:00", "is_available": True},
        {"id": weekday + "-" + str(3), "start": "13:00", "end": "16:00", "is_available": True},
        {"id": weekday + "-" + str(4), "start": "16:00", "end": "19:00", "is_available": True}
    ]
    return available_time


def create_discipline():
    global discipline_id
    d_capacity = random.randint(2, 3)
    disciplines = []

    for x in range(d_capacity):
        professor = get_professor()
        discipline = {
            'id': "D" + str(discipline_id),
            'professor': professor
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

        discipline = create_discipline()
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


# generating dataset with 350 disciplines as slots quantity
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
