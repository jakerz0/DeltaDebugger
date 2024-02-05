import pprint
import sys
import subprocess
'''
    testing file should be a copy of the original (file1v1.java) with changes applied
'''
# def fileInput():
#     global file1, file2

#     if (len(sys.argv) != 3):
#         print("Invalid format, please try again with python3 Debugger.py file1 file2")
#         exit()
#     file1 = sys.argv[1]
#     file2 = sys.argv[2]
#     command = 'diff -u0 ' + file1 + ' ' + file2 + ' > changes.txt'
#     subprocess.call(command, shell=True)
def fileInput():
    global file1, file2
    paramList = []
    function = ''

    if (len(sys.argv) == 3):
        print("Ruinning generic test on division")
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    elif (len(sys.argv) > 3):
        print("Running user-given test")
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        function = sys.argv[3]
        i = 4
        while i < len(sys.argv):
            paramList.append(sys.argv[i])
            i += 1
    else:
        print("No files given, running on defaults with default test")
    command = 'diff -u0 ' + file1 + ' ' + file2 + ' > changes.txt'
    subprocess.call(command, shell=True)
    return function, paramList

def getChanges():
    lines = f.readlines()
    i = 0
    index = 0
    ranAlready = False
    for i in range(len(lines)):
        if (lines[i][0] == '@'):
            j = i
            lineToAdd = lines[i].replace('@', '')
            lineToAdd = lineToAdd.replace('\n', '')
            tempLine = lines[min(len(lines) - 1, j + 1)]
            tempList = []
            while (tempLine[0] != '@' and not ranAlready):
                tempLine = tempLine[2:]
                tempList.append(' '.join(tempLine.split()))
                j += 1
                tempLine = lines[min(len(lines) - 1, j + 1)]
                if (j >= len(lines)):
                    ranAlready = True
            first, second = lineToAdd.split(" ")[1:3]
            removing = getChangeInfo(first)
            adding = getChangeInfo(second)
            lineInfo = [removing, adding]
            changes[index] = (lineInfo, tempList)
            index += 1
            i += 1

def deltaDebug(config, remainApplied):
    global deltaDebugStepNum
    #running files where file3 is the file where the changes are applied

    size = len(config)
    half = int(size / 2)

    # c1 = [int(x+1) for x in range(half)]
    c1 = [config[i] for i in range(half)]
    # c2 = [x for x in range(half+1, size+1)]
    c2 = [config[i] for i in range(half, size)] 

    c1exe = loadBitvector(c1, remainApplied)
    createTestFile(c1exe)
    success1 = compileAndRun()
    deltaDebugStepNum += 1

    # new 11/1
    if not success1:
        ddPrint(exePrint(c1exe), 1)
    else:
        ddPrint(exePrint(c1exe), 0)

    # if not success1:
    #     ddPrint(exePrint(c1exe), 1)
    #     if(half == 1):
    #         return
    #     # dd only this half (c1) with no remains
    #     newRemainApplied = [0 for i in range(len(changes))] #no remains
    #     # deltaDebug(c1, newRemainApplied)
    # else:
    #     # do something... mark for reapply
    #     ddPrint(exePrint(c1exe), 0)
    #     if(half == 1):
    #         return
    #     # deltaDebug(c2, c1) # c1 remains, test with other side (c2)
        
    c2exe = loadBitvector(c2, remainApplied)
    createTestFile(c2exe)
    success2 = compileAndRun()
    deltaDebugStepNum += 1

    #new 11/1
    if not success2:
        ddPrint(exePrint(c2exe), 1)
    else:
        ddPrint(exePrint(c2exe), 0)

    # if not success2:
    #     ddPrint(exePrint(c2exe), 1)
    #     if(size-half == 1):
    #         return
    #     # dd only this half (c1) with no remains
    #     newRemainApplied = [0 for i in range(len(changes))] #no remains
    #     # deltaDebug(c2, newRemainApplied)
    # else:
    #     # do something... mark for reapply
    #     ddPrint(exePrint(c2exe), 0)
    #     if(size-half == 1):
    #         return
    #     # deltaDebug(c1, c2) # c1 remains, test with other side (c2)

    if success1 == success2:
        newRemainApplied1 = remainApplied.copy()
        j = 0
        i = 0
        while j < len(c2):
            if c2[j] == i+1:
                newRemainApplied1[i] = c2[j]
                j += 1
            i += 1
        if len(c1) > 1: deltaDebug(c1,newRemainApplied1)
        else: errors.append(c1[0])

        newRemainApplied2 = remainApplied.copy()
        j = 0
        i = 0
        while j < len(c1):
            if c1[j] == i+1:
                newRemainApplied2[i] = c1[j]
                j += 1
            i += 1
        if len(c2) > 1: deltaDebug(c2,newRemainApplied2)
        else: errors.append(c2[0])

    if success1 and not success2:
        newRemainApplied2 = remainApplied.copy()
        # j = 0
        # i = 0
        # while j < len(c1):
        #     if c1[j] == i+1:
        #         newRemainApplied2[i] = c1[j]
        #         j += 1
        #     i += 1
        if len(c2) > 1: deltaDebug(c2,newRemainApplied2)
        else: errors.append(c2[0])
    
    if success2 and not success1:
        newRemainApplied1 = remainApplied.copy()
        # j = 0
        # i = 0
        # while j < len(c2):
        #     if c2[j] == i+1:
        #         newRemainApplied1[i] = c2[j]
        #         j += 1
        #     i += 1
        if len(c1) > 1: deltaDebug(c1,newRemainApplied1)
        else: errors.append(c1[0])

