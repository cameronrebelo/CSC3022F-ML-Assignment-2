from FourRooms import FourRooms
import numpy as np

e = 0.5
qTable = {} #some default value
rTable = {}

lr = 1
discount = 0.5
aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

def explorationFunction(currentPosition):
    global e
    #starts off very exploratative and gradualy becomes less
    if(np.random.random()<e):
        print("random")
        action = np.random.randint(0,4)
        while(isLegalPosition(currentPosition, action)==False):
            action = np.random.randint(0,4)
    else:
        print("deterministic")
        action = maxNext(currentPosition, False)
        while(isLegalPosition(currentPosition, action)==False):
            action = maxNext(currentPosition, False)
    # if(e>0):          
    #     e -= 0.5
    return action

def maxNext(currentPosition, update):
    actions = [
                 qTable[currentPosition][0]
                ,qTable[currentPosition][1]
                ,qTable[currentPosition][2]
                ,qTable[currentPosition][3]
              ]
    maxQValue = max(actions)
    if(update==True):
        return maxQValue
    maxIndex = np.random.choice([i for i in range(len(actions)) if actions[i] == maxQValue])
    return maxIndex



def tableUpdate(oldPos,action,newPos):
    global qTable
    qTable[oldPos][action] += lr *((rTable[oldPos][action] + discount*maxNext(newPos, True)) -  qTable[oldPos][action])


def nextActionReward(currentPosition, action):
    if(action == 0 ):
        return rTable[currentPosition[0]][currentPosition[1]-1]
    if(action == 1 ):
        return rTable[currentPosition[0]][currentPosition[1]+1]
    if(action == 2 ):
        return rTable[currentPosition[0]-1][currentPosition[1]]
    if(action == 3 ):
        return rTable[currentPosition[0]+1][currentPosition[1]]

def isLegalPosition(currentPosition,action):
    if(rTable[currentPosition][action]==-1):
        print("illegal")
        for a in range(4):
            print(rTable[currentPosition][a])
        return False
    print("legal")
    return True


def printOut():
    for i in range(13):
        for j in range(13):
            name = (i,j)
            first = rTable[name][0]
            second = rTable[name][1]
            third = rTable[name][2]
            fourth = rTable[name][3]
            print(name, first, second, third, fourth)
            



def main():
    global qTable
    global rTable
    
    for iteration in range(1):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('multi')
        for i in range(13):
            for j in range(13):
                qTable[(i,j)] = {}
                rTable[(i,j)] = {}
                for k in range(4):
                    qTable[(i,j)][k] = 0
                    rTable[(i,j)][k] = 0
        for i in range (13):
            for j in range(13):
                if(i == 0 or i == 12 or j == 0 or j == 12 or j == 6):
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
        wallList = [(6,1),(6,3),(6,4),(6,5),(7,7),(7,8),(7,10),(7,11)]
        for i in wallList:
            for a in range(4):
                rTable[i][j] = -1

        printOut()
        for epoch in range(10):

            # Starting Position
            currentPosition = fourRoomsObj.getPosition()
            print('Agent starts at: {0}'.format(currentPosition))   

            # Repeat until in a terminal state
            isTerminal=fourRoomsObj.isTerminal()
            while(isTerminal==False):
                nextAction = explorationFunction(currentPosition)
                gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(nextAction)
                if(gridType>0):
                    if(packagesRemaining>0):
                        rTable[currentPosition][nextAction] = 100
                        # set current found package temp to 0
                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                tableUpdate(currentPosition,nextAction,newPos)
                # print("Q\n\n",qTable)
                currentPosition = newPos
            # print("Q\n\n",qTable)
            fourRoomsObj.showPath(-1,"./data/Scenario1_iter_{0}_epoch_{1}.png".format(iteration,epoch))
            fourRoomsObj.newEpoch()
            

if __name__ == "__main__":
    main()
