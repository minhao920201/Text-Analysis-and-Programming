import csv
table = [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]
with open('test.csv', 'wt', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(table)

import csv
with open('test.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        print(row)