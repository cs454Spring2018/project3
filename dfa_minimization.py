# dfa mimization
# example from https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm
graph = [
	# edge, next state
	[1, 2],
	[0, 3],
	[4, 5],
	[4, 5],
	[4, 5],
	[5, 5]
]
'''
graph = [
	# edge, next state
	[1, 0],
	[3, 0],
	[1, 1],
	[4, 5],
	[4, 5],
	[5, 5],
	
]
'''

# upgrade so a table is used instead of adjaciency list
# remove states unreachable
# bfs
# after bfs is over read the visited list
# all items with 0 can be deleted

def Pop(queue):
	item = queue[0]
	del queue[0]
	return item

def Push(queue, item):

	queue.append(item)
	return queue
def bfs(state_transition_table, start_state, alphabet, accepting_states):

	visited = [0] * len(state_transition_table)
	queue = []
	visited[start_state] = 1
	queue = Push(queue, start_state)


	while queue != []:
		current_remainder = Pop(queue)
		next_remainders = [next_remainder for i, next_remainder in enumerate(state_transition_table[current_remainder])]

		for next_remainder in next_remainders:

			if visited[next_remainder] == 0:
				visited[next_remainder] = 1
				queue = Push(queue, next_remainder)
	
	return visited

def deleteNodes(graph, visited):
	new_graph = {i: row for i, row in enumerate(graph)}
	for j, bin_ in enumerate(visited):
		if visited[j] == 0:
			del new_graph[j]
	#print(new_graph)
	offset_map = {key: i for i, key in enumerate(list(new_graph.keys()))}
	#print(offset_map)
	third_graph = []
	for i in new_graph:
		row = []
		for j in new_graph[i]:
			row.append(offset_map[j])
		third_graph.append(row)

	return third_graph


def markWAcceptingState(i, j, table, new_items_added):
	if (j in accepting_states) and (i not in accepting_states) or (
		j not in accepting_states) and (i in accepting_states):

		# (j, i) because the j axis starts first
		table[j][i] = 1
		new_items_added.append((j, i))


def markWithPreviouslyMarked(i, j, table, new_items_added, graph):

	# (j, i) because the j axis starts first
	#print(graph)
	next_states = [ [ graph[j][k], graph[i][k] ] for k, edge in enumerate(graph[i]) ]
	#print(next_states)
	#[print(a) for a in table]
	for jj, ii in next_states:
		#print(jj, ii)
		if table[j][i] == 0 and table[jj][ii] == 1:

			table[j][i] = 1
			new_items_added.append((j, i))


def tableFilling(dfa, accepting_states, f, g):

	total_states = len(dfa)
	table = []
	for a in range(total_states):
		row = []
		for b in range(total_states):
			if a == b:
				row.append(3)
			else:
				row.append(0)
		table.append(row)
	

	first_round = True
	new_items_added = [0]

	while new_items_added != []:
		new_items_added = []

		# visits all slots in table 1 time
		j = 1
		while j < len(table):
			i = 0
			while i < j:
				if first_round:
					f(i, j, table, new_items_added)

				else:
					g(i, j, table, new_items_added, graph)
				i += 1
			j += 1
		first_round = False

		#[print(a) for a in table]
		#print()
	return table



def collectIslands(table):

	islands = []
	j = 1
	while j < len(table):
		i = 0
		while i < j:
			if table[j][i] == 0:
				islands.append(collectNeighbors(i, j, table))

			i += 1
		j += 1

	return islands
def collectNeighbors(i, j, table):

	# all neighbors of this form can be marged into a single unique state combo if the union of all neighbors and start cell is taken
	# y: x
	#j + 1: [i+0, i+1, i + 2, ...] i < j
	# go 1 down
	# go across all untill out of range
	# all unmarked cells found go into a group

	island = []
	

	# each island is separated by a partial row(each row is not completely used in the program) completely covered in 1's
	jj = j
	while jj < len(table):
		wall = []
		ii = i

		while ii < jj:
			#print(ii, jj)
			if table[jj][ii]:
				wall.append(1)
			else:
				island.append((ii, jj))
				table[jj][ii] = 2

			ii += 1
		# there is a wall of 1's
		if len(wall) == ii:
			break
		jj += 1
	return island
	
def collectCombos(table):
	combos = []
	j = 1
	while j < len(table):
		i = 0
		while i < j:
			if table[j][i] == 0:
				combos.append((i, j))
			i += 1
		j += 1
	return combos
