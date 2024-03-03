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


# check if a given text is a word representing an hour
def check_hours(text):
    if text in HOURS:
        return True
    return False


# check if a given text is a word representing a minute measure
def check_minutes(text):
    extended_digits = [
        ""
    ] + DIGITS  # add empty item to list to enable numbers like 'twenty'
    minute_numbers = HOURS[:-5] + [
        i + j for i in TENS for j in extended_digits
    ]  # compine words to form all numbers from one to fiftynine
    if text in minute_numbers:
        return True
    return False


# main checker function
def parse_time(description):
    description = description.lower()
    dimension_case = "t"
    check_minutes(description)
    extended_digits = [""] + DIGITS
    minute_numbers = HOURS[:-5] + [
        i + j for i in TENS for j in extended_digits
    ]
    re_to = r"\b(?:{})\s+to\s+\b(?:{})".format(
        "|".join(minute_numbers), "|".join(HOURS)
    )  # RE to check whether an text is of the structure "<minute> to <hour>"

    # recognizing to expression
    if re.match(re_to, description):
        match_object = re.search(re_to, description)
        sub_string = description[match_object.start() : match_object.end()]
        split_string = sub_string.split(" to ")
        minutes = 59 - minute_numbers.index(split_string[0])
        hours = HOURS.index(split_string[1])
        return datetime.time(hours, minutes)

    # purely for testing
    if re.search("o'clock", description):
        return f"o'clock found"
    if dimension_case == "t":
        return datetime.time(1, 0)
    elif dimension_case == "d":
        return datetime.datetime(2024, 2, 28)


if __name__ == "__main__":
    print(parse_time("four o'clock"))
