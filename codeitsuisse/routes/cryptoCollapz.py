from flask import request, jsonify

from codeitsuisse import app

mem = {}


@app.route("/cryptocollapz", methods=["GET", "POST"])
def cryptocollapz():
    data = request.get_json()
    result = crypto_collapz(data)
    return jsonify(result)


def collatz(number):
    if number % 2 == 0:
        return number // 2
    elif number % 2 == 1:
        return 3 * number + 1


def apply(lst):
    return list(map(compute, lst))


def crypto_collapz(numbers):
    return list(map(apply, numbers))


def compute(val):

    global mem

    if val in mem:
        return mem[val]

    if val == 1:
        mem[val] = 4
        return 4

    if (val and not (val & (val - 1))) and val >= 4:
        mem[val] = val
        return mem[val]

    if val % 2 == 0:
        m = max(val, val // 2, compute(val // 2))
        if val in mem and m > mem[val]:
            mem[val] = m
        else:
            mem[val] = m

        return mem[val]

    else:
        m = max(val * 3 + 1, compute(val * 3 + 1))
        if val in mem and m > mem[val]:
            mem[val] = m
        else:
            mem[val] = m
        return mem[val]
