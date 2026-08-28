import json

with open("../data/group.json", "r") as file:
    groups = json.load(file)

with open("../data/room.json", "r") as file:
    rooms = json.load(file)

total_disciplines = sum(
    group["discipline_quantity"]
    for group in groups
)

print("disciplines " + str(total_disciplines))
print("slots " + str(len(rooms[0]['time_slots']) * 50 * 4))

# available_slots = [
#     room
#     for room in rooms
#     for time in room['time_slots']
#     for slot in time['times']
#     if slot['is_available'] == True
# ]

if rooms[0]['time_slots'][0]['times'][0]['is_available']:
    print("available")
else:
    print("unavailable")



print(groups[0]['capacity'])
print(groups[0]['disciplines'][0])

#
# for group in groups:
#     for discipline in group['disciplines']:
#         for room in rooms:
#             if room['time_slots'][0]['times'][0]['is_available']
#                 and :
#                 rooms['time_slots'][0]['times'][0]['is_available'] = False
#                 rooms['time_slots'][0]['times'][0]['group'] = group
#                 rooms['time_slots'][0]['times'][0]['discipline'] = discipline




