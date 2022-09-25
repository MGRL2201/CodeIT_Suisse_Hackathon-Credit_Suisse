import json

from flask import request
import calendar

from codeitsuisse import app


@app.route("/calendarDays", methods=["GET", "POST"])
def calendarDays():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    input = data.get("numbers")
    result_p1 = part1(input)
    result_p2 = part2(result_p1)
    json_obj = {"part1": result_p1, "part2": result_p2}

    return json.dumps(json_obj)


# how many days to increment by for each month
days = {
    1: 0,
    2: 31,
    3: 59,
    4: 90,
    5: 120,
    6: 151,
    7: 181,
    8: 212,
    9: 243,
    10: 273,
    11: 304,
    12: 334,
}

days_leap = {
    1: 0,
    2: 31,
    3: 60,
    4: 91,
    5: 121,
    6: 152,
    7: 182,
    8: 213,
    9: 244,
    10: 274,
    11: 305,
    12: 335,
}


def get_month(day, year):
    if day <= 0:
        return -1
    for i in range(1, 13):
        month = get_weeks(i, year)
        month_flat = [day for week in month for day in week]
        if day in month_flat:
            return i
    return -1


def get_weekends(month, year):
    months = get_weeks(month, year)
    weekends = []
    for elem in months:
        weekends += elem[5:7]
    return weekends


def get_weekends_separated(month, year):
    months = get_weeks(month, year)
    weekends = []
    for elem in months:
        weekends.append(elem[5:7])
    return weekends


def get_week_days(month, year):
    months = get_weeks(month, year)
    weekdays = []
    for elem in months:
        weekdays += elem[0:5]
    return weekdays


def get_week_days_separated(month, year):
    months = get_weeks(month, year)
    weekdays = []
    for elem in months:
        weekdays.append(elem[0:5])
    return weekdays


def get_weeks(month, year):
    is_leap = (year % 400 == 0) or ((year % 100 != 0) and (year % 4 == 0))
    if not is_leap:
        return list(
            map(
                lambda x: [i + days[month] if i != 0 else i + 0 for i in x],
                calendar.Calendar().monthdayscalendar(year, month),
            )
        )
    return list(
        map(
            lambda x: [i + days_leap[month] if i != 0 else i + 0 for i in x],
            calendar.Calendar().monthdayscalendar(year, month),
        )
    )


def get_day(day, month, year):
    months = get_weeks(month, year)
    for month in months:
        if day in month:
            return month.index(day)
    return -1


def part1(input):
    year = input[0]
    days = input[1:]

    res_list = [[" ", " ", " ", " ", " ", " ", " "] for i in range(12)]

    def get_res(week_day, month):
        if week_day == 0:
            res_list[month - 1][week_day] = "m"
        elif week_day == 1:
            res_list[month - 1][week_day] = "t"
        elif week_day == 2:
            res_list[month - 1][week_day] = "w"
        elif week_day == 3:
            res_list[month - 1][week_day] = "t"
        elif week_day == 4:
            res_list[month - 1][week_day] = "f"
        elif week_day == 5:
            res_list[month - 1][week_day] = "s"
        elif week_day == 6:
            res_list[month - 1][week_day] = "s"

    for day in days:

        month = get_month(day, year)
        if month != -1:
            week_day = get_day(day, month, year)
            get_res(week_day, month)

    for i in range(len(res_list)):
        if res_list[i] == ["m", "t", "w", "t", "f", "s", "s"]:
            res_list[i] = ["alldays"]
        elif res_list[i] == ["m", "t", "w", "t", "f", " ", " "]:
            res_list[i] = ["weekday"]
        elif res_list[i] == [" ", " ", " ", " ", " ", "s", "s"]:
            res_list[i] = ["weekend"]

    return ",".join(["".join(elem) for elem in res_list]) + ","
    # print(res_list)


def part2(part1_out):
    index = 0
    for i in range(len(part1_out)):
        if part1_out[i] == " ":
            index = i
            break
    new_year = 2001 + index

    output = [new_year]

    temp = part1_out.split(",")

    for i in range(len(temp)):
        elem = temp[i]
        if elem == "weekend":
            output += get_weekends_separated(i + 1, new_year)[1]
        elif elem == "weekday":
            output += get_week_days_separated(i + 1, new_year)[1]

        elif elem == "alldays":

            output += get_weeks(i + 1, new_year)[1]
        else:
            for j in range(len(elem)):
                if elem[j] != " ":
                    output.append(get_weeks(i + 1, new_year)[1][j])

    return output
