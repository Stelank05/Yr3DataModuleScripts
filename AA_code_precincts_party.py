"""
  A Python Script that finds the Discrepancy in Total Precincts vs Reported Precincts,
    based on the Party
  Pairs with Candidate Script, done due to Parties having multiple Candidates,
    and Candidates running for multiple parties.
  Finds the Average Discrepancy, and the Maximum Discrepancy
  Outputs Results into a CSV File in 'output/party discrepancy data.csv'
"""

import os

# Create County Class for easier Data Storage
class County:
    def __init__(self, row: list[str]) -> None:
        self.party_name: str = row[9].upper()
        self.precinct_discrepancy: int = int(row[6]) - int(row[5])

# Load Counties from 'raw data.csv' into Program
file_name: str = os.path.join("data - raw", "raw data.csv")

counties: list[County] = []
parties: list[str] = []

file = open(file_name, "r")

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] != "County2012Id":
        counties.append(County(line))

        if counties[-1].party_name not in parties: parties.append(counties[-1].party_name)

file.close()
# print(parties)
# input()

# Get all 'Unequal Counties' - Counties where Precincts Reported is INEQUAL to Total Precincts
unequal_counties_count: int = 0
unequal_counties: list[County] = []

total_discrepancy: int = 0
max_discrepancy_total: int = 0

for county in counties:
    if county.precinct_discrepancy > 0:
        unequal_counties_count += 1
        unequal_counties.append(county)

        total_discrepancy += county.precinct_discrepancy

        if county.precinct_discrepancy > max_discrepancy_total: max_discrepancy_total = county.precinct_discrepancy

average_discrepancy_total: float = 0.0
if unequal_counties_count > 0: average_discrepancy_total = round(total_discrepancy / unequal_counties_count, 2)

# Display the Number
print(f"Number of Unequal Counties: {unequal_counties_count}")
print(f"Average Discrepancy in Total VS Reported Precints: {average_discrepancy_total}")
print(f"Maximum Discrepancy in Total VS Reported Precints: {max_discrepancy_total}")
input()

# Separate Counties by Party
current_county: int = 0

total_discrepancy_party: int = 0
min_discrepancy_party: int = 0
max_discrepancy_party: int = 0
total_counties: int = 0
total_counties_party: int = 0
average_discrepancy_party: float = 0.0

discrepancies: list[list[str, int, float]] = []

for current_party in parties:
    current_county = 0
    total_discrepancy_party = 0
    min_discrepancy_party = 0
    max_discrepancy_party = 0
    total_counties_party = 0

    while current_county < len(unequal_counties):
        if unequal_counties[current_county].party_name == current_party:
            if unequal_counties[current_county].precinct_discrepancy > 0:
                total_counties_party += 1
                total_counties += 1
                total_discrepancy_party += unequal_counties[current_county].precinct_discrepancy

                if unequal_counties[current_county].precinct_discrepancy < min_discrepancy_party:
                    min_discrepancy_party = unequal_counties[current_county].precinct_discrepancy
                elif min_discrepancy_party == 0:
                    min_discrepancy_party = unequal_counties[current_county].precinct_discrepancy
                
                if unequal_counties[current_county].precinct_discrepancy > max_discrepancy_party:
                    max_discrepancy_party = unequal_counties[current_county].precinct_discrepancy
        
            unequal_counties.remove(unequal_counties[current_county])
        else: current_county += 1
    
    if total_counties_party > 0: average_discrepancy_party = round(total_discrepancy_party / total_counties_party, 2)
    else: average_discrepancy_party = 0.0

    print(f"{current_party} Country Discrepancies:")
    print(f"  Counties with Discrepancies / Average Discrepancy: {total_counties_party} / {average_discrepancy_party}")
    print(f"  Maximum Discrepancy / Mininum Discrepancy: {max_discrepancy_party} / {min_discrepancy_party}")

    discrepancies.append([current_party, total_counties_party, average_discrepancy_party, max_discrepancy_party, min_discrepancy_party])

# print(f"Number of Unequal Counties: {total_counties}")

# Puts Total Discrepancy Data into a CSV File for Easy Storage / Later Referral
file_name_new: str = os.path.join("output", "discrepancy data.csv")
write_string: str = "Party Code,Total Unequal Counties,Average Discrepancy,Maximum Discrepancy,Minimum Discrepancy"

for discrepancy in discrepancies:
    write_string += f"\n{discrepancy[0]},{discrepancy[1]},{discrepancy[2]},{discrepancy[3]},{discrepancy[4]}"

file = open(file_name_new, "w")
file.write(write_string)
file.close()