import json

with open("../data/group.json", "r") as file:
    groups = json.load(file)

# mapping disciplines
disciplines = [
    {
        **discipline,
        "group_id": group["id"]
    }
    for group in groups
    for discipline in group["disciplines"]
]

disciplines.sort(key=lambda discipline: discipline["capacity"], reverse=True)


def build_conflict_graph():
    # creating a hash map for disciplines
    graph_set = {
        discipline["id"]: set()
        for discipline in disciplines
    }

    for i in range(len(disciplines)):
        for j in range(i + 1, len(disciplines)):

            d1 = disciplines[i]
            d2 = disciplines[j]

            same_professor = (
                    d1["professor"]["id"] == d2["professor"]["id"]
            )

            if same_professor:
                graph_set[d1["id"]].add(d2["id"])
                graph_set[d2["id"]].add(d1["id"])

    return graph_set
graph = build_conflict_graph()

#gpt code#
def welsh_powell():
    # Collect all vertices, including neighbors
    vertices = set(graph.keys())

    for neighbors in graph.values():
        vertices.update(neighbors)

    # Sort by degree (highest number of conflicts first)
    vertices = sorted(
        vertices,
        key=lambda vertex: len(graph.get(vertex, set())),
        reverse=True
    )

    colors = {}
    current_color = 0

    while len(colors) < len(vertices):

        # Find first uncolored vertex
        for vertex in vertices:
            if vertex not in colors:
                colors[vertex] = current_color
                break

        # Try to assign the same color to compatible vertices
        for vertex in vertices:
            if vertex in colors:
                continue

            # Check whether this vertex conflicts with
            # another vertex using the current color
            conflict = any(
                neighbor in colors and colors[neighbor] == current_color
                for neighbor in graph.get(vertex, set())
            )

            if not conflict:
                colors[vertex] = current_color

        current_color += 1

    return colors


colors = welsh_powell()

graph_json = {
    node: list(conflicts)
    for node, conflicts in graph.items()
}

graph_json_str = json.dumps(graph_json, indent=4)
with open("../data/graph_engine/graph.json", "w") as f:
    f.write(graph_json_str)

colors_json_str = json.dumps(colors, indent=4)
with open("../data/graph_engine/welsh_powell_colors.json", "w") as f:
    f.write(colors_json_str)


