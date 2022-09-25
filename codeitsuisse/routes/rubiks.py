import json

from flask import request, jsonify

from codeitsuisse import app


@app.route("/rubiks", methods=["GET", "POST"])
def rubiks():
    data = request.get_json()
    inputValue1 = data.get("ops")
    inputValue2 = data.get("state")
    result = make_moves(inputValue1, inputValue2)
    json_obj = result
    return json.dumps(json_obj)


def rotate_clockwise(side):
    N = len(side[0])
    for i in range(N // 2):
        for j in range(i, N - i - 1):
            temp = side[i][j]
            side[i][j] = side[N - 1 - j][i]
            side[N - 1 - j][i] = side[N - 1 - i][N - 1 - j]
            side[N - 1 - i][N - 1 - j] = side[j][N - 1 - i]
            side[j][N - 1 - i] = temp


def rotate_anticlockwise(side):
    N = len(side[0])
    for i in range(0, int(N / 2)):
        for j in range(i, N - i - 1):
            temp = side[i][j]
            side[i][j] = side[j][N - 1 - i]
            side[j][N - 1 - i] = side[N - 1 - i][N - 1 - j]
            side[N - 1 - i][N - 1 - j] = side[N - 1 - j][i]
            side[N - 1 - j][i] = temp


def copy_2d(matrix):
    res = []
    for row in matrix:
        res.append(row.copy())
    return res


def clockwise_move(op, state):
    if op == "u":
        rotate_clockwise(state["u"])
        temp = state["f"][0].copy()
        state["f"][0] = state["r"][0]
        state["r"][0] = state["b"][0]
        state["b"][0] = state["l"][0]
        state["l"][0] = temp
    if op == "d":
        rotate_clockwise(state["d"])
        temp = state["f"][2].copy()
        state["f"][2] = state["l"][2]
        state["l"][2] = state["b"][2]
        state["b"][2] = state["r"][2]
        state["r"][2] = temp
    if op == "l":
        rotate_clockwise(state["l"])
        temp = [state["f"][0][0], state["f"][1][0], state["f"][2][0]]
        state["f"][0][0] = state["u"][0][0]
        state["f"][1][0] = state["u"][1][0]
        state["f"][2][0] = state["u"][2][0]
        state["u"][0][0] = state["b"][2][2]
        state["u"][1][0] = state["b"][1][2]
        state["u"][2][0] = state["b"][0][2]
        state["b"][2][2] = state["d"][0][0]
        state["b"][1][2] = state["d"][1][0]
        state["b"][0][2] = state["d"][2][0]
        state["d"][0][0] = temp[0]
        state["d"][1][0] = temp[1]
        state["d"][2][0] = temp[2]
    if op == "r":
        rotate_clockwise(state["r"])
        temp = [state["f"][0][2], state["f"][1][2], state["f"][2][2]]
        state["f"][0][2] = state["d"][0][2]
        state["f"][1][2] = state["d"][1][2]
        state["f"][2][2] = state["d"][2][2]
        state["d"][0][2] = state["b"][2][0]
        state["d"][1][2] = state["b"][1][0]
        state["d"][2][2] = state["b"][0][0]
        state["b"][2][0] = state["u"][0][2]
        state["b"][1][0] = state["u"][1][2]
        state["b"][0][0] = state["u"][2][2]
        state["u"][0][2] = temp[0]
        state["u"][1][2] = temp[1]
        state["u"][2][2] = temp[2]
    if op == "f":
        rotate_clockwise(state["f"])
        temp = state["u"][2].copy()
        state["u"][2][0] = state["l"][2][2]
        state["u"][2][1] = state["l"][1][2]
        state["u"][2][2] = state["l"][0][2]
        state["l"][0][2] = state["d"][0][0]
        state["l"][1][2] = state["d"][0][1]
        state["l"][2][2] = state["d"][0][2]
        state["d"][0][0] = state["r"][2][0]
        state["d"][0][1] = state["r"][1][0]
        state["d"][0][2] = state["r"][0][0]
        state["r"][2][0] = temp[2]
        state["r"][1][0] = temp[1]
        state["r"][0][0] = temp[0]
    if op == "b":
        rotate_clockwise(state["b"])
        temp = state["u"][0].copy()
        state["u"][0][0] = state["r"][0][2]
        state["u"][0][1] = state["r"][1][2]
        state["u"][0][2] = state["r"][2][2]
        state["r"][0][2] = state["d"][2][2]
        state["r"][1][2] = state["d"][2][1]
        state["r"][2][2] = state["d"][2][0]
        state["d"][2][2] = state["l"][2][0]
        state["d"][2][1] = state["l"][1][0]
        state["d"][2][0] = state["l"][0][0]
        state["l"][2][0] = temp[0]
        state["l"][1][0] = temp[1]
        state["l"][0][0] = temp[2]


def anticlockwise_move(op, state):
    if op == "u":
        rotate_anticlockwise(state["u"])
        temp = state["f"][0].copy()
        state["f"][0] = state["l"][0]
        state["l"][0] = state["b"][0]
        state["b"][0] = state["r"][0]
        state["r"][0] = temp
    if op == "d":
        rotate_anticlockwise(state["d"])
        temp = state["f"][2].copy()
        state["f"][2] = state["r"][2]
        state["r"][2] = state["b"][2]
        state["b"][2] = state["l"][2]
        state["l"][2] = temp
    if op == "l":
        rotate_anticlockwise(state["l"])
        temp = [state["f"][0][0], state["f"][1][0], state["f"][2][0]]
        state["f"][0][0] = state["d"][0][0]
        state["f"][1][0] = state["d"][1][0]
        state["f"][2][0] = state["d"][2][0]
        state["d"][0][0] = state["b"][2][2]
        state["d"][1][0] = state["b"][1][2]
        state["d"][2][0] = state["b"][0][2]
        state["b"][2][2] = state["u"][0][0]
        state["b"][1][2] = state["u"][1][0]
        state["b"][0][2] = state["u"][2][0]
        state["u"][0][0] = temp[0]
        state["u"][1][0] = temp[1]
        state["u"][2][0] = temp[2]
    if op == "r":
        rotate_anticlockwise(state["r"])
        temp = [state["f"][0][2], state["f"][1][2], state["f"][2][2]]
        state["f"][0][2] = state["u"][0][2]
        state["f"][1][2] = state["u"][1][2]
        state["f"][2][2] = state["u"][2][2]
        state["u"][0][2] = state["b"][2][0]
        state["u"][1][2] = state["b"][1][0]
        state["u"][2][2] = state["b"][0][0]
        state["b"][2][0] = state["d"][0][2]
        state["b"][1][0] = state["d"][1][2]
        state["b"][0][0] = state["d"][2][2]
        state["d"][0][2] = temp[0]
        state["d"][1][2] = temp[1]
        state["d"][2][2] = temp[2]
    if op == "f":
        rotate_anticlockwise(state["f"])
        temp = state["u"][2].copy()
        state["u"][2][0] = state["r"][0][0]
        state["u"][2][1] = state["r"][1][0]
        state["u"][2][2] = state["r"][2][0]
        state["r"][0][0] = state["d"][0][2]
        state["r"][1][0] = state["d"][0][1]
        state["r"][2][0] = state["d"][0][0]
        state["d"][0][0] = state["l"][0][2]
        state["d"][0][1] = state["l"][1][2]
        state["d"][0][2] = state["l"][2][2]
        state["l"][0][2] = temp[2]
        state["l"][1][2] = temp[1]
        state["l"][2][2] = temp[0]
    if op == "b":
        rotate_anticlockwise(state["b"])
        temp = state["u"][0].copy()
        state["u"][0][0] = state["l"][2][0]
        state["u"][0][1] = state["l"][1][0]
        state["u"][0][2] = state["l"][0][0]
        state["l"][2][0] = state["d"][2][2]
        state["l"][1][0] = state["d"][2][1]
        state["l"][0][0] = state["d"][2][0]
        state["d"][2][2] = state["r"][0][2]
        state["d"][2][1] = state["r"][1][2]
        state["d"][2][0] = state["r"][2][2]
        state["r"][0][2] = temp[0]
        state["r"][1][2] = temp[1]
        state["r"][2][2] = temp[2]


def make_moves(ops: str, state: dict()):
    moves = []
    for c in ops:
        if c == "i":
            moves[-1] = moves[-1] + c
        else:
            moves.append(c.lower())
    for move in moves:
        if len(move) == 1:
            clockwise_move(move, state)
        else:
            anticlockwise_move(move[0], state)
    return state
