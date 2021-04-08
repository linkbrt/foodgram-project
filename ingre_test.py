from csv import reader
from os import read


with open('ingredients.csv', 'r') as file:
    csv_reader = reader(file)
    unique_lines = []
    for row, line in csv_reader:
        # print(row, line)
        if line not in unique_lines:
            unique_lines.append(line)
    print(unique_lines)
