from FourRooms import FourRooms
import numpy as np
import copy
import sys

e = 0.8
lr = 1
discount = 0.5

stoFlag = False

qTable = {} 
rTable = {}

qTableRED = {} 
rTableRED = {}
qTableGREEN = {} 
rTableGREEN = {}
qTableBLUE = {} 
rTableBLUE = {}
mode = 1

aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

def explorationFunction(currentPosition):
    global e
    #starts off very exploratative and gradualy becomes less
    if(np.random.random()<e):
        action = np.random.randint(0,4)
        while(isLegalPosition(currentPosition, action)==False):
            action = np.random.randint(0,4)
    else:
        action = maxNext(currentPosition, False)
        while(isLegalPosition(currentPosition, action)==False):
            action = maxNext(currentPosition, False)
    return action

def maxNext(currentPosition, update):
    if(mode == 1):
        actions = [
                    qTableRED[currentPosition][0]
                    ,qTableRED[currentPosition][1]
                    ,qTableRED[currentPosition][2]
                    ,qTableRED[currentPosition][3]
                ]
    if(mode == 2):
        actions = [
                    qTableGREEN[currentPosition][0]
                    ,qTableGREEN[currentPosition][1]
                    ,qTableGREEN[currentPosition][2]
                    ,qTableGREEN[currentPosition][3]
                ]
    if(mode == 3):
        actions = [
                    qTableBLUE[currentPosition][0]
                    ,qTableBLUE[currentPosition][1]
                    ,qTableBLUE[currentPosition][2]
                    ,qTableBLUE[currentPosition][3]
                ]            
        
    maxQValue = max(actions)
    if(update==True):
        return maxQValue
    maxIndex = np.random.choice([i for i in range(len(actions)) if actions[i] == maxQValue])
    return maxIndex



def tableUpdate(oldPos,action,newPos):
    global qTableRED
    global qTableGREEN
    global qTableBLUE
    if(mode == 1):
        qTableRED[oldPos][action] += lr *((rTableRED[oldPos][action] + discount*maxNext(newPos, True)) -  qTableRED[oldPos][action])
    if(mode == 2):
        qTableGREEN[oldPos][action] += lr *((rTableGREEN[oldPos][action] + discount*maxNext(newPos, True)) -  qTableGREEN[oldPos][action])
    if(mode == 3):
        qTableBLUE[oldPos][action] += lr *((rTableBLUE[oldPos][action] + discount*maxNext(newPos, True)) -  qTableBLUE[oldPos][action])

def isLegalPosition(currentPosition,action):
    if(mode == 1):
        if(rTableRED[currentPosition][action]==-1):
            return False
        return True
    if(mode == 2):
        if(rTableGREEN[currentPosition][action]==-1):
            return False
        return True
    if(mode == 3):
        if(rTableBLUE[currentPosition][action]==-1):
            return False
        return True
    


def printOut(package):
    if(package==1):
        table = rTableRED
    if(package==2):
        table = rTableGREEN
    if(package==3):
        table = rTableBLUE
    for i in range(13):
        for j in range(13):
            name = (i,j)
            first = table[name][0]
            second = table[name][1]
            third = table[name][2]
            fourth = table[name][3]
            print(name, first, second, third, fourth)
            



