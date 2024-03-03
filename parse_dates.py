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

EXTENDED_DIGITS = [
    ""
] + DIGITS  # add empty item to list to enable numbers like 'twenty'

MINUTES = HOURS[:-5] + [i + j for i in TENS for j in EXTENDED_DIGITS]


# check if a given text is a word representing an hour
def check_hours(text):
    if text in HOURS:
        return True
    return False


# check if a given text is a word representing a minute measure
def check_minutes(text):
    # compine words to form all numbers from one to fiftynine
    if text in MINUTES:
        return True
    return False


def check_to(description):
    re_to = r"\b(?:{})\s+to\s+\b(?:{})".format(
        "|".join(MINUTES), "|".join(HOURS)
    )  # RE to check whether an text is of the structure "<minute> to <hour>"

    # recognizing to expression
    if match_object := re.search(re_to, description):
        sub_string = description[match_object.start() : match_object.end()]
        split_string = sub_string.split(" to ")
        minutes = 59 - MINUTES.index(split_string[0])
        hours = HOURS.index(split_string[1])
        return datetime.time(hours, minutes)
    return False


def check_past(description):
    re_past = r"\b(?:{})\s+past\s+\b(?:{})".format(
        "|".join(MINUTES), "|".join(HOURS)
    )  # RE to check whether an text is of the structure "<minute> past <hour>"

    # recognizing past expression
    if match_object := re.search(re_past, description):
        sub_string = description[match_object.start() : match_object.end()]
        split_string = sub_string.split(" past ")
        minutes = MINUTES.index(split_string[0]) + 1
        hours = HOURS.index(split_string[1]) + 1
        return datetime.time(hours, minutes)
    return False


# function that converts occurences of fractions
def convert_fractions(description):
    common_fractions = ["quarter", "half"]
    values = ["fifteen", "thirty"]
    re_fractions = r"\b(a\s)?({})\s((to\s)|(past\s)?)".format(
        "|".join(common_fractions)
    )
    adjusted_description = description
    matches = list(re.finditer(re_fractions, description))
    if any(matches):
        for matched in matches:
            addition = ""
            if matched.group(5):
                addition = " past "
            else:
                addition = " to "
            adjusted_description = (
                adjusted_description[: matched.start()]
                + values[common_fractions.index(matched.group(2))]
                + addition
                + adjusted_description[matched.end() :]
            )
    return adjusted_description


# function that checks for "<hour> o'clock" and returns a datetime.time object
def check_oclock(description):
    re_oclock = r"\b({})\s+o'?clock".format("|".join(HOURS))
    if matched := re.search(re_oclock, description):
        return datetime.time(HOURS.index(matched.group(1)) + 1, 0)


# main checker function
def parse_time(description):
    description = description.lower()
    dimension_case = "t"

    # convert fractions to minutes
    description = convert_fractions(description)

    if check_to_result := check_to(description):
        return check_to_result  # datetime.time object
    if check_past_result := check_past(description):
        return check_past_result  # datetime.time object
    if check_oclock_result := check_oclock(description):
        return check_oclock_result  # datetime.time object
    # purely for testing
    if re.search("o'clock", description):
        return f"o'clock found"
    if dimension_case == "t":
        return datetime.time(1, 0)
    elif dimension_case == "d":
        return datetime.datetime(2024, 2, 28)


if __name__ == "__main__":
    print(parse_time("four o'clock"))
