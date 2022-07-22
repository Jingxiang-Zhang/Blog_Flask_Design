

with open("a.txt","rb") as file:
    line = str(file.readlines()[0])

    while True:
        a = line.find(" src=\"",)
        if a==-1:
            break
        line = line[a+6:]
        a = line.find("\"")
        print(line[0:a])

