import datetime
import re

import ephem

current_date = datetime.datetime.now().date()
current_time = datetime.datetime.now().time()
current_weekday = datetime.datetime.now().weekday()


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

DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
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


# takes a string of type
# "<number> <time unit> <number> <time unit> ..."
# and returns datetime.timedelta
# e.g: >>>parse_interval("an hour twentysix minutes")
#         datetime.timedelta(seconds=5160)
def parse_interval(string):
    s = string.split()
    interval = datetime.timedelta()
    l = len(s)
    pars = {}
    for i in range(0, l, 2):
        if s[i] in ["a", "an"]:
            n = 1
            s[i + 1] += "s"
        elif s[i] in MINUTES:
            n = MINUTES.index(s[i]) + 1
        else:
            raise ValueError("Invalid string format")
        if s[i + 1] in ["minutes", "hours", "days", "weeks"]:
            pars[s[i + 1]] = n
        else:
            raise ValueError("Invalid string format")
    return datetime.timedelta(**pars)


def check_ago(description, current_time):
    re_ago = (
        rf"\b(?:{'|'.join(DIGITS + TENS)})\s+ago\s+\b(?:{'|'.join(HOURS)})"
    )

    if match_object := re.search(re_ago, description):
        sub_string = description[match_object.start() : match_object.end()]
        split_string = sub_string.split(" ago")
        minutes = DIGITS.index(split_string[0]) + 1
        hours = HOURS.index(split_string[1].strip()) + 1
        return datetime.datetime.combine(
            current_date, datetime.time(f"{hours:02d}", f"{minutes:02d}")
        )
    return False


def check_tomorrow(description):
    re_tomorrow = rf"\b(?:{'|'.join(DAYS)})\s+tomorrow\b"

    if match_object := re.search(re_tomorrow, description):
        return current_date + datetime.timedelta(days=1)
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
    re_oclock = r"\s+o'?clock"
    if matched := re.search(re_oclock, description):
        return description[: matched.start()] + description[matched.end() :]
    return description


def check_basic_time(description):
    re_basic = r"\b({})\s*({})?".format("|".join(HOURS), "|".join(MINUTES))
    if matched := re.match(re_basic, description):
        hour = HOURS.index(matched.group(1)) + 1
        minutes = (
            MINUTES.index(matched.group(2)) + 1 if matched.group(2) else 0
        )
        return datetime.time(hour, minutes)


def check_easter(description):
    re_easter = r"(\bnext\s)?easter"
    if matched := re.search(re_easter, description):
        equinox = ephem.localtime(ephem.next_equinox(ephem.now()))
        full_moon = ephem.localtime(
            ephem.next_full_moon(equinox - datetime.timedelta(days=1))
        )
        weekday_fullmoon = full_moon.weekday()
        diff_to_sunday = 6 - weekday_fullmoon
        easter_date = full_moon + datetime.timedelta(days=diff_to_sunday)
        return easter_date.date()


def check_ramadan(description):
    re_ramadan = r"\b(?:start\s+of\s+)?ramadan\b"
    if matched := re.search(re_ramadan, description):
        ramadan_date = datetime.date(1, 1, 1)  # placeholder for actual value
        return ramadan_date.date()


def check_hebrew_new_year(description):
    re_hebrew_new_year = r"\b(?:hebrew\s+new\s+year|rosh\s+hashanah)\b"
    if matched := re.search(re_hebrew_new_year, description):
        hebrew_new_year_date = datetime.date(1, 1, 1)  # placeholder again
        return hebrew_new_year_date


# function that returns datetime.datetime from a description of a
# fixed datetime. Maybe useful?
def parse_fixed_time(description):
    True


# function that returns datetime.datetime of a description of a
# single datetime point (it can be fixed or relative)
def parse_point_time(description):
    output_date = None
    output_time = None
    description = description.lower()
    dimension_case = "t"

    # convert fractions to minutes
    description = convert_fractions(description)
    # remove o'clock
    description = check_oclock(description)
    if check_easter_result := check_easter(description):
        output_date = check_easter_result
    if check_ago_result := check_ago(description, current_time):
        output_time = check_ago_result  # datetime.datetime object
    elif check_tomorrow_result := check_tomorrow(description):
        output_date = current_date + datetime.timedelta(days=1)
    if check_to_result := check_to(description):
        output_time = check_to_result  # datetime.time object
    elif check_past_result := check_past(description):
        output_time = check_past_result  # datetime.time object
    elif check_basic_result := check_basic_time(description):
        output_time = check_basic_result  # datetime.time object
    if output_date and output_time:
        return datetime.datetime.combine(output_date, output_time)
    elif output_date:
        return output_date
    elif output_time:
        return output_time
    else:
        return datetime.time(1, 0)  # default


# function that checks for <from <datetime1> to <datetime2>> and returns
# a tuple of (datetime.datetime,datetime.datetime)
def check_from_to(des):
    re_from = r"\bfrom\s+"
    re_to = r"\bto\s+"
    if not (match_from := re.search(re_from, des)):
        return False
    match_to = re.search(re_to, des)

    des_left = des[match_from.end() : match_to.start()]
    dt_left = parse_point_time(des_left)

    des_right = des[match_to.end() :]
    dt_right = parse_point_time(des_right)

    if match_from.start() == 0:
        return (dt_left, dt_right)
    else:
        des_bef = des[: match_from.start()]
        date_bef = parse_point_time(des_bef)
        return (
            datetime.datetime.combine(date_bef, dt_left),
            datetime.datetime.combine(date_bef, dt_right),
        )


def check_for(des):
    re_for = r"\bfor\s+"
    if not (match_for := re.search(re_for, des)):
        return False
    des_left = des[0]


# main checker function
def parse_time(description):
    output_date = None
    output_time = None
    description = description.lower()
    dimension_case = "t"

    # convert fractions to minutes
    description = convert_fractions(description)
    # remove o'clock
    description = check_oclock(description)
    if check_easter_result := check_easter(description):
        output_date = check_easter_result
    if check_ago_result := check_ago(description, current_time):
        output_time = check_ago_result  # datetime.datetime object
    elif check_tomorrow_result := check_tomorrow(description):
        output_date = current_date + datetime.timedelta(days=1)
    if check_to_result := check_to(description):
        output_time = check_to_result  # datetime.time object
    elif check_past_result := check_past(description):
        output_time = check_past_result  # datetime.time object
    elif check_basic_result := check_basic_time(description):
        output_time = check_basic_result  # datetime.time object
    if output_date and output_time:
        return datetime.datetime.combine(output_date, output_time)
    elif output_date:
        return output_date
    elif output_time:
        return output_time.date()  # Return only the date part
    else:
        return datetime.time(1, 0)  # default


if __name__ == "__main__":
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    current_weekday = datetime.datetime.now().weekday()

    print(parse_time("tomorrow"))