def main():
    global stoFlag
    if(len(sys.argv)>1):
        if(sys.argv[1].lower()=="-stochastic"):
            stoFlag = True

    global qTable
    global rTable
    global qTableRED
    global qTableGREEN
    global qTableBLUE
    global rTableRED
    global rTableGREEN
    global rTableBLUE
    global mode

    global e
    
    for iteration in range(1):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('rgb',stoFlag)
        for i in range(13):
            for j in range(13):
                qTable[(i,j)] = {}
                rTable[(i,j)] = {}
                for k in range(4):
                    qTable[(i,j)][k] = 0
                    rTable[(i,j)][k] = 0
        for i in range (13):
            for j in range(13):
                if(i == 0 or i == 12 or j == 0 or j == 12 or i == 6):
                    for k in range(4):
                        rTable[(i,j)][k] = -1
        hrznHall = [(6,3),(6,10)]
        for i in hrznHall:
            rTable[i][0] = -1
            rTable[i][1] = -1
            rTable[i][2] = 0
            rTable[i][3] = 0
        vertHall = [(2,6),(9,7)]
        for i in vertHall:
            rTable[i][0] = 0
            rTable[i][1] = 0
            rTable[i][2] = -1
            rTable[i][3] = -1
        wallList = [(1,6),(3,6),(4,6),(5,6),(7,7),(8,7),(10,7),(11,7)]
        for i in wallList:
            for a in range(4):
                rTable[i][j] = -1
        rTableRED = copy.deepcopy(rTable)
        rTableGREEN = copy.deepcopy(rTable)
        rTableBLUE = copy.deepcopy(rTable)
        qTableRED = copy.deepcopy(qTable)
        qTableGREEN = copy.deepcopy(qTable)
        qTableBLUE = copy.deepcopy(qTable)


        # printOut()
        for epoch in range(20):

            # Starting Position
            currentPosition = fourRoomsObj.getPosition()
            print('Agent starts at: {0}'.format(currentPosition))   

            # Repeat until in a terminal state
            isTerminal=fourRoomsObj.isTerminal()
            # qTable = qTableRED
            # rTable = rTableRED
            mode = 1
            while(isTerminal==False):
                nextAction = explorationFunction(currentPosition)
                gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(nextAction)

                print(packagesRemaining)
                # if(packagesRemaining==3): #update red package tables
                #     rTableRED = rTable
                #     qTableRED = qTable

                # if(packagesRemaining==2): # save red information then switch tables to green
                #     rTableRED = rTable
                #     rTable = rTableGREEN
                    
                #     qTableRED = qTable
                #     qTable = qTableGREEN

                # if(packagesRemaining==3): # save green information then switch tables to blue
                #     rTableRED = rTable
                #     rTable = rTableBLUE
                    
                #     qTableRED = qTable
                #     qTable = qTableBLUE

                # if(packagesRemaining==0): # save blue
                #     rTableBLUE = rTable
                #     qTableBLUE = qTable


                if(gridType==1): # if found red package, update reds table and prevent blue and green from going to that cell
                    # qTableRED = qTable
                    
                    rTableRED[currentPosition][nextAction] = 100
                    rTableGREEN[currentPosition][nextAction] = -1
                    rTableBLUE[currentPosition][nextAction] = -1
                    tableUpdate(currentPosition,nextAction,newPos)
                    mode = 2

                    # tableUpdate(currentPosition,nextAction,newPos)

                    # rTable = rTableGREEN
                    # qTable = qTableGREEN

                if(gridType==2): # if found green package, update greens table and prevent blue and red from going to that cell
                    # qTableGREEN = qTable
                    
                    rTableRED[currentPosition][nextAction] = -1
                    rTableGREEN[currentPosition][nextAction] = 100
                    rTableBLUE[currentPosition][nextAction] = -1
                    tableUpdate(currentPosition,nextAction,newPos)
                    mode = 3
                    # tableUpdate(currentPosition,nextAction,newPos)

                    # rTable = rTableBLUE
                    # qTable = qTableBLUE
                    
                if(gridType==3): # if found blue package, update blues table and prevent red and green from going to that cell
                    # qTableBLUE = qTable
                    
                    rTableRED[currentPosition][nextAction] = -1
                    rTableGREEN[currentPosition][nextAction] = -1
                    rTableBLUE[currentPosition][nextAction] = 100
                    tableUpdate(currentPosition,nextAction,newPos)

                    # mode = 3

                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                currentPosition = newPos
            printOut(1)
            printOut(2)
            printOut(3)
            fourRoomsObj.showPath(-1,"./data/Scenario3/Scenario3_iter_{0}_epoch_{1}.png".format(iteration,epoch))
            fourRoomsObj.newEpoch()
            if(e>0):
                e-=0.05
            

if __name__ == "__main__":
    main()
