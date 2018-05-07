from collections import OrderedDict as od

def openFile(fileName):
    file = open(fileName, 'r')
    numstates = int(file.readline())
    acceptingstates = file.readline()
    acceptingstates = [int(i) for i in acceptingstates.split()]
    return [list(map(int, line.rstrip().split())) for line in file][0:], numstates, acceptingstates

def findChildAndLength(parent, child):
    path_count = 0
    while child != parent[child]:
        child = parent[child]
        path_count += 1
    return child, path_count

def union(parent_graph, pair):

    # union and compress path
    parent_node_0, path_count_0 = findChildAndLength(parent_graph['parent'], pair[0])
    parent_node_1, path_count_1 = findChildAndLength(parent_graph['parent'], pair[1])
    #print(parent_node_0, path_count_0, parent_node_1, path_count_1)
    # cases for compressing the path
    if path_count_0 == 0 and path_count_1 == 1:
        parent_graph['parent'][ parent_node_0 ] = parent_node_1

    elif path_count_0 == 1 and path_count_1 == 0:
        parent_graph['parent'][ parent_node_1 ] = parent_node_0

    elif path_count_0 == 1 and path_count_1 == 1:
        parent_graph['parent'][ parent_node_1 ] = parent_node_0
        parent_graph['parent'][ pair[1] ] = parent_node_0

    else:
        parent_graph['parent'][ parent_node_1 ] = parent_node_0
    # the distance from all children to their respective parents should = 1
    return parent_graph['parent']



def findtransition(graph, state, alphabetinput):
    transitionslist = graph['graph'][state]
    #print("translist ", transitionslist)
    goesto = transitionslist[alphabetinput]
    return goesto

#returns set the state belongs to
def find(graph, state):
    return graph['parent'][state]

#def findstatetransitions(parent_graph, state):
    
def getTransitions(parent_graph, state):
    print("parentgraph: ", parent_graph)
    parentlist = parent_graph
    print("should be same: ", parentlist)
    transitions = []
    itr = 0
    for i in parentlist:
        #print("this is i[0]: ", i[0])
        #if parentlist[i][0] == state:
        if i[0] == state: 
            transitions.append(i[1])
            print(state, " goes to state: ", i[1])
    return transitions


# add 2 states to an island
graph = [
    # edge, next state
    [1, 2],
    [0, 3],
    [4, 5],
    [4, 5],
    [4, 5],
    [5, 5],
]
graph2 = [
    # edge, next state
    [1, 3],
    [0, 5],
    [4, 4],
    [4, 3],
    [4, 2],
    [5, 1]
]

def findpair(parentgraph, belongswith):
    #print("this is parentgraph: ", parentgraph)
    #print("this is belongs with: ", belongswith)
    pairstates = []
    #testlist = parent_graph
    itr = 0
    for i in parentgraph:
        #itr+=1
        if parentgraph[i] == belongswith:
            #print("if statement hits!")
            pairstates.append(itr)
        itr+=1 
    return pairstates

def unionfindcompare(dfa1file, dfa2file):
    dfa1, dfa1numstates, dfa1accept = openFile(dfa1file)
    dfa2, dfa2numstates, dfa2accept = openFile(dfa2file)
    
    updateddfa2accept = []
    for i in dfa2accept:
        #print("this is i: ", i)
        updateddfa2accept.append(i+len(dfa1))

    combinedaccept = dfa1accept + updateddfa2accept
        
    combineddfa = dfa1 + changestatenames(dfa1, dfa2)
    
    parent_graph = od([
            ('graph', combineddfa),
            ('parent', createparentlist(combineddfa))
        ])
    
    parent_graph['parent'] = union(parent_graph,(0, len(dfa1)))

    stack = []
    stack.append(findpair(parent_graph['parent'],0))
    while(len(stack) != 0):
        #singleset should only ever be a pair of 2 states
        singleset = stack.pop()
        dfa1state = singleset[0]
        dfa2state = singleset[1]
        #print(dfa1state, dfa2state)
        #for every transition between the 2 states, find the 
        #sets that they belong to and if they do not equal each
        #other, union them and push onto stack.
        alphabetsize = len(parent_graph['graph'][0])
        #print("size of alphabet: ", len(parent_graph['graph'][0]))
        #while(alphabetsize > 0):
        for i in range(alphabetsize):
            transition1 = findtransition(parent_graph, dfa1state, i)
            r1 = find(parent_graph, transition1)
            transition2 = findtransition(parent_graph, dfa2state, i)
            r2 = find(parent_graph, transition2)
            #print("r1 and r2 = ", r1, r2)
            if r1 != r2:
                parent_graph['parent'] = union(parent_graph, (r1,r2))
                temp = []
                temp.append(r1)
                temp.append(r2)
                stack.append(temp)
        singleset = []
    
    #print(combinedaccept)
    #print(parent_graph['parent'])
     
    if checkequivalence(parent_graph, combinedaccept):
        print("The dfas are equal!")
    else: print("The dfas are not equal!")

def checkequivalence(graph, acceptingstates):
    #for i in acceptingstates:
        #for j in graph['parent']:
    acceptingflag = False
    notacceptingflag = False
    itr = 0
    myset = set(graph['parent'])
    #print(myset)
    mysetlist = list(myset)
    #print(mysetlist)
    for i in mysetlist:
        itr = 0
        for j in graph['parent']:
            if i == j and itr in acceptingstates:
                #print("acceptflag set for: ", i)
                acceptingflag = True
            elif i == j and itr not in acceptingstates:
                #print("not acceptflag set for: ", i)
                notacceptingflag = True
            if acceptingflag == True and notacceptingflag == True:
                return False
            itr += 1
        acceptingflag = False
        notacceptingflag = False
    return True

#changes the dfa2 state numbers so they don't match dfa1's
def changestatenames(dfa1, dfa2):
    newg2 = []
    temp =[]
    graphnumstate = len(dfa1)
    for i in dfa2:
        for j in range(len(i)):
            temp.append(i[j] + graphnumstate)
            #print("this is temp: ", temp)
        #temp.append(i[0] + graphnumstate)
        #temp.append(i[1] + graphnumstate)
        newg2.append(temp)
        temp = []
    return newg2

def createparentlist(dfa):
    parentlist = []
    dfanumstates = len(dfa)
    for i in range(len(dfa)):
        parentlist.append(i)
    return parentlist
     
#this is wrong for parent, it counts all transitions not states
'''
parent_graph = od([
        ('graph', graph3),
        ('parent', [ i for i, next_states in enumerate(graph3)])
    ])
'''

'''
these should be different I think?
unionfindcompare('dfa3.txt', 'dfa4.txt')
'''

'''
these should be equal, the text files are identical
unionfindcompare('dfa3.txt', 'copydfa3.txt')
'''

#should be equal (is the example the pdf describing the alg was using: 
#program says they are! woohoo!
#unionfindcompare('testdfa.txt', 'testdfa2.txt')

unionfindcompare('dfa3.txt', 'dfa4.txt')
