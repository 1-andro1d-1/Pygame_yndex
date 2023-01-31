with open("info.txt") as file:
    data = file.readlines()
    data[0] = '2'+"\n"
    print(data[0])
with open("info.txt", 'wt') as file:
    for i in data:
        file.write(''.join(i))
