input_file = "companies.txt"
output_file = "debug"

unique_lines = []
unique_lines_lowercase = []

with open(input_file, 'r') as file:
    for line in file:
        line_lowercase = line.lower().strip()
        if line_lowercase not in unique_lines_lowercase:
            if len(line_lowercase.split(" ")) > 1:
                for word in line_lowercase.split(" "):
                    if word in unique_lines:
                        print(f"{word} of {line} was a duplicate risk")
                else:
                    unique_lines.append(line)
                    unique_lines_lowercase.append(line_lowercase)
            else:
                unique_lines.append(line)
                unique_lines_lowercase.append(line_lowercase)
        else:
            print(f"{line} was a duplicate")

unique_lines.sort()

with open(output_file, 'w') as file:
    for line in unique_lines:
        file.write(line)