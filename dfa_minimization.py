# dfa mimization
# example from https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm
from collections import defaultdict
from collections import OrderedDict as od
import copy
from functools import reduce

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
def collectIslandParts(table):

	islands = []
	j = 1
	while j < len(table):
		i = 0
		while i < j:
			if table[j][i] == 0:
				islands.append((i, j))

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
    #print(current_col)
    return current_col

def nextComboState(A, combo_state, minimized_dfa_states):

	next_combo_states = []
	replacement_next_combo_states = []

	#print(A[0][0])
	#print(A[0])
	#exit()
	#print('getting next combo state')

	for col, next_states in enumerate(A[0]):
		#print(col, next_states, combo_state)
		current_states = currentStates(combo_state)

		current_col = nextStates(A, col, current_states)
		next_combo_states.append('_'.join([str(j) for j in current_col]))
	#print(next_combo_states)
		#print(minimized_dfa_states)
		
		#next_combo_states = [tuple(replacement_next_combo_states)]
		#print(next_combo_states)

		#exit()
		#after the new combo state have been collected, intersect them with the minimized dfa states
		#if it intersects with a min dfa state
		#	replace it with the dfa state in next_combo_states
		#print("SUPERHERE")
	#exit()
	for i, state in enumerate(next_combo_states):
		#print(i, state)
		for j, minimized_dfa_combo_state in enumerate(minimized_dfa_states):
			if set(state.split('_')).intersection(set(minimized_dfa_combo_state.split('_'))) != set():

				replacement_next_combo_states.append(minimized_dfa_combo_state)

				#print(replacement_next_combo_states)

		#print(next_combo_states)
		#print(col)
		#print(minimized_dfa_states)
	#print(replacement_next_combo_states)
	#print('end of next combo state')
	#print()
	return replacement_next_combo_states

def makeRow(B, combo_state, A, next_combo_states):

    row = [] 
    for i, next_state in enumerate(next_combo_states):
        row.append(next_state)
    return row

def addAcceptingStatesToF(current_combo_state, F, combo_state, accepting_states):

    for number in [int(k) for k in combo_state.split('_')]:
        if number in accepting_states:
            F.add(current_combo_state)
    return F

def appendNextComboStates(unadded_states, next_combo_states):
    for j in next_combo_states:
        unadded_states.append(j)
    return unadded_states



def convertNFAToDFA(A, accepting_states, minimized_dfa_states):


    unadded_states = [ i for i in minimized_dfa_states]
    F = set()
    B = od([])
    while unadded_states != []:


        combo_state = unadded_states[0]
        del unadded_states[0]

        next_combo_states = nextComboState(A, combo_state, minimized_dfa_states)

        current_combo_state = next_combo_states[0][0]

        F = addAcceptingStatesToF(current_combo_state, F, combo_state, accepting_states)
        #print('combo states')
        #print(combo_state)
        #print(makeRow(B, combo_state, A, next_combo_states))
        #print('end of combo states')
        B[combo_state] = makeRow(B, combo_state, A, next_combo_states)
        #print('after adding')
        #print(unadded_states, next_combo_states)

        unadded_states = appendNextComboStates(unadded_states, next_combo_states)
        #print(unadded_states)

        #print()

        x = set(unadded_states)
        y = set(B.keys())
        if list(x & y) != []:

            unadded_states = list(x - y)

    return B, F
def generateUnionFindPairIndecies(island_parts):

	total_states = len(island_parts)
	table = []
	for a in range(total_states):
		row = []
		for b in range(total_states):
			if a == b:
				row.append(3)
			else:
				row.append(0)
		table.append(row)

	pairs = []
	j = 1
	while j < len(table):
		i = 0
		while i < j:
			pairs.append([i, j])
			i += 1
		j += 1
	return pairs

def canMerge(pair, id_island_parts):
	a = set(id_island_parts[ pair[0] ])
	b = set(id_island_parts[ pair[1] ])
	c = a.intersection(b)
	if c != set():
		return True
	return False
def find(parent, child):
	path_count = 0
	while child != parent[child]:
		child = parent[child]
		path_count += 1
	return child, path_count
def union(parent, pair, id_island_parts):
	if canMerge(pair, id_island_parts):

		# union and compress path
		parent_node_0, path_count_0 = find(parent, pair[0])
		parent_node_1, path_count_1 = find(parent, pair[1])

		# cases for compressing the path
		if path_count_0 == 0 and path_count_1 == 1:
			parent[ parent_node_0 ] = parent_node_1

		elif path_count_0 == 1 and path_count_1 == 0:
			parent[ parent_node_1 ] = parent_node_0

		elif path_count_0 == 1 and path_count_1 == 1:
			parent[ parent_node_1 ] = parent_node_0
			parent[ pair[1] ] = parent_node_0

		else:
			parent[ parent_node_1 ] = parent_node_0
		# the distance from all children to their respective parents should = 1
	return parent

def makeIslands(parent, island_parts):

	pairs = generateUnionFindPairIndecies(island_parts)


	for k, pair in enumerate(pairs):

		parent = union(parent, pairs[k], id_island_parts)

	# group each set of children -> parent in parent so each set can be accessed using the parent key 
	island_id = defaultdict(int)

	for i, parent_node in enumerate(parent):
		if island_id[parent_node]:
			island_id[parent_node].append(i)
		else:
			island_id[parent_node] = [i]
	return island_id

