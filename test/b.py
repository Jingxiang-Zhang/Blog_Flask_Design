import requests

with open("html.txt") as file:
    for i,line in enumerate(file.readlines()):
        url=line.strip()
        image = requests.get(url)
        with open("pic/"+str(i)+".png","wb") as p:
            p.write(image.content)





