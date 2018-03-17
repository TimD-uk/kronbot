import time
import sys

import util

def getTime(color):
    if color == True:            
        return '[' + util.colors.FAIL + time.strftime('%H:%M:%S') + util.colors.ENDC + '] '
    else:
        return '['  + time.strftime('%H:%M:%S') + '] '

def go(text, toFile, toConsole):
    if toFile == True:        
        myFile = open("logs/latest.log", "a+")
        addedText = text.replace(util.colors.HEADER, "")
        addedText = addedText.replace(util.colors.OKBLUE, "")
        addedText = addedText.replace(util.colors.OKGREEN, "")
        addedText = addedText.replace(util.colors.WARNING, "")
        addedText = addedText.replace(util.colors.FAIL, "")
        addedText = addedText.replace(util.colors.ENDC, "")
        addedText = addedText.replace(util.colors.BOLD, "")
        addedText = addedText.replace(util.colors.UNDERLINE, "")
        addedText = getTime(False) + addedText + "\n"
        myFile.write(addedText)
        myFile.close()
        
        if toConsole == True:
            print(getTime(True) + text)
    elif toFile == False:
        print(getTime(True) + text)        
    