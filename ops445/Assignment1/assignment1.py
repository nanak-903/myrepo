#!/usr/bin/env python3

'''
OPS445 Assignment 1
Program: assignment1.py 
Author: "Nanak Dayal Singh Pabla"
Semester: "Summer 2025"

The python code in this file (assignment1.py) is original work written by
"Nanak Dayal Singh Pabla". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''

import sys
from datetime import datetime, timedelta

def day_of_week(year: int, month: int, date: int) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'] 
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + date) % 7
    return days[num]

def mon_max(month:int, year:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
    if month == 2:
        return 29 if leap_year(year) else 28
    days_in_month = {1:31, 3:31, 4:30, 5:31, 6:30,
                     7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    return days_in_month.get(month, 0)

def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This fucntion has been tested to work for year after 1582
    '''
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)
    lyear = year % 4
    if lyear == 0:
        feb_max = 29 # this is a leap year
    else:
        feb_max = 28 # this is not a leap year

    lyear = year % 100
    if lyear == 0:
        feb_max = 28 # this is not a leap year

    lyear = year % 400
    if lyear == 0:
        feb_max = 29 # this is a leap year

    mon_max_dict = { 1:31, 2:feb_max, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    tmp_day = day + 1  # next day

    if tmp_day > mon_max_dict[month]:
        to_day = tmp_day % mon_max_dict[month]  # if tmp_day > this month's max, reset to 1 
        tmp_month = month + 1
    else:
        to_day = tmp_day
        tmp_month = month + 0

    if tmp_month > 12:
        to_month = 1
        year = year + 1
    else:
        to_month = tmp_month + 0

    next_date = f"{year}-{to_month:02}-{to_day:02}"

    return next_date

def before(date: str) -> str:
    '''
    before() -> date for previous day in YYYY-MM-DD string format

    Return the date for the previous day of the given date in YYYY-MM-DD format.
    '''
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)
    
    # Setting leap year rules
    lyear = year % 4
    if lyear == 0:
        feb_max = 29 # This is a leap year
    else:
        feb_max = 28  # This is not a leap year
    
    lyear = year % 100
    if lyear == 0:
        feb_max = 28 # This is not a leap year
    
    lyear = year % 400
    if lyear == 0:
        feb_max = 29 # This is a leap year
    
    mon_max_dict = {1:31, 2:feb_max, 3:31, 4:30, 5:31, 6:30,
                    7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    
    # Calculating previous day by subtracting 1
    tmp_day = day - 1 # previous day
    
    if tmp_day == 0:
        tmp_month = month - 1
        if tmp_month == 0:
            tmp_month = 12
            year = year - 1
        to_day = mon_max_dict[tmp_month]
    else:
        to_day = tmp_day
        tmp_month = month + 0

    if tmp_month > 12:
        to_month = 1
        year = year + 1
    else:
        to_month = tmp_month + 0    

    # Format date string
    prev_date = f"{year}-{to_month:02}-{to_day:02}"
    
    return prev_date

def usage():
    "Print a usage message to the user"
    print("Usage: python3 assignment1.py <start date> <end date>")
    print("Dates must be in YYYY-MM-DD format, e.g. 2025-01-01")

def leap_year(year: int) -> bool:
    "return True if the year is a leap year"
    if (year % 400) == 0:
        return True
    if (year % 100) == 0:
        return False
    if (year % 4) == 0:
        return True
    return False

def valid_date(date: str) -> bool:
    "check validity of date and return True if valid"
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        # Additional check: year after 1582 as per instructions
        if dt.year < 1583:
            return False
        return True
    except ValueError:
        return False

def day_count(start_date: str, stop_date: str) -> int:
    "Loops through range of dates, and returns number of weekend days"
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        stop = datetime.strptime(stop_date, '%Y-%m-%d')
    except ValueError:
        return 0

    if start > stop:
        start, stop = stop, start

    count = 0
    current = start
    while current <= stop:
        if current.weekday() >= 5:  # Saturday=5, Sunday=6
            count += 1
        current += timedelta(days=1)
    return count


if __name__ == "__main__":
    # minimal CLI to comply with tests and usage
    
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    if not valid_date(start_date) or not valid_date(end_date):
        usage()
        sys.exit(1)

    # Sort dates so start_date <= end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    weekends = day_count(start_date, end_date)
    print(f"The period between {start_date} and {end_date} includes {weekends} weekend days")
