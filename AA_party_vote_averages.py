"""
  This Script counts the Total Votes received by Each Party during the 2012 US Presidential Election
"""

import os

file_name: str = os.path.join("output", "county average winning percentage data.csv")
file = open(file_name, "r")

lines: list[list[str]] = []
parties: list[str, int] = []

current_party: str = ""
achieved_votes: int = 0
total_votes: int = 0
national_total_votes: int = 0

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] == "Total Counties with 0 Votes:" or line[0] == "County Name": continue

    line[3] = line[3].upper()
    lines.append(line)
    national_total_votes += int(line[6])

print(national_total_votes)
# Sorts Data by County then by Party, so all data is in order
swap: bool = False

""" County Ordering removed as it's not required, and slows the Script further
for i in range(len(lines) - 1):
    swap = False

    for j in range(len(lines) - i - 1):
        if lines[j][0] > lines[j + 1][0]:
            swap = True

            lines[j], lines[j + 1] = lines[j + 1], lines[j]

    if not swap: break
# """

for i in range(len(lines) - 1):
    swap = False

    for j in range(len(lines) - i - 1):
        if lines[j][3] > lines[j + 1][3]:
            swap = True

            lines[j], lines[j + 1] = lines[j + 1], lines[j]

    if not swap: break

for line in lines:
    if current_party != line[3]:
        if current_party != "": parties.append([current_party, round(achieved_votes / total_votes * 100, 2), round(achieved_votes / national_total_votes * 100, 2), achieved_votes, total_votes, national_total_votes])

        current_party = line[3]
        achieved_votes = int(line[6])
        total_votes = int(line[7])
        continue
    
    achieved_votes += int(line[6])
    total_votes += int(line[7])
    print(f"{line[0]} - {line[6]} - {achieved_votes}")

file.close()

# print(parties)

write_string: str = "Party,Achievable %, National %,,Achieved Votes,Achievable Votes,National Vote Count"

for party in parties:
    write_string += f"\n{party[0]},{party[1]},{party[2]},,{party[3]},{party[4]},{party[5]}"

# print(write_string)

new_file_name: str = os.path.join("output", "party vote averages.csv")

file = open(new_file_name, "w")
file.write(write_string)
file.close()