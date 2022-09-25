from flask import request, Response

from codeitsuisse import app


@app.route("/travelling-suisse-robot", methods=["GET", "POST"])
def travelling_suisse_robot():
    data = request.get_data()
    result = compute_path(data)
    return Response(result, mimetype="text/plain")


class State:
    def __init__(self, pos, direction, path, target, visited, path_length):
        self.pos = pos
        self.direction = direction
        self.path = path
        self.target = target
        self.visited = visited
        self.path_length = path_length


def get_shortest_path(state, dest):
    path = ""
    pos = state.pos
    direction = state.direction
    vert_move = dest[0] - pos[0]
    hori_move = dest[1] - pos[1]
    if direction == "u":
        if vert_move > 0:
            direction = "d"
            path += "RR" + "S" * abs(vert_move)
        elif vert_move < 0:
            path += "S" * abs(vert_move)
    elif direction == "d":
        if vert_move > 0:
            path += "S" * abs(vert_move)
        elif vert_move < 0:
            direction = "u"
            path += "RR" + "S" * abs(vert_move)
    elif direction == "l":
        if vert_move > 0:
            direction = "d"
            path += "L" + "S" * abs(vert_move)
        elif vert_move < 0:
            direction = "u"
            path += "R" + "S" * abs(vert_move)
    elif direction == "r":
        if vert_move > 0:
            direction = "d"
            path += "R" + "S" * abs(vert_move)
        elif vert_move < 0:
            direction = "u"
            path += "L" + "S" * abs(vert_move)

    if direction == "u":
        if hori_move > 0:
            direction = "r"
            path += "R" + "S" * abs(hori_move)
        elif hori_move < 0:
            direction = "l"
            path += "L" + "S" * abs(hori_move)
    elif direction == "d":
        if hori_move > 0:
            direction = "r"
            path += "L" + "S" * abs(hori_move)
        elif hori_move < 0:
            direction = "l"
            path += "R" + "S" * abs(hori_move)
    elif direction == "l":
        if hori_move > 0:
            direction = "r"
            path += "RR" + "S" * abs(hori_move)
        elif hori_move < 0:
            path += "S" * abs(hori_move)
    elif direction == "r":
        if hori_move > 0:
            path += "S" * abs(hori_move)
        elif hori_move < 0:
            direction = "l"
            path += "RR" + "S" * abs(hori_move)
    path += "P"
    visited = state.visited.copy()
    visited.append(dest)
    target = "" if len(state.target) == 1 else state.target[1:]
    return State(
        dest,
        direction,
        state.path + path,
        target,
        visited,
        state.path_length + abs(hori_move) + abs(vert_move),
    )


def compute_path(data):
    data = str(data, "utf-8")
    data = data.split("\\n\r\n")
    rows = len(data)
    cols = len(data[0])
    map = {}
    for i in range(rows):
        for j in range(cols):
            val = data[i][j]
            if val != " " and val in map.keys():
                map[val].append((i, j))
            else:
                map[val] = [(i, j)]
    pos = map.get("X")
    start = State(pos[0], "u", "", "CODEITSUISSE", [], 0)
    ends = []
    search(ends, start, map)
    best = ends[0]
    if len(ends) > 1:
        for state in ends[1:]:
            if best.path_length > state.path_length:
                best = state
    return best.path


def search(ends, state, map):
    if state and state.target == "":
        return state
    target_letter = state.target[0]
    if len(map.get(target_letter)) == 1:
        next_state = get_shortest_path(state, map.get(target_letter)[0])
        next_state = search(ends, next_state, map)
        if next_state:
            ends.append(next_state)
    else:
        for location in map.get(target_letter):
            if location not in state.visited:
                next_state = get_shortest_path(state, location)
                next_state = search(ends, next_state, map)
                if next_state:
                    ends.append(next_state)
