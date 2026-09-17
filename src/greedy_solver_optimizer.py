import json

with open("../data/group.json", "r") as file:
    groups = json.load(file)

with open("../data/room.json", "r") as file:
    rooms = json.load(file)

with open("../data/professor.json", "r") as file:
    professors = json.load(file)

# mapping disciplines
disciplines = [
    discipline
    for group in groups
    for discipline in group["disciplines"]
]

disciplines.sort(key=lambda discipline: discipline["capacity"], reverse=True)

# mapping slots
slots = [
    slot
    for room in rooms
    for time_slot in room["time_slots"]
    for slot in time_slot["times"]
]

slots.sort(key=lambda time_slot: time_slot["capacity"], reverse=True)

print("disciplines " + str(len(disciplines)))
print("rooms " + str(len(slots)))

professor_availabilities = []
professor_conflicts = []
disciplines_not_allocated = []
slots_not_allocated = []
scheduling = []

filtered_disciplines = []

counter = 0
def interval_partitioning():

    for slot in slots:
        for discipline in disciplines:
            if discipline["capacity"] <= slot["capacity"] and discipline["slot"] is None:
                professor_id = discipline["professor"]["id"]
                professor_availability = next(
                    filter(
                        lambda availability: availability["id"] == professor_id,
                        professor_availabilities
                    ),
                    None
                )

                if professor_availability is not None and slot["id"] in professor_availability["not_available_slots"]:
                    professor_conflicts.append(discipline)
                else:
                    scheduling.append({
                        'discipline': discipline,
                        'slot': slot
                    })
                    slot["is_available"] = False
                    discipline["slot"] = slot

                    if professor_availability is not None:
                        professor_availability['not_available_slots'].append(slot["id"])
                    else:
                        professor_availabilities.append({
                            'id': discipline["professor"]['id'],
                            'not_available_slots': [slot["id"]]
                        })

                break

        if slot["is_available"]:
            slots_not_allocated.append(slot)

    filtered_disciplines = list(
        filter(lambda disc: disc["slot"] is None, disciplines)
    )

    print("discipline_not_allocated " + str(len(filtered_disciplines)))
    disc_not_allocated_json_str = json.dumps(filtered_disciplines, indent=4)
    with open("../data/discpline_not_allocated_json_str.json", "w") as f:
        f.write(disc_not_allocated_json_str)

    global counter
    slots_available = [
        item for item in slots
        if item["is_available"]
    ]

    print("slots_available:", len(slots_available))
    print("counter:", counter)
    print("condition 1:", len(slots_available) > 1)
    print("condition 2:", counter < 10)

    if len(slots_available) > 1 and counter < 10:
        print("interval_partitioning " + str(counter))
        counter += 1
        interval_partitioning()

    return None


interval_partitioning()

print("slots_not_allocated " + str(len(slots_not_allocated)))
slots_not_allocated_json_str = json.dumps(slots_not_allocated, indent=4)
with open("../data/slots_not_allocated_json_str.json", "w") as f:
    f.write(slots_not_allocated_json_str)

print("conflicts_quantity " + str(len(professor_conflicts)))
professor_conflicts_json_str = json.dumps(professor_conflicts, indent=4)
with open("../data/professor_conflicts.json", "w") as f:
    f.write(professor_conflicts_json_str)

print("professor_availabilities " + str(len(professor_availabilities)))
professor_availabilities_json_str = json.dumps(professor_availabilities, indent=4)
with open("../data/professor_availabilities_json_str.json", "w") as f:
    f.write(professor_availabilities_json_str)

scheduling_json_str = json.dumps(scheduling, indent=4)
with open("../data/match_discipline_slot.json", "w") as f:
    f.write(scheduling_json_str)