import re

def removeSrc(text):
    startIndex = text.find("<img")
    curIndex = startIndex
    text = [char for char in text]
    while text[curIndex] != ">":
        text[curIndex] = ""
        curIndex += 1
    text[curIndex] = ""

    return "".join(text)





f = open("data.txt", "r")
x=f.read()



questions = x.replace("<p>","").replace("</p>","").replace("&nbsp;"," ").strip("[").strip("]").strip('"').strip('"')


while "<img" in questions:
    questions = removeSrc(questions)
questions = str(questions)
Index = questions.find("\\n")
print(Index)
questions = questions.replace("\\n","").split('","')

print(len(questions))

for i in range(len(questions)):
    pass
