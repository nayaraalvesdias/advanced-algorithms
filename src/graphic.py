import matplotlib.pyplot as plt

dataset = [
    {
        "id": "R0",
        "capacity": 35,
        "time_slots": [
            {"id": "T0", "start": "07:00", "end": "09:00", "is_available": True},
            {"id": "T1", "start": "09:00", "end": "11:00", "is_available": True},
            {"id": "T2", "start": "11:00", "end": "13:00", "is_available": True},
            {"id": "T3", "start": "13:00", "end": "15:00", "is_available": True},
            {"id": "T4", "start": "15:00", "end": "18:00", "is_available": True},
            {"id": "T5", "start": "18:00", "end": "20:00", "is_available": True},
            {"id": "T6", "start": "20:00", "end": "22:00", "is_available": True},
        ]
    }
]


def time_to_hours(time_string):
    """Convert HH:MM to decimal hours."""
    hours, minutes = map(int, time_string.split(":"))
    return hours + minutes / 60


resource = dataset[0]

fig, ax = plt.subplots(figsize=(12, 7))

slots = resource["time_slots"]

# Draw vertical columns
for i, slot in enumerate(slots):

    start = time_to_hours(slot["start"])
    end = time_to_hours(slot["end"])

    duration = end - start

    ax.bar(
        i,
        duration,
        bottom=start,
        width=0.8,
        edgecolor="black",
        linewidth=1.5
    )

    # Label inside column
    ax.text(
        i,
        (start + end) / 2,
        f'{slot["id"]}\n'
        f'{slot["start"]} - {slot["end"]}',
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold"
    )


# X axis = time slots
ax.set_xticks(range(len(slots)))

ax.set_xticklabels(
    [slot["id"] for slot in slots]
)

ax.set_xlabel("Time Slot")

# Y axis = actual time
ax.set_ylim(7, 22)

ax.set_yticks(range(7, 23))

ax.set_yticklabels(
    [f"{hour:02d}:00" for hour in range(7, 23)]
)

ax.set_ylabel("Time")


# Title
ax.set_title(
    f'Time Schedule — {resource["id"]} | Capacity: {resource["capacity"]}',
    fontsize=16,
    fontweight="bold"
)

# Grid
ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()