import sys
from FourRooms import FourRooms
import numpy as np

e = 0.8
lr = 1
discount = 0.5

qTable = {}
rTable = {}

stoFlag = False

aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

def explorationFunction(currentPosition):
    global e
    #starts off very exploratative and gradualy becomes less
    if(np.random.random()<e):
        action = np.random.randint(0,4)
        # Make sure agent is moving to valid state, if not, choose again
        while(isLegalPosition(currentPosition, action)==False):
            action = np.random.randint(0,4)
    else:
        action = maxNext(currentPosition, False)
        # Make sure agent is moving to valid state, if not, choose again
        while(isLegalPosition(currentPosition, action)==False):
            action = maxNext(currentPosition, False)
    return action

# Choose best action to take in current position
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

# check if the agent is in a legal position
def isLegalPosition(currentPosition,action):
    if(rTable[currentPosition][action]==-1):
        return False
    return True


def main():
    global qTable
    global rTable
    global e
    global stoFlag

    # CLI
    if(len(sys.argv) >1):
        if(sys.argv[1] == '-stochastic'):
            stoFlag = True
    
    for iteration in range(1):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('simple', stoFlag)

        # Init Q and Rewards tables using environment details
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


        for epoch in range(20):

            # Starting Position
            currentPosition = fourRoomsObj.getPosition()
            print('Agent starts at: {0}'.format(currentPosition))   

            # Repeat until in a terminal state
            isTerminal=fourRoomsObj.isTerminal()
            while(isTerminal==False):

                nextAction = explorationFunction(currentPosition)
                gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(nextAction)

                # Found package
                if(gridType>0):
                    rTable[currentPosition][nextAction] = 100

                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                tableUpdate(currentPosition,nextAction,newPos)
                # Update position
                currentPosition = newPos

            fourRoomsObj.showPath(-1,"./data/Scenario1/Scenario1_iter_{0}_epoch_{1}.png".format(iteration,epoch))
            fourRoomsObj.newEpoch()
            # Decrease e threshold to make agent more exploitative
            if(e>0):
                e-=0.05
            

if __name__ == "__main__":
    main()
