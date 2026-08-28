professor = []
for i in range(professor_quantity):
    professor.append({
        "name": "P" + str(i),
        "disciplines_capacity": random.randint(1, 5),
        "disciplines_quantity": 0
    })

group = []
group_quantity = random.randint(40, 100)

for i in range(group_quantity):
    discipline_capacity = random.randint(5, 7)
    for j in range(discipline_capacity):
        group.append({
            "name": "G" + str(i),

        })