def exePrint(exe):
    ret = []
    for i in range(len(exe)):
        if exe[i] == 1:
            ret.append(i+1)
    return ret
    
def ddPrint(config, status):
    global  deltaDebugStepNum
    ret = 'Step ' + str(deltaDebugStepNum) + ': ' + 'c_' + str(deltaDebugStepNum) + ': ' + str(config)
    if status == 0:
        ret += ' PASS'
    else:
        ret += ' FAIL'

    print(ret)

def loadBitvector(config: list, remainApplied: list):
    
    bitvector = []
    #fill bitvector with 0s so it has indexes later
    for i in range(len(changes)):
        bitvector.append(0)

    j = 1
    i = 0
    while i < len(config):
        if config[i] == j:
            bitvector[j-1] = 1
            i += 1
        # if remainApplied[i] == j:
        #     bitvector[j-1] = 1
        #     i += 1
        j += 1

    i = 0
    j = 1
    while i < len(remainApplied):
        if remainApplied[i] == i+1:
            bitvector[i] = 1

        i += 1
    
    
    return bitvector

def createTestFile(bitvector: list):
    global changes
    file1_obj = open(file1)
    file2_obj = open(file2)

    file3_obj = open(file3, "r+")
    file3_obj.truncate(0) # remove all text in file
    # file3_obj.close()
    # file3_obj = open(file3, "a") # append mode

    lines1 = file1_obj.readlines()
    lines2 = file2_obj.readlines()

    # file3_obj.write("public class file1_test {\n")
    changeIter = 0
    skipNext = False
    j = 0
    for i in range(len(lines1)):
        if (j < len(changes) and changes[j][0][0][0] == i + 1):
            attemptedChange = True
            k = 0
            if (bitvector[j] == 1):
                if (changes[j][0][1][1] > 0):
                    if (changes[j][0][0][1] == 0):
                        file3_obj.write(lines1[i])
                    while (k < changes[j][0][1][1]):
                        file3_obj.write(changes[j][1][changes[j][0][0][1] + k] + '\n')
                        k += 1
                if (changes[j][0][1][1] == 0 and changes[j][0][0][1] > 1):
                    skipNext = True
            else:
                file3_obj.write(lines1[i] + '\n')
            if attemptedChange:
                j += 1
                attemptedChange = False
            
        else:
            if (not skipNext):
                file3_obj.write(lines1[i] +'\n')
            skipNext = False

        # for j in range(len(changes)):
        #     if changes[j][0][0][0] == i - 1:

    # bookkeeping
    file1_obj.close()
    file2_obj.close()
    file3_obj.close()
    
def getChangeInfo(cmd: str):
    spot_tmp = ''
    space_tmp = ''
    spacing = False
    for i in range(len(cmd)):
        if cmd[i].isdigit() and not spacing:
            spot_tmp += cmd[i]
        elif cmd[i].isdigit() and spacing:
            space_tmp += cmd[i]
        elif cmd[i] == ',':
            spacing = True
        
    if space_tmp == '':
        space_tmp = '1'
    ret = int(spot_tmp)

    return abs(ret), int(space_tmp)

# def compileAndRun():
#     command = 'javac ' + file3
#     subprocess.call(command, shell=True)
#     #just testing summation
#     command = [ 'java', file3[:-5], '5', '0', 'division' ]

#     # JUST TEST THE DIVIDE BY 0 DEFAULT FROM PDF WOOOOO!!!!!

#     #output = subprocess.run(command, shell=True, capture_output=True)
#     output = subprocess.call(command, shell=True, 
#                              stdout=subprocess.DEVNULL,
#                              stderr=subprocess.DEVNULL) # output = returncode
#     # print(output)
#     return (output == 0)  # no error if returncode output is 0
def compileAndRun():
    command = 'javac ' + file3
    subprocess.call(command, shell=True)
    #just testing summation
    if (len(paramsList) > 0):
        command = [ 'java ' + file3[:-5] + ' ']
        for i in paramsList:
            command[0] += i + ' '
        command[0] += func
    else:
        command = [ 'java ' + file3[:-5] + ' 5 ' + '0 ' + 'division' ]

    # JUST TEST THE DIVIDE BY 0 DEFAULT FROM PDF WOOOOO!!!!!

    #output = subprocess.run(command, shell=True, capture_output=True)
    output = subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL) # output = returncode
    # print(output)
    return (output == 0)  # no error if returncode output is 0
    



file1 = 'files/file1v1.java'
file2 = 'files/file1v2.java'
file3 = 'file1v1.java'
#gets system in and makes changes.txt
deltaDebugStepNum = 0

func = ''
paramsList = []
#gets system in and makes changes.txt
deltaDebugStepNum = 0
func, paramsList = fileInput()

f = open("changes.txt", "r")
changes = {}
errors = []
#stores changes in changes{}
getChanges()
for key, value in changes.items():
    print('-' + str(value[0][0]) + ' +' + str(value[0][1]))
print("# of total change sets = ", len(changes))    
#attempts to locate bug(s) and tests java files
#set no remainapps
initRemainApplied = [0 for i in range(len(changes))]
initConfig = [i+1 for i in range(len(changes))]
deltaDebug(initConfig, initRemainApplied)

#pprint.pprint(changes)


print('Changes where bugs occurred: ' + str(errors))

f.close()