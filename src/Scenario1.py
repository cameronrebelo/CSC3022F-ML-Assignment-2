from FourRooms import FourRooms
import numpy as np

e = 0
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
        action = np.random.randint(0,4)
        while(isLegalPosition(currentPosition, action)==False):
            action = np.random.randint(0,4)
    else:
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
        return False
    return True

def main():
    global qTable
    global rTable
    
    for iteration in range(1):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('simple')
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
        hrznHall = [(3,6),(10,6)]
        for i in hrznHall:
            rTable[i][0] = -1
            rTable[i][1] = -1
            rTable[i][2] = 0
            rTable[i][3] = 0
        vertHall = [(6,2),(7,9)]
        for i in vertHall:
            rTable[i][0] = 0
            rTable[i][1] = 0
            rTable[i][2] = -1
            rTable[i][3] = -1
        wallList = [(6,1),(6,3),(6,4),(6,5),(7,7),(7,8),(7,10),(7,11)]
        for i in wallList:
            for a in range(4):
                rTable[i][j] = -1
        print(rTable)
        # print(qTable)
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
                    rTable[currentPosition][nextAction] = 100
                    # qTable[newPos[0]][newPos[1]] = 100
                    # print("updated R table")
                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                tableUpdate(currentPosition,nextAction,newPos)
                # print("Q\n\n",qTable)
                currentPosition = newPos
            # print("Q\n\n",qTable)
            fourRoomsObj.showPath(-1,"./data/Scenario1_iter_{0}_epoch_{1}.png".format(iteration,epoch))
            fourRoomsObj.newEpoch()
            


            # This will try to draw a zero
            # actSeq = [FourRooms.LEFT, FourRooms.LEFT, FourRooms.LEFT,
            #         FourRooms.UP, FourRooms.UP, FourRooms.UP,
            #         FourRooms.RIGHT, FourRooms.RIGHT, FourRooms.RIGHT,
            #         FourRooms.DOWN, FourRooms.DOWN, FourRooms.DOWN]


            # for act in actSeq:
            #     gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(act)

            #     print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[act], newPos, gTypes[gridType]))

            #     if isTerminal:
            #         break

            # Don't forget to call newEpoch when you start a new simulation run

            # Show Path
        #     fourRoomsObj.showPath(-1)
        # fourRoomsObj.newEpoch()

if __name__ == "__main__":
    main()
