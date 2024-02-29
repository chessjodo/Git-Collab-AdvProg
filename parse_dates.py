import datetime
import re

DIGITS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

HOURS = DIGITS + [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "twentyone",
    "twentytwo",
    "twentythree",
    "twentyfour",
]

TENS = ["twenty", "thirty", "fourty", "fifty"]


def check_hours(text):
    if text in HOURS:
        return True
    return False


def check_minutes(text):
    extended_digits = [""] + DIGITS
    minute_numbers = HOURS[:-5] + [
        i + j for i in TENS for j in extended_digits
    ]
    if text in minute_numbers:
        return True
    return False


def parse_time(description):
    dimension_case = "t"
    check_minutes(description)
    if re.search("o'clock", description):
        return f"o'clock found"
    if dimension_case == "t":
        return datetime.time(1, 0)
    elif dimension_case == "d":
        return datetime.datetime(2024, 2, 28)


if __name__ == "__main__":
    print(parse_time("four o'clock"))
