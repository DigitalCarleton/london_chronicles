"""
***********************************
********INSTRUCTIONS TO RUN********
*
* On Mac and Linux computers:
*
* 1. Save the excel file as a csv file (Each chronicle should be its own excel file).
*
* 2. Save the csv file, the London Gazetteer json file, and this python file to your desktop
*
* 3. Open your terminal and navigate to your desktop (type: cd Desktop)
*
* 4. Confirm that the 3 files are there (Enter: ls) 
* (this command will list off all the files in your directory)
*
* 5. Enter: python3 python_file_name.py  
* (where python_file_name.py is the name of this file, be sure to include the .py file extension)
*
* 6. Follow the instructions in the terminal
***********************************
"""

import csv
import json
import re

print('\nIn order for this code to work the excel file must follow a few formatting rules: \n\n\
1) The first 6 columns should have data on the following: year, Mayoral Year, Regnal Year, Page number,\n\
Foolio in MS, Entry \n\n\
2) Every column for Non-London/Non-English places names must have the word "Non" somewhere in the header.\n\
capitalization matters\n\n\
3) Each London place name cell should have at most one place in it.\n\n\
4) For every london place name cell, the corresponding context cell should be the next cell to the right\n\n\
5) Each context column should have the word "Context" somewhere in the header (capitalization matters)\n\n\
6) The name of the csv file should be the name of the chronicle\n')

input('If all these conditions are met, press enter to continue. Otherwise, kill the program and make the necessary changes\n')

excel_file = input(
    'Enter the name of the csv file with place data (be sure to include the .csv extension)\nname: ')

json_file = input(
    '\nEnter the name of the json Gazetteer (be sure to include the .csv extension)\nname: ')

chronicle = excel_file.split('.')[0]

final_data = []
final_data.append(['Place Name', 'XML ID', 'London?', 'Chronicle',
                   'Year', 'Mayoral Year', 'Regnal Year', 'Context'])

new_file_name = chronicle + '-reformatted' + '.csv'

data = []
with open(excel_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)

print(len(data))
header_row = data[0]

f = open(json_file, encoding="utf8")
json_data = json.load(f)
f.close()

for row in data[1:]:
    for i in range(6, len(row) - 1):
        if row[i]:
            if 'Non' in header_row[i]:
                row_places = re.split(',|;', row[i])
                for place in row_places:
                    if place[0] == ' ':
                        place = place[1:]
                    final_data.append(
                        [place, None, 'N', chronicle, row[0], row[1], row[2], None])
            elif 'Context' not in header_row[i]:
                xml = 'Not Found'
                for feature in json_data['features']:
                    if feature['title'] == row[i]:
                        xml = feature['id']
                final_data.append(
                    [row[i], xml, 'Y', chronicle, row[0], row[1], row[2], row[i + 1]])


with open(new_file_name, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_data)


print('\nSuccess! You should see a new file on your desktop with \
the name {n}. \nSome of the XML tags may \
say "Not Found" These tags should be entered manually\n'.format(n=new_file_name))
