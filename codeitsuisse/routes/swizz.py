import json

from typing import Any, List, Dict
from flask import request, Response
from codeitsuisse import app


@app.route("/stig/warmup", methods=["GET", "POST"])
def stig_warmup():
    data = request.get_json()
    res = get_accuracies(data)
    return json.dumps(res)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def get_accuracies(data: Any) -> List[Dict[str, int]]:
    return [
        get_accuracy(interview["questions"], interview["maxRating"])
        for interview in data
    ]


def get_accuracy(questions: List[Dict[str, int]], max_rating: int) -> Dict[str, int]:
    record = [0 for _ in range(max_rating + 2)]
    for q in questions:
        lower = q["lower"]
        upper = q["upper"]
        record[lower] += 1
        record[upper + 1] -= 1
    accounted = 0
    counter = 0
    for i in range(1, max_rating + 1):
        num = record[i]
        counter += num
        if counter > 0:
            accounted += 1
    greatest_common_factor = gcd(accounted, max_rating)
    return {
        "p": accounted // greatest_common_factor,
        "q": max_rating // greatest_common_factor,
    }


def main():
    data = [
        {
            "questions": [
                {
                    "lower": 2,
                    "upper": 3,
                }
            ],
            "maxRating": 5,
        }
    ]
    expected = [
        {
            "p": 2,
            "q": 5,
        }
    ]
    output = get_accuracies(data)
    print(f"{output=}")
    if output != expected:
        print(f"{output=}")
        print(f"{expected=}")
