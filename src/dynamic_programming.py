import json

with open("../data/group.json", "r") as file:
    groups = json.load(file)

with open("../data/room.json", "r") as file:
    rooms = json.load(file)

disciplines = [
    {
        **discipline,
        "capacity": discipline["capacity"]
    }
    for group in groups
    for discipline in group["disciplines"]
]

slots = [
    {
        **slot,
        "room": room["id"],
        "capacity": room["capacity"]
    }
    for room in rooms
    for time_slot in room["time_slots"]
    for slot in time_slot["times"]
]


def quick_sort(array, low, high):

    if low >= high:
        return

    pivot = array[high]["capacity"]

    i = low

    for j in range(low, high):

        if array[j]["capacity"] < pivot:

            array[i], array[j] = array[j], array[i]

            i += 1

    array[i], array[high] = \
        array[high], array[i]

    quick_sort(array, low, i - 1)

    quick_sort(array, i + 1, high)


# sort disciplines
quick_sort(
    disciplines,
    0,
    len(disciplines) - 1
)


quick_sort(
    slots,
    0,
    len(slots) - 1
)


capacity_conflict = []
# join discipline and slots
for i in range(len(disciplines)):
    disciplines[i]["slot"] = slots[i]
    if disciplines[i]["capacity"] > slots[i]["capacity"]:
        capacity_conflict.append(disciplines[i])


print("capacity_conflict " + str(len(capacity_conflict)))


match_quick_sort_disciplines_slot_json_str = json.dumps(disciplines, indent=4)
with open("../data/match_quick_sort_disciplines_slot.json", "w") as f:
    f.write(match_quick_sort_disciplines_slot_json_str)


# I need to check conflicts with professor time
# to do the quicksort in the same method for disciplines and slots