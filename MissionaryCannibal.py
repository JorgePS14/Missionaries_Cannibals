class Boat(object):
    def __init__(self, side, missionaries=0, cannibals=0):
        self.side = side
        self.missionaries = missionaries
        self.cannibals = cannibals

    def board(self, missionaries, cannibals):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.side.missionaries = self.side.missionaries - self.missionaries
        self.side.cannibals = self.side.cannibals - self.cannibals

    def travel(self):
        self.side = self.side.otherSide
        self.side.missionaries = self.side.missionaries + self.missionaries
        self.side.cannibals = self.side.cannibals + self.cannibals
        self.missionaries = 0
        self.cannibals = 0


class Shore(object):
    def __init__(self, side, missionaries=0, cannibals=0, otherSide=None):
        self.side = side
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.otherSide = otherSide

    def getPeople(self):
        people = ['M']*self.missionaries+['C']*self.cannibals
        return people

def initialize():
    leftShore = Shore("Left",3,3)
    rightShore = Shore("Right")
    leftShore.otherSide = rightShore
    rightShore.otherSide = leftShore
    boat = Boat(leftShore, 0, 0)
    return leftShore, rightShore, boat

leftShore, rightShore, boat = initialize()
transitions = {1:(2,0), 2:(0,2), 3:(1,1), 4:(1,0), 5:(0,1)}

def keepSearching(goal, lastTravel, visited):
    currentState = (leftShore.getPeople(), rightShore.getPeople())
    if currentState == goal:
        return visited
    else:
        courses = analyzeCourses(visited, boat.side, lastTravel)
        if courses:
            for course in courses:
                newCurrentState = (leftShore.getPeople(), rightShore.getPeople())
                if checkValidity(boat, course):
                    print(newCurrentState)
                    visited.append(newCurrentState)
                    keepSearching(goal, course, visited)
        boat.board(lastTravel[0], lastTravel[1])
        boat.travel()
    return visited

def checkValidity(boat, crew):
    boat.board(crew[0], crew[1])
    boat.travel()
    if (leftShore.missionaries >= leftShore.cannibals or leftShore.missionaries == 0) and (rightShore.missionaries >= rightShore.cannibals or rightShore.missionaries == 0):
        return True
    boat.board(crew[0], crew[1])
    boat.travel()
    return False

def searchSolution(goal):
    visited = []
    currentState = (leftShore.getPeople(), rightShore.getPeople())
    visited.append(currentState)
    print(currentState)
    courses = analyzeCourses(visited, boat.side)
    for course in courses:
        if checkValidity(boat, course):
            visited = keepSearching(goal, course, visited)
            if visited[-1] == goal:
                return visited
    return visited

def analyzeCourses(visited, currShore, lastTravel=None):
    trans = []
    if currShore.cannibals > 0:
        trans.append(transitions[5])
        if currShore.cannibals > 1:
            trans.append(transitions[2])
        if currShore.missionaries > 0:
            trans.append(transitions[4])
            trans.append(transitions[3])
            if currShore.missionaries > 1:
                trans.append(transitions[1])
    elif currShore.missionaries > 0:
        trans.append(transitions[4])
        if currShore.missionaries > 1:
            trans.append(transitions[1])
    
    if lastTravel:
        trans.remove(lastTravel)

    return trans

print("\nHistory of states: \n\n"+str(searchSolution(([], ['M','M','M','C','C','C']))))