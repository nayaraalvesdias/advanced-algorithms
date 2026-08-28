import heapq


def interval_partitioning(intervals):
    """
    Finds the minimum number of resources (e.g., classrooms) required
    to schedule all intervals without overlaps.

    Parameters:
    intervals (list of tuples): A list where each tuple is (start_time, end_time)

    Returns:
    int: The minimum number of resources required.
    list of lists: The actual schedule grouping the intervals by resource.
    """
    if not intervals:
        return 0, []

    # 1. Sort intervals by their start times.
    # Keep track of the original index/interval structure if needed,
    # but sorting tuples directly works by the first element.
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    # 2. Initialize a min-heap to track the end times of active resources.
    # Store tuples in the heap: (end_time, resource_id)
    rooms_heap = []

    # Track the actual schedules for each room
    # room_schedules[i] will hold the intervals assigned to room i
    room_schedules = []

    # 3. Process each interval sequentially
    for start, end in sorted_intervals:

        # Check if the room that frees up the earliest is available
        if rooms_heap and rooms_heap[0][0] <= start:
            # Re-use this room: remove its old end time from the heap
            _, room_id = heapq.heappop(rooms_heap)
        else:
            # Allocate a brand-new room
            room_id = len(room_schedules)
            room_schedules.append([])

        # Assign the current interval to the chosen room
        room_schedules[room_id].append((start, end))

        # Push the updated end time of this room back into the heap
        heapq.heappush(rooms_heap, (end, room_id))

    # The total number of rooms allocated is the length of our schedule list
    min_rooms = len(room_schedules)

    return min_rooms, room_schedules


# --- Example Usage ---
if __name__ == "__main__":
    # Example: A list of (start, end) times for lectures
    lectures = [(9, 10.5), (9, 12.5), (10.5, 12.5), (11, 14), (13, 14.5), (14, 16.5)]

    total_rooms, schedule = interval_partitioning(lectures)

    print(f"Minimum rooms required: {total_rooms}\n")
    for room_num, assigned_lectures in enumerate(schedule):
        print(f"Room {room_num + 1}: {assigned_lectures}")
