import enum
import re

def isLetter(x):
    if re.search('[a-zA-Z]',str(x)):
        return  True
    else:
        return False

def isDigit (x):
    if re.search('[0-9]',str(x)):
        return True
    else:
        return False

def reserved_word(token):
    rW = ['if','then','else','end','repeat','until','read','write']
    if token in rW:
        return True
    else:
        return False
def special_symbol(char):
    sS = ['+','-','*','/','=','<','(',')',';']
    if char in sS:
        return True
    else:
        return  False

def main():
    class state (enum.Enum):
        start = 0
        inComment = 1
        inNum = 2
        inId = 3
        inAssign = 4
        done = 5
    currentState = state.start

    while True:
            while True:
                try:
                    inputfileName = input("Input file path: ")
                    fhand = open(inputfileName)
                except FileNotFoundError:
                    print("File not found\n")
                    continue
                break

            outputFileName = input("Output file path:")
            outputFile = open(outputFileName, "+w")

            token = ""
            tokenType = ""
            for line in fhand:
                i=0
                if line[len(line)-1] != '\n':
                    line = line + '\n'
                while i < int(len(line)):
                    if currentState == state.start:
                        while line[i] == ' ' or line[i]=='\t':
                            i = i+1
                        if line[i] == '{':
                            currentState = state.inComment
                            i = i+1
                        elif isDigit(line[i]):
                            currentState= state.inNum
                        elif isLetter(line[i]):
                            currentState = state.inId
                        elif line[i] == ':':
                            currentState = state.inAssign
                        elif special_symbol(line[i]):
                            token = line[i]
                            i = i+1
                            tokenType = 'symbol'
                            currentState = state.done
                    elif currentState == state.inNum:
                        while isDigit(line[i]):
                            token = token+ line[i]
                            i=i+1
                        tokenType = 'Number'
                        currentState = state.done
                    elif currentState == state.inId:
                        while isLetter(line[i]) or isDigit(line[i]):
                            token = token+ line[i]
                            i = i+1
                        if reserved_word(token):
                            tokenType = 'reserved_word'
                        else:
                            tokenType = 'Identifier'
                        currentState = state.done
                    elif currentState == state.inAssign:
                        token = token+ line[i]
                        i = i+1
                        while line[i] !='=':
                            i = i+1
                        token = token+ line[i]
                        i= i+1
                        tokenType = 'Symbol'
                        currentState = state.done
                    elif currentState == state.inComment:
                        while line[i]!= '}':
                            token = token+line[i]
                            i = i+1
                            if line[i]=='\n':
                                break
                        if line[i]=='}':
                            i = i+1
                            tokenType = 'Comment'
                            currentState = state.done
                    elif currentState == state.done:
                        if token != "":
                            outputFile.write(token + ', ' + tokenType + '\n')
                            print(token +', ' +tokenType)
                        token = ""
                        tokenType = ""
                        currentState = state.start
                    if line[i] == '\n':
                        i = i+1
            if token != "":
                outputFile.write(token + ', ' + tokenType)
                print(token + ', ' + tokenType)
                exit = input('Want to exit Y/N?\n')
                if exit == 'y' or exit =='Y':
                    break
                else:
                    continue

if __name__ =='__main__':
    main()