def getStatesPartOfCombos(state_combinations):
	states_part_of_combos = set()
	for k, l in state_combinations:
		states_part_of_combos.add(k)
		states_part_of_combos.add(l)
	return states_part_of_combos

def makeNonEqualStateSingletons(non_equal_states):

	return [ [state] for state in non_equal_states]


NFA = [
    [[0, 1], [0, 3]],
    [[0, 2], [1, 2]],
    [[3, 0], [0]],
    [[], []],

]

import copy
def currentStates(current_state):

    if len(current_state.split('_')) > 1:
        return [int(j) for j in current_state.split('_')]
    else:
        return [int(current_state)]
    #return next_states

def nextStates(A, col, current_states):

    current_col = set()
    
    #print("HERE")
    for state in current_states:
        #print(state, " " , col)
        for next_state in A[state][col]:
            current_col.add(next_state)
    #print("HERE")
    return current_col

def nextComboState(A, combo_state):

    next_combo_states = []
    #print(A[0][0])
 #  #print(A[0])
    for col, next_states in enumerate(A[0][0]):
        current_states = currentStates(combo_state)

        current_col = nextStates(A, col, current_states)

        next_combo_states.append(('_'.join([str(j) for j in current_states]),
                                '_'.join([str(i) for i in sorted(copy.deepcopy(current_col))])))
        #after the new combo state have been collected, intersect them with the minimized dfa states
        #if it intersects with a min dfa state
        #	replace it with the dfa state in next_combo_states
        #print("SUPERHERE")
    return next_combo_states

def makeRow(B, combo_state, A, next_combo_states):

    row = [] 
    for i, next_state in enumerate(next_combo_states):
        row.append(next_state[1])
    return row

def addAcceptingStatesToF(current_combo_state, F, combo_state, accepting_states):

    for number in [int(k) for k in combo_state.split('_')]:
        if number in accepting_states:
            F.add(current_combo_state)
    return F

def appendNextComboStates(unadded_states, next_combo_states):
    for j in next_combo_states:
        unadded_states.append(j[1])
    return unadded_states



def convertNFAToDFA(A, accepting_states):

    unadded_states = ['0']

    F = set()
    B = od([])
    while unadded_states != []:


        combo_state = unadded_states[0]
        del unadded_states[0]

        next_combo_states = nextComboState(A, combo_state)

        current_combo_state = next_combo_states[0][0]

        F = addAcceptingStatesToF(current_combo_state, F, combo_state, accepting_states)

        B[combo_state] = makeRow(B, combo_state, A, next_combo_states)

        unadded_states = appendNextComboStates(unadded_states, next_combo_states)

        x = set(unadded_states)
        y = set(B.keys())
        if list(x & y) != []:

            unadded_states = list(x - y)

    return B, F

# use nfa to dfa converter to finish the process
accepting_states = [2, 3, 4]

x = bfs(graph, 0, [0, 1], accepting_states)
#print(x)
revised_graph = deleteNodes(graph, x)
#print(revised_graph)
#exit()

table = tableFilling(graph, accepting_states, markWAcceptingState, markWithPreviouslyMarked)
'''
table = [
	[3, 0, 0, 0, 0, 0],
	[0, 3, 0, 0, 0, 0],
	[0, 0, 3, 0, 0, 0],
	[0, 1, 0, 3, 0, 0],
	[1, 1, 0, 0, 3, 0],
	[1, 1, 1, 1, 1, 3]
]
'''

islands = collectIslands(table)
[print(a) for a in table]
print()
print(islands)
# convert into combo states and have a list of all state involved with the combo states
sets = []
combo_states = set()
for island in islands:
	new_set = set()
	for tuple_ in island:
		for state in tuple_:
			new_set.add(state)
			combo_states.add(state)
	sets.append('_'.join([str(i) for i in new_set]))
print(sets)
print(list(combo_states))

# 234 -> 4 via 0
# nfa -> dfa would assume 4 is a new state
# instead of making new states intersect the new state with the current state and if new state in dfa states then use current state

exit()
equality_combos = collectCombos(table)

states_part_of_combos = getStatesPartOfCombos(equality_combos)

#print(equality_combos)
#print(states_part_of_combos)

non_equal_states = set(graph.keys())- states_part_of_combos
#print(non_equal_states)
non_equal_state_singletons = makeNonEqualStateSingletons(non_equal_states)

#print(non_equal_state_singletons)

transitiveProperty(equality_combos)