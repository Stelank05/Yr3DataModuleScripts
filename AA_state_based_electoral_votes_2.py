import os
from AA_state_vote_counts import *

# county_name: str

data: list[list] = []
# counties: list[list] = [] # All The Counties
# county_names: list[str] = []

parties: dict = {}

file_name: str = os.path.join("data - raw", "raw data.csv")
file = open(file_name, "r")

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] == "County2012Id": continue
    if line[9].lower() == "dem" or line[9].lower() == "gop":
        data.append([line[1], line[2], line[9].upper(), int(line[12])])

file.close()

# print(data)

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

# print(data, len(data))
# input()

counter: int = 1

while counter < len(data):
    data.pop(counter)
    counter += 1

# print(data, len(data))

states: dict = {}

for item in list(data):
    if item[0] not in list(states): states[item[0]] = {}
    if item[2] not in states[item[0]]: states[item[0]][item[2]] = 1
    elif item[2] in states[item[0]]: states[item[0]][item[2]] += 1

# print(states)

parties: dict = {
    "DEM": [0, 0, 0], # Counties Won, States Won, EC Votes
    "GOP": [0, 0, 0]  # Counties Won, States Won, EC Votes
}

for state in list(states):
    if "DEM" not in states[state]: states[state]["DEM"] = 0
    if "GOP" not in states[state]: states[state]["GOP"] = 0

    states[state] = sorted(states[state].items(), key = lambda items: (items[1], items[0]), reverse = True)
    # print(state, states[state])

    for party in states[state]:
        # print(party[0], party[1])
        parties[party[0]][0] += party[1]

        if party[1] == states[state][0][1]:
            parties[party[0]][1] += 1
            parties[party[0]][2] += state_votes[state]

print(parties)

file_name_new_a: str = os.path.join("output", "state based electoral votes a states.csv") # States Dict
file_name_new_b: str = os.path.join("output", "state based electoral votes b parties.csv") # Parties Dict

write_string_a: str = "State,DEM,GOP"
write_string_b: str = "Party,Counties Won,States Won,EC Votes"

for state in list(states):
    write_string_a += f"\n{state},{states[state][0][1] if states[state][0][0] == "DEM" else states[state][1][1]},{states[state][1][1] if states[state][1][0] == "GOP" else states[state][0][1]}"

for party in list(parties):
    write_string_b += f"\n{party},{parties[party][0]},{parties[party][1]},{parties[party][2]}"

file_a = open(file_name_new_a, "w"); file_a.write(write_string_a); file_a.close()
file_b = open(file_name_new_b, "w"); file_b.write(write_string_b); file_b.close()