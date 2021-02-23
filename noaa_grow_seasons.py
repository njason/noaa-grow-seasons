import argparse
import csv
from datetime import datetime

parser = argparse.ArgumentParser('NOAA Grow Season Calculator')
parser.add_argument('input_file', type=str, help='Input CSV file from NOAA report, see README for details on obtaining report CSV file.')

args = parser.parse_args()

station = None
name = None
years = {}
incomplete_years = {}

# parse input file
with open(args.input_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not station:
            station = row['STATION']
        if not name:
            name = row['NAME']

        date = datetime.strptime(row['DATE'], '%Y-%m-%d')

        if row['TMIN'] == '':
            incomplete_years[date.year] = None
        
        if date.year not in years:
            years[date.year] = []
        
        years[date.year].append(row['TMIN'])

# output grow season length
for year, days in years.items():
    if year in incomplete_years:
        continue

    last_spring_frost = None
    first_fall_frost = None

    for i, day_min_temp in enumerate(days):
        # the 200th day of the year is in the middle of July, hottest time of the year anywhere is the continental USA
        if i < 200 and int(day_min_temp) < 33:
            last_spring_frost = i
        elif i >= 200 and int(day_min_temp) < 33:
            first_fall_frost = i
    
    print(str(year) + ' ' + str(first_fall_frost - last_spring_frost))
