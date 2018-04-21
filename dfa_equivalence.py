
from itertools import zip_longest

dfa1AcceptingStates = set()
dfa2AcceptingStates = set()
equivalent = True

def openFile(fileName):
    file = open(fileName ,'r')
    return [list(map(int, line.rstrip().split('  '))) for line in file][1:]

def mergeStates(array1, array2):
    return [[stateOne, stateTwo] for stateOne, stateTwo in zip_longest(array1, array2, fillvalue='')]

def checkEquivalence(leftState, rightState):

    global equivalent

    if not equivalent:
        return

    if (leftState not in dfa1AcceptingStates) and (rightState not in dfa2AcceptingStates):
        return

    if (leftState in dfa1AcceptingStates) and (rightState in dfa2AcceptingStates):
        return

    equivalent = False


def compareDFA(dfa1, dfa2):

    queue      = [[0, 0]]
    newDFA     = []
    isSeen     = set()

    while (len(queue) != 0):
        stateLevel = []
        nextStates = queue.pop(0)
        leftState, rightState = nextStates
        if "{},{}".format(leftState, rightState) not in isSeen:
            checkEquivalence(leftState, rightState)
            stateLevel.append([leftState, rightState])
            merged = mergeStates(dfa1[leftState], dfa2[rightState])
            stateLevel += merged
            newDFA.append(stateLevel)

            queue += merged
            isSeen.add("{},{}".format(leftState, rightState))

    return newDFA

def main():
    dfa1 = openFile('dfa3.txt')
    dfa2 = openFile('dfa4.txt')

    dfa1AcceptingStates.update(dfa1.pop(0))
    dfa2AcceptingStates.update(dfa2.pop(0))

    newDFA = compareDFA(dfa1, dfa2)

    if equivalent:
        print("They are equivalent")

    else:
        print("They are not equivalent")

main()
