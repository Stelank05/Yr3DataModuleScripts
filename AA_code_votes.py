import os

# Load Data from File
file_name: str = os.path.join("data - raw", "raw data.csv")
file = open(file_name, "r")

write_string: str = "" # "County Name,Candidate Surname,Candidate Firstname,Party,Vote Percentage,,Achieved Votes,Total Votes"
zero_count: int = 0

for line in file:
    line = line.replace("\n", "").replace("ï»¿", "").split(",")

    if line[0] == "County2012Id": continue
    if int(line[7]) == 0:
        zero_count += 1
        
    write_string += f"\n{line[1]} - {line[2]},{line[11]},{line[10]},{line[9]},{round((int(line[12]) / int(line[7])) * 100, 2)},,{line[12]},{line[7]}"

file.close()

write_string = f"Total Counties with 0 Votes:,{zero_count}\nCounty Name,Candidate Surname,Candidate Firstname,Party,Vote Percentage,,Achieved Votes,Total Votes{write_string}"

file_name_new: str = os.path.join("output", "county average winning percentage data.csv")

file = open(file_name_new, "w")
file.write(write_string)
file.close()