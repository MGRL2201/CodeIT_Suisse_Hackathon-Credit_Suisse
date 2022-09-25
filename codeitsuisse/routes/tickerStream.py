import json

from flask import request, jsonify

from codeitsuisse import app


@app.route("/tickerStreamPart1", methods=["GET", "POST"])
def tickerStreamPart1():
    data = request.get_json()
    inputValue = data.get("stream")
    result = to_cumulative(inputValue)
    json_obj = {"output": result}
    return json.dumps(json_obj)


@app.route("/tickerStreamPart2", methods=["GET", "POST"])
def tickerStreamPart2():
    data = request.get_json()
    inputValue1 = data.get("stream")
    inputValue2 = data.get("quantityBlock")
    result = to_cumulative_delayed(inputValue1, inputValue2)
    json_obj = {"output": result}
    return json.dumps(json_obj)


# returns if the new quantity makes a new block
def is_new_block(prev_qty: int, qty_block, qty):
    dist = qty_block - prev_qty % qty_block
    return qty >= dist


# makes string for to_cumulative values
def get_str(ticker: str, cum_qty: int, cum_notional: float):
    res = ",".join([ticker, str(cum_qty), str(round(cum_notional, 2))])
    return res


# makes string for to_cumulative_delayed values
def get_delayed_str(
    ticker: str, curr_qty: int, curr_notional: float, excess: str, price: float
):
    block = str(curr_qty - excess)
    block_notional = str(round(curr_notional - (excess * price), 2))
    res = ",".join([ticker, block, block_notional])
    return res


# performs the additional calulations needed for the delayed version
def do_delayed(
    ticker: str,
    curr_qty: int,
    prev_qty: int,
    curr_notional: float,
    qty_block: int,
    price: float,
):
    excess = curr_qty % qty_block
    qty = curr_qty - prev_qty
    if is_new_block(prev_qty, qty_block, qty):
        excess = curr_qty % qty_block
        val = get_delayed_str(ticker, curr_qty, curr_notional, excess, float(price))
    else:
        val = ""
    return val


# returns a list of strings given a dictionary
def join_string(map: dict()):
    res = []
    for key in map.keys():
        temp = map.get(key)
        s = []
        for k in temp:
            s.append(temp.get(k))
        s = ",".join(s)
        res.append(key + "," + s)
    return res


# performs the calculations for the to_cumulative functions
# delayed and qty_block are arguments for to_cumulative_delay
def cumulate(stream: list, delayed: bool = False, qty_block: int = 0):
    # store ticker and cumulative values in dictionary with timestamp as key
    map = {}
    # store cumulative values in dictionary with ticker as key
    cumulative_map = {}
    # loop through list and compute cumulative values, adding them to the
    # cumulative map. Also adds strings to a list stored in the map which is
    # used later for generating the output
    for item in stream:
        ts, ticker, qty, price = item.split(",")
        notional = float(qty) * float(price)
        # add cumulative notional and qty to cumulative map
        if ticker in cumulative_map.keys():
            prev_qty, prev_notional = cumulative_map.get(ticker)
            curr_qty = prev_qty + int(qty)
            curr_notional = prev_notional + notional
        else:
            prev_qty = 0
            curr_qty, curr_notional = int(qty), notional
        cumulative_map[ticker] = (curr_qty, curr_notional)

        # perform calculations for delayed version
        if delayed:
            val = do_delayed(
                ticker, curr_qty, prev_qty, curr_notional, qty_block, price
            )
        # get string for normal version
        else:
            val = get_str(ticker, curr_qty, curr_notional)

        # add string to map if exists
        if val and ts in map.keys():
            map[ts][ticker] = val
        elif val:
            map[ts] = {ticker: val}

    # generate output from map and return
    return join_string(map)


def to_cumulative(stream: list):
    """
    Assumptions made:
      1. tickers are case sensitive, 'a' is different from 'A', sorted
         in order of python string comparison. i.e. A-Z and a-z are in order,
         however use of a-z and A-Z will not have A < a < B < b. May have
         A-Z before a-z.
      2. tickers do not appear multiple times at the same timestamp
         however they can be repeated throughout different timestamps
    """
    stream.sort()
    return cumulate(stream)


def to_cumulative_delayed(stream: list, quantity_block: int):
    """
    Assumptions made:
      1. same as above
      2. only the maximum block achieved is displayed in the output
         e.g. if current qty is 3 and qty_block is 5, if new qty is 8,
         output will display a cumulative qty of 10 rather than 5 and 10.
    """
    stream.sort()
    return cumulate(stream, True, quantity_block)
