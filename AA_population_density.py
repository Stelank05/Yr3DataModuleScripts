"""
Python Script to calculate avg Population Density of Counties won by the 2 Major Parties during the 2012 US Presidential Election
"""

data: list[type] = []

import os
import pandas as pd

file_name: str = os.path.join("data - raw", "raw data.csv")
file = open(file_name, "r")

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] == "County2012Id": continue
    if line[9].lower() == "dem" or line[9].lower() == "gop":
        # print(line)
        data.append([line[1], line[2], int(line[7]), line[9].upper(), int(line[12])])

file.close()

swap: bool

for i in range (len(data) - 1):
    swap = False

    for j in range(len(data) - i - 1):
        if data[j][-1] < data[j + 1][-1]:
            swap = True
            data[j], data[j + 1] = data[j + 1], data[j]

    if not swap: break

for i in range (len(data) - 1):
    swap = False

    for j in range(len(data) - i - 1):
        if f"{data[j][0]} - {data[j][1]}" > f"{data[j + 1][0]} - {data[j + 1][1]}":
            swap = True
            data[j], data[j + 1] = data[j + 1], data[j]

    if not swap: break

print(data)
print(len(data))
# print(len(data) / 2)
# input()

parties: dict = {}

counter: int = 0

while counter < len(data):
    print(f"{counter}: {data[counter][0]} {data[counter][1]} / {data[counter + 1][0]} {data[counter + 1][1]}")

    if f"{data[counter][0]} {data[counter][1]}" != f"{data[counter + 1][0]} {data[counter + 1][1]}": break
    else:
        print(data[counter])
        if data[counter][3] not in list(parties.keys()):
            parties[data[counter][3]] = [[data[counter][2]], data[counter][2]]
        else:
            parties[data[counter][3]][0].append(data[counter][2])
            parties[data[counter][3]][1] += data[counter][2]
    
    counter += 2

# print(parties)
print(list(parties))
for party in list(parties):
    print(party, parties[party][1], f"Avg Pop: {parties[party][1] / len(parties[party][0])}")

write_string: str = "Party,Counties Won,Total Pop,Avg Pop"

for party in list(parties):
    write_string += f"\n{party},{len(parties[party][0])},{parties[party][1]},{round(parties[party][1] / len(parties[party][0]), 2)}"

print(write_string)

new_file_name: str = os.path.join("output", "population density data.csv")

file = open(new_file_name, "w")
file.write(write_string)
file.close()