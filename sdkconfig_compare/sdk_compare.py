def reformat_not_set(entry):
    entry_lst = list(entry[2:])
    entry_lst[-11] = '='
    return "".join(entry_lst)


def setLength(s, max_length):
    return (s + ' ' * max_length)[:max_length]


with open('sdk1.txt') as f:
    sdk1_lines = f.readlines()
    sdk1_lines = [line.strip() for line in sdk1_lines]
    sdk1_lines = [line for line in sdk1_lines if line]  # remove empty strings

with open('sdk2.txt') as f:
    sdk2_lines = f.readlines()
    sdk2_lines = [line.strip() for line in sdk2_lines]
    sdk2_lines = [line for line in sdk2_lines if line]  # remove empty strings

diff1 = list(set(sdk1_lines) - set(sdk2_lines))
diff2 = list(set(sdk2_lines) - set(sdk1_lines))

diff1_cleaned = []
diff2_cleaned = []

for line in diff1:
    if line[0] == '#':
        diff1_cleaned.append(reformat_not_set(line))
    else:
        diff1_cleaned.append(line)

for line in diff2:
    if line[0] == '#':
        diff2_cleaned.append(reformat_not_set(line))
    else:
        diff2_cleaned.append(line)

diff1_sorted = sorted(diff1_cleaned)
diff2_sorted = sorted(diff2_cleaned)

diff1_split = [line.split('=') for line in diff1_sorted]
diff2_split = [line.split('=') for line in diff2_sorted]

mutual = []
rest1 = []
rest2 = []
for line in diff1_split:
    if any(line[0] in sublist for sublist in diff2_split):
        mutual.append(line)
        # Find the mutual config in other file
        for entry in diff2_split:
            if entry[0] == line[0]:
                mutual.append(entry)
    else:
        rest1.append(line)

for line in diff2_split:
    if any(line[0] in sublist for sublist in diff1_split):
        pass
    else:
        rest2.append(line)

for line in rest1:
    mutual.append(line)
    mutual.append(['', ''])

for line in rest2:
    mutual.append(['', ''])
    mutual.append(line)

# print(mutual)

list1 = mutual[0::2]
list2 = mutual[1::2]


print("---------------------------------------------------------------------------------------------------------------")
print("                                         SDKCONFIG FILE DIFFERENCES:", len(diff1)+len(diff2))
print("---------------------------------------------------------------------------------------------------------------")
print("File1                                                           File2")
print("------                                                          ------")
for l1, l2 in zip(list1, list2):
    print(setLength(l1[0], 45), '=', setLength(l1[1], 10), "\t   ", setLength(l2[0], 45), '=', l2[1])
print("---------------------------------------------------------------------------------------------------------------")
