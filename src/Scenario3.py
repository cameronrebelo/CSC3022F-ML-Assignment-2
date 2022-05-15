import sys
from FourRooms import FourRooms
import numpy as np

e = 0.8
lr = 1
discount = 0.5

qTable = {} 
rTable = {}

qTableRED = {} 
rTableRED = {}
qTableGREEN = {} 
rTableGREEN = {}
qTableBLUE = {} 
rTableBLUE = {}
stoFlag = False
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
    qTableRED[oldPos][action] += lr *((rTableRED[oldPos][action] + discount*maxNext(newPos, True)) -  qTableRED[oldPos][action])
    qTableGREEN[oldPos][action] += lr *((rTableGREEN[oldPos][action] + discount*maxNext(newPos, True)) -  qTableGREEN[oldPos][action])
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
          

def main():
    global stoFlag

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
    # CLI
    if(len(sys.argv)>1):
        if(sys.argv[1].lower()=="-stochastic"):
            stoFlag = True
    
    for iteration in range(10):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('rgb',stoFlag)

        # Init Q and Rewards tables using environment details
        for i in range(13):
            for j in range(13):
                qTableRED[(i,j)] = {}
                rTableRED[(i,j)] = {}
                qTableGREEN[(i,j)] = {}
                rTableGREEN[(i,j)] = {}
                qTableBLUE[(i,j)] = {}
                rTableBLUE[(i,j)] = {}
                for k in range(4):
                    qTableRED[(i,j)][k] = 0
                    rTableRED[(i,j)][k] = 0
                    qTableGREEN[(i,j)][k] = 0
                    rTableGREEN[(i,j)][k] = 0
                    qTableBLUE[(i,j)][k] = 0
                    rTableBLUE[(i,j)][k] = 0
        for i in range (13):
            for j in range(13):
                if(i == 0 or i == 12 or j == 0 or j == 12 or i == 6):
                    for k in range(4):
                        rTableRED[(i,j)][k] = -1
                        rTableGREEN[(i,j)][k] = -1
                        rTableBLUE[(i,j)][k] = -1
        hrznHall = [(6,3),(6,10)]
        for i in hrznHall:
            rTableRED[i][0] = -1
            rTableRED[i][1] = -1
            rTableRED[i][2] = 0
            rTableRED[i][3] = 0
            rTableGREEN[i][0] = -1
            rTableGREEN[i][1] = -1
            rTableGREEN[i][2] = 0
            rTableGREEN[i][3] = 0
            rTableBLUE[i][0] = -1
            rTableBLUE[i][1] = -1
            rTableBLUE[i][2] = 0
            rTableBLUE[i][3] = 0
        vertHall = [(2,6),(9,7)]
        for i in vertHall:
            rTableRED[i][0] = 0
            rTableRED[i][1] = 0
            rTableRED[i][2] = -1
            rTableRED[i][3] = -1
            rTableGREEN[i][0] = 0
            rTableGREEN[i][1] = 0
            rTableGREEN[i][2] = -1
            rTableGREEN[i][3] = -1
            rTableBLUE[i][0] = 0
            rTableBLUE[i][1] = 0
            rTableBLUE[i][2] = -1
            rTableBLUE[i][3] = -1
        wallList = [(1,6),(3,6),(4,6),(5,6),(7,7),(8,7),(10,7),(11,7)]
        for i in wallList:
            for a in range(4):
                rTableRED[i][j] = -1
                rTableGREEN[i][j] = -1
                rTableBLUE[i][j] = -1


        for epoch in range(20):

            # Starting Position
            currentPosition = fourRoomsObj.getPosition()
            print('Agent starts at: {0}'.format(currentPosition))   

            # Repeat until in a terminal state
            isTerminal=fourRoomsObj.isTerminal()
            while(isTerminal==False):
                nextAction = explorationFunction(currentPosition)
                gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(nextAction)

                # if found red package
                if(gridType==1):
                    rTableRED[currentPosition][nextAction] = 100
                    rTableGREEN[currentPosition][nextAction] = -100
                    rTableBLUE[currentPosition][nextAction] = -100
                    mode=2
                # if found green package
                if(gridType==2):
                    if(packagesRemaining!=1):
                        rTableRED[currentPosition][nextAction] = -100
                        rTableBLUE[currentPosition][nextAction] = -100
                        isTerminal = True
                    else:
                        rTableGREEN[currentPosition][nextAction] = 100
                        mode=3
                # if found blue package
                if(gridType==3):
                    if(packagesRemaining!=0):
                        rTableRED[currentPosition][nextAction] = -100
                        rTableGREEN[currentPosition][nextAction] = -100
                        isTerminal = True
                    else:
                        rTableBLUE[currentPosition][nextAction] = 100
                        isTerminal=True
                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                tableUpdate(currentPosition,nextAction,newPos)
                currentPosition = newPos
            fourRoomsObj.showPath(-1,"./data/Scenario1/Scenario1_iter_{0}_epoch_{1}.png".format(iteration,epoch))
            fourRoomsObj.newEpoch()
            if(e>0):
                e-=0.05
        # printOut()
            

if __name__ == "__main__":
    main()
