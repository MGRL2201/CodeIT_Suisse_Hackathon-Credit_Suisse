from collections import Counter
import json
import string

from flask import request, jsonify

from codeitsuisse import app


@app.route("/quordleKeyboard", methods=["GET", "POST"])
def quordleKeyboard():
    data = request.get_json()
    print(data)
    answers = data.get("answers")
    attempts = data.get("attempts")
    numbers = data.get("numbers")
    result, compliment = part_1(answers, attempts)
    result2 = part_2(numbers, result, compliment)
    d = {"part1": result, "part2": result2}
    return json.dumps(d)


d = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
}


def part_1(answers, attempts):
    print(answers)
    print(attempts)
    ans = ""
    d1 = dict.fromkeys(string.ascii_uppercase, 0)
    d2 = dict.fromkeys(string.ascii_uppercase, -1)
    temp = "".join(answers)
    for c in temp:
        d1[c] += 1
    for index, a in enumerate(attempts):
        if a in answers:
            counts = Counter(a)
            for key in counts.keys():
                d1[key] -= counts[key]
                if d1[key] <= 0 and d2[key] == -1:
                    d2[key] = index
        else:
            for c in a:
                if d1[c] == 0 and d2[c] == -1:
                    d1[c] -= 1
                    d2[c] = index
    compliment = ""
    for key in d2.keys():
        if d2[key] != -1:
            ans += str(9 - d2[key])
        else:
            compliment += key
    m = 9

    for x in ans:
        m = min(int(x), m)
    diff = m - 1
    final_ans = ""
    for x in ans:
        final_ans += str(int(x) - diff)
    return final_ans, compliment


def part_2(numbers, part1, compliment):

    global d

    lst = []
    for i in range(0, len(numbers), 5):
        list_5 = numbers[i : i + 5]
        res = ""
        for j in list_5:
            if str(j) in part1:
                res += "1"
            else:
                res += "0"
        lst.append(d[int(res, 2) - 1])
    res = "".join(lst)
    return res + compliment
