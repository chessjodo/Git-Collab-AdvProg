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


def check_to(description):
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
    return False


def convert_fractions(description):
    common_fractions = ["quarter", "half"]
    values = ["fifteen", "thirty"]
    re_fractions = r"\b(a )?({})".format("|".join(common_fractions))
    adjusted_description = description
    if matched := re.match(re_fractions, description):
        adjusted_description = (
            description[: matched.start()]
            + values[common_fractions.index(matched.group(2))]
            + description[matched.end() :]
        )
        print("NEW DESCRIPTION", adjusted_description)
    return adjusted_description


# main checker function
def parse_time(description):
    description = description.lower()
    dimension_case = "t"
    # convert fractions to minutes
    description = convert_fractions(description)
    if check_to_result := check_to(description):
        return check_to_result
    # purely for testing
    if re.search("o'clock", description):
        return f"o'clock found"
    if dimension_case == "t":
        return datetime.time(1, 0)
    elif dimension_case == "d":
        return datetime.datetime(2024, 2, 28)


if __name__ == "__main__":
    print(parse_time("four o'clock"))
