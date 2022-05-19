


with open('sdk1.txt') as f:
    sdk1_lines = f.readlines()
    sdk1_lines = [line.strip() for line in sdk1_lines]
    sdk1_lines = [line for line in sdk1_lines if line]
    # sdk1_lines = [line for line in sdk1_lines if line[0] != '#']

with open('sdk2.txt') as f:
    sdk2_lines = f.readlines()
    sdk2_lines = [line.strip() for line in sdk2_lines]
    sdk2_lines = [line for line in sdk2_lines if line]
    # sdk2_lines = [line for line in sdk2_lines if line[0] != '#']

# print(len(sdk1_lines), sdk1_lines)
# print(len(sdk2_lines), sdk2_lines)

diff1 = list(set(sdk2_lines) - set(sdk1_lines))
diff2 = list(set(sdk1_lines) - set(sdk2_lines))

diff1_cleaned = []
diff2_cleaned = []

for line in diff1:
    if line[0] == '#':
        diff1_cleaned.append(line[2:])
    else:
        diff1_cleaned.append(line)

for line in diff2:
    if line[0] == '#':
        diff2_cleaned.append(line[2:])
    else:
        diff2_cleaned.append(line)



table_data = [
    diff1,
    diff2
]

print("-------------------------------------------------")
print("    SDKCONFIG FILE DIFFERENCES:", len(diff1)+len(diff2))
print("-------------------------------------------------")
# col_width = max(len(word) for row in table_data for word in row) + 2  # padding
# for row in table_data:
#     print("".join(word.ljust(col_width) for word in row))
#

print("not in sdk2")
print("----------------------------")
for line in sorted(diff1_cleaned):
    print(line)
print("----------------------------")
print("not in sdk1")
print("----------------------------")

for line in sorted(diff2_cleaned):
    print(line)
print("-------------------------------------------------")

