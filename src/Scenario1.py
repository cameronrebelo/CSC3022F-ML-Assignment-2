from FourRooms import FourRooms
from FourRooms import numpy as np

e = 0.8
qTable = np.zeroes((12,12)) #some default value
rTable = np.zeroes((12,12))
lr = 0.8
discount = 0.5

def explorationFunction(currentPosition):
    #starts off very exploratative and gradualy becomes less
    rand = np.random.Random()
    if(rand>e):
        action = np.random.randint(0,4)
    else:
        action = maxNext(currentPosition)
    e -= 0.5
    return action

def maxNext(currentPosition):
    actions = [qTable[currentPosition[0]][currentPosition[1]-1]
        , qTable[currentPosition[0]][currentPosition[1]+1]
        , qTable[currentPosition[0]-1][currentPosition[1]]
        , qTable[currentPosition[0]+1][currentPosition[1]]]
    max_ = max(actions)
    index = np.random.choice([i for i in range(len(actions)) if actions[i] == max_])
    action = index

def tableUpdate(oldPos,newPos):
    qTable[oldPos[0]][oldPos[1]] = qTable[oldPos[0]][oldPos[1]] + lr *((rTable[oldPos[0]][oldPos[1]] + discount*max(newPos)) - qTable[oldPos[0]][oldPos[1]])



def main():
    for iteration in range(10):
        # Create FourRooms Object
        fourRoomsObj = FourRooms('simple')
        qTable = np.zeroes((12,12))
        rTable = fourRoomsObj.__environment
        rTable[fourRoomsObj.__package_locations[0][0]][fourRoomsObj.__package_locations[0][1]] = 100
        
        for epoch in range(10):
            aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']
            currentPosition = fourRoomsObj.getPosition
            print('Agent starts at: {0}'.format(currentPosition))   
            while(isTerminal==False):
                nextAction = explorationFunction(currentPosition)
                gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(nextAction)
                print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[nextAction], newPos, gTypes[gridType]))
                tableUpdate(currentPosition,newPos)
                currentPosition = newPos
            fourRoomsObj.showPath(-1,)
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
            fourRoomsObj.showPath(-1)
        fourRoomsObj.newEpoch()

if __name__ == "__main__":
    main()