def makeMinimizedDFAStates(islands, island_parts):
	minimized_dfa_states = []
	for id_ in islands:
		dfa_combo_keys = islands[id_]

		minimized_dfa_state = set()
		for i in dfa_combo_keys:
			minimized_dfa_state = minimized_dfa_state.union(island_parts[i])

		minimized_dfa_states.append('_'.join(map(str, minimized_dfa_state)))
	return minimized_dfa_states


graph = [
	# edge, next state
	[1, 2],
	[0, 3],
	[4, 5],
	[4, 5],
	[4, 5],
	[5, 5]
]
def convertToNFAStyle(dfa):

	new_nfa = []
	for state in dfa:
		row = []
		for next_state in state:
			row.append([next_state])
		new_nfa.append(row)
	return new_nfa

def convertStringsInDFAToNumbers(minimized_dfa, string_int):

	number_minimized_dfa = []
	for key in minimized_dfa:
		next_states_numbers = []
		for next_states in minimized_dfa[key]:

			next_states_numbers.append(string_int[next_states])
		number_minimized_dfa.append(next_states_numbers)
	return number_minimized_dfa

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

NFA = [
    [[0, 1], [0, 3]],
    [[0, 2], [1, 2]],
    [[3, 0], [0]],
    [[], []],

]

# the largest path for each island id is the island
# use nfa to dfa converter to finish the process
accepting_states = [2, 3, 4]
# get rid of unused states
x = bfs(graph, 0, [0, 1], accepting_states)
#print(x)
revised_graph = deleteNodes(graph, x)



#print(revised_graph)
#exit()
# collect all pairs of equvalent states
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

#counterexample
'''
table = [
	[3, 0, 0, 0, 0, 0],
	[0, 3, 0, 0, 0, 0],
	[1, 1, 3, 0, 0, 0],
	[1, 1, 0, 3, 0, 0],
	[0, 1, 0, 0, 3, 0],
	[1, 1, 1, 1, 1, 3]
]
'''
'''
table = [
	[3, 0, 0, 0, 0, 0],
	[0, 3, 0, 0, 0, 0],
	[1, 1, 3, 0, 0, 0],
	[1, 0, 1, 3, 0, 0],
	[1, 1, 1, 1, 3, 0],
	[1, 1, 1, 0, 0, 3]
]
'''
island_parts = collectIslandParts(table)



#print(transitiveProperty(island_parts))
#print(island_parts)
#island_parts = [(0, 1), (2, 3), (3, 4), (5, 6), (7, 6)]
#exit()

#id_island_parts = {i : island_part for i, island_part in enumerate(island_parts)}
# create longest sequences that satisfy the transitive property(the number of longest sequences = # of states in mimized dfa)
parent = [ i for i, island_part in enumerate(island_parts) ]
id_island_parts = { i : island_part for i, island_part in enumerate(island_parts) }


islands = makeIslands(parent, island_parts)

#[print(parent_node, i) for i, parent_node in enumerate(parent)]
equal_minimized_dfa_states = makeMinimizedDFAStates(islands, island_parts)


# get the states that are not equal
equivalent_states = reduce( (lambda x, y: x.union(y)), [ set(map(int, i.split('_'))) for i in  equal_minimized_dfa_states ] )
#print(equivalent_states)
#print(equivalent_states)
#print(set(i for i, edges in enumerate(graph)))
non_equal_states = [ str(i) for i in list( set( i for i, edges in enumerate(graph) ) - equivalent_states ) ]
#print(non_equal_states)

#print(equal_minimized_dfa_states)

minimized_dfa_states = equal_minimized_dfa_states + non_equal_states
#print(minimized_dfa_states)

nfa_style = convertToNFAStyle(graph)
#[print(i) for i in nfa_style]
#print()
(DFA, F) = convertNFAToDFA(nfa_style, accepting_states, minimized_dfa_states)

#[print(i, DFA[i]) for i in DFA]
#print(DFA)
#print(minimized_dfa_states)
string_int = {key : i for i, key in enumerate(list(DFA.keys()))}
#print(string_int)
number_minimized_DFA = convertStringsInDFAToNumbers(DFA, string_int)
[print(i, number_minimized_DFA[i]) for i, next_states in enumerate(number_minimized_DFA)]
#print(accepting_states)
replacement_next_combo_states = set()
for i, state in enumerate(accepting_states):
		#print(i, state)
		for j, minimized_dfa_combo_state in enumerate(minimized_dfa_states):
			if set(str(state)).intersection(set(minimized_dfa_combo_state.split('_'))) != set():

				replacement_next_combo_states.add(minimized_dfa_combo_state)
#print(list(replacement_next_combo_states))
minimized_final_states = []
for i in replacement_next_combo_states:
	minimized_final_states.append(string_int[i])
print(minimized_final_states)




# if pair 1 intersects with pair 2
	# use union
#transitiveProperty(island_parts)
# 234 -> 4 via 0
# nfa -> dfa would assume 4 is a new state
# instead of making new states intersect the new state with the current state and if new state in dfa states then use current state

exit()