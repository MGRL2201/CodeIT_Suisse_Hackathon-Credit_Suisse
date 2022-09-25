from collections import OrderedDict
from decimal import Decimal
import json

from flask import request, jsonify
from codeitsuisse import app


@app.route("/instantiateDNSLookup", methods=["GET", "POST"])
def part_1():
    data = request.get_json()

    with open("data.json", "w") as f:
        json.dump(data, f)

    resp = {"success": "true"}
    return jsonify(resp)


@app.route("/simulateQuery", methods=["GET", "POST"])
def part_2():
    data = request.get_json()
    cache_size = data.get("cache_size")
    log = data.get("log")

    with open("data.json", "r") as f:
        db = json.load(f)["lookupTable"]

    return jsonify(helper(cache_size, log, db))


class Cache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        if key in self.cache:
            value = self.cache[key]
            del self.cache[key]
            self.cache[key] = value
            return self.cache[key]
        return ""

    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            for k in self.cache:
                del self.cache[k]
                break


def helper(cache_size, log, db):
    cache = Cache(cache_size)
    res = []
    for item in log:
        val = cache.get(item)
        if val == "":
            if item not in db:
                res.append({"status": "invalid", "ipAddress": None})
            else:
                cache.put(item, db[item])
                res.append({"status": "cache miss", "ipAddress": db[item]})
        else:
            res.append({"status": "cache hit", "ipAddress": val})
    return res
