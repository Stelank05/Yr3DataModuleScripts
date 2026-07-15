"""
  Calculates what party won what state, and then uses that,
    in conjunction with 2012 US Electoral College Vote Amounts,
    to calculate the winner of the election
"""

import os
from AA_state_vote_counts import *

"""
total: int = 0

for state in state_votes: total += state_votes[state]

print(total)
# """

states: dict = {}


# Load Data
file_name: str = os.path.join("data - raw", "raw data.csv")
file = open(file_name, "r")

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] == "County2012Id": continue

    if line[1] not in list(states.keys()): states[line[1]] = {}

    if line[9].upper() not in list(states[line[1]].keys()): states[line[1]][line[9].upper()] = int(line[12])
    else: states[line[1]][line[9].upper()] += int(line[12])

states = dict(sorted(states.items(), key = lambda item: item[0]))

parties: dict = {}

write_string: str = "State,Votes"

for state in list(states.keys()):
    votes = sorted(states[state].items(), key = lambda items: (items[1], items[0]), reverse = True)
#     print(state, len(votes), votes)
#     print(states[state].keys())

    write_string += f"\n{state}"

    for i in range(len(votes)):
        if votes[i][1] >= 5000: write_string += f",{votes[i][0]}: {votes[i][1]}"

#     print(write_string)
 
    # print(votes[0][0], votes[0][1], state_votes[state])

    if votes[0][0] not in list(parties.keys()): parties[votes[0][0]] = [state_votes[state], 1, [state]]
    else:
        parties[votes[0][0]][0] += state_votes[state]
        parties[votes[0][0]][1] += 1
        parties[votes[0][0]][2].append(state)

# print(parties)

parties = sorted(parties.items(), key = lambda items: (items[1], items[0]), reverse = True)

write_string += "\n\nParty,EC Votes,States Won,States"
print()

for i in range(len(parties)):
    print(f"{parties[i][0]}: {parties[i][1][0]} / {parties[i][1][1]} States Carried - {parties[i][1][2]}")

    write_string += f"\n{parties[i][0]},{parties[i][1][0]},{parties[i][1][1]}"

    for state in parties[i][1][2]:
        write_string += f",{state}"

new_file_name: str = os.path.join("output", "state win data.csv")

file = open(new_file_name, "w")
file.write(write_string)
file.close()