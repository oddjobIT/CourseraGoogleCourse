#!/usr/bin/env python3


import csv
import datetime
import requests


FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"



def get_start_date():
  """Interactively get the start date to query for."""

  print()
  print('Getting the first start date to query for.')
  print()
  print('The date must be greater than Jan 1st, 2018')
  year = int(input('Enter a value for the year: '))
  month = int(input('Enter a value for the month: '))
  day = int(input('Enter a value for the day: '))
  print()

  return datetime.datetime(year, month, day)


def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

  # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines


url = FILE_URL


def get_same_or_newer():
  #Returns the employees that started on the given date, or the closest one.
  data = get_file_lines(FILE_URL)
  reader = csv.reader(data[1:])
  d={}
  [d.setdefault( datetime.datetime.strptime(row['Start Date'], '%Y-%m-%d'), []).append(row['Name']+' '+ row['Surname']) for row in csv.DictReader(data)]
  employeeStartDateDict = sorted(d.items(),reverse=True)
  # We want all employees that started at the same date or the closest newer
  # date. To calculate that, we go through all the data and find the
  # employees that started on the smallest date that's equal or bigger than
  # the given start date.
  min_date = datetime.datetime.today()
  ##min_date_employees = []
  ##for row in reader: 
  ##  row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')
  return d


