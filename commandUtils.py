from interfaceUtils import runCommand, requestBuildArea

def makeBuildArea(width = 128, height = 128):
    runCommand("execute at @p run setbuildarea ~{} 0 ~{} ~{} 255 ~{}".format(int(-1*width/2), int(-1*height/2), int(width/2), int(height/2)))
    buildArea = requestBuildArea()
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    return (x1, z1, x2 - x1, z2 - z1)

def setSignText(x, y, z, line1 = "", line2 = "", line3 = "", line4 = ""):
    l1 = 'Text1:\'{"text":"'+line1+'"}\''
    l2 = 'Text2:\'{"text":"'+line2+'"}\''
    l3 = 'Text3:\'{"text":"'+line3+'"}\''
    l4 = 'Text4:\'{"text":"'+line4+'"}\''
    blockNBT = "{"+l1+","+l2+","+l3+","+l4+"}"
    return(runCommand("data merge block {} {} {} ".format(x, y, z) + blockNBT))

def addItemChest(x, y, z, items):
    for id,v in enumerate(items):
        command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                               "container."+str(id),
                                                               v[0],
                                                               v[1])
        runCommand(command)

def makeBookItem(text, title = "", author = "", desc = ""):
    booktext = "pages:["
    while len(text) > 0:
        page = text[:15*23]
        text = text[15*23:]
        bookpage = "'{\"text\":\""
        while len(page) > 0:
            line = page[:23]
            page = page[23:]
            bookpage += line+"\\\\n"
        bookpage += "\"}',"
        booktext += bookpage

    booktext = booktext + "],"

    booktitle = "title:\""+title+"\","
    bookauthor = "author:\""+author+"\","
    bookdesc = "display:{Lore:[\""+desc+"\"]}"

    return "written_book{"+booktext+booktitle+bookauthor+bookdesc+"}"
