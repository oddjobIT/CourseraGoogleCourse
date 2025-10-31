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

def get_same_or_newer(start_date):
  """Returns the employees that started on the given date, or the closest one."""
  data = get_file_lines(FILE_URL)
  ##reader = csv.reader(data[1:])
  d={}
  [d.setdefault( datetime.datetime.strptime(row['Start Date'], '%Y-%m-%d'), []).append(row['Name']+' '+ row['Surname']) for row in csv.DictReader(data)]
  employeeStartDateDict = dict(sorted(d.items(),reverse=True))
  # We want all employees that started at the same date or the closest newer
  # date. To calculate that, we go through all the data and find the
  # employees that started on the smallest date that's equal or bigger than
  # the given start date.
  #min_date = datetime.datetime.today()
  min_date_employees = {}
  for key in employeeStartDateDict: 
    print(key)
    if key >= start_date:
      min_date_employees[key] = employeeStartDateDict[key]
    # If this date is smaller than the one we're looking for,
    # we skip this row
    if key < start_date:
      break
  return min_date_employees

def list_newer(start_date):
  foundMatches = get_same_or_newer(start_date)
  for key in foundMatches:
    print(f"Started on {key.strftime("%b %d, %Y")}: {foundMatches[key]}")
    #print("Started on {}: {}".format(start_date.strftime("%b %d, %Y"), employees))

    # Now move the date to the next one
    #start_date = start_date + datetime.timedelta(days=1)

def main():
  start_date = get_start_date()
  list_newer(start_date)

if __name__ == "__main__":
  main()