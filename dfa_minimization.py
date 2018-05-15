# dfa mimization
# example from https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm
from collections import defaultdict
from collections import OrderedDict as od
import copy
from functools import reduce

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
	'''

	graph = [
	[1, 2],
	[1, 2],
	[3, 0],
	[4, 0],
	[4, 0]
	
]
	(j, i)
	2 -> 3  on 0
	1 -> 1 on 0
	(3, 1)


	2 -> 0  on 1
	1 -> 2 on 1
	(0, 2)
	

	[
	[1, 2],
	[1, 2]
	]

	'''
	#x = [[graph[j][k] for k, edge in enumerate(graph[i]) ]] + [[ graph[i][k] for k, edge in enumerate(graph[i]) ]]
	#print(x)
	#print('p q')
	#print(i, j)
	#print()
	next_states = [ [ graph[j][k], graph[i][k] ] for k, edge in enumerate(graph[i]) ]
	#print('[(r s)]')
	#print(next_states)
	#print()
	for ii, jj in next_states:
		#print(ii, jj)
		# need to check both axies using (ii, jj)
		if (table[jj][ii] == 1 or table[ii][jj] == 1) and table[j][i] == 0:
			table[j][i] = 1
			new_items_added.append((j, i))

	#[print(a) for a in table]

	#print()

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
					if table[j][i] != 1:
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
    #print('current state')
    #print(current_states)
    #print("HERE")
    for state in current_states:
        #print(state, " " , col, ' ', A[state][col])
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
	#print(combo_state)
	for col, next_states in enumerate(A[0]):
		#print(col, next_states, combo_state)
		current_states = currentStates(combo_state)
		#print(current_states)
		current_col = nextStates(A, col, current_states)
		#print(col, current_col)
		#print()
		next_combo_states.append('_'.join([str(j) for j in current_col]))
	print('combo states')
	print(next_combo_states)
	#print(minimized_dfa_states)

		#print(minimized_dfa_states)
		
		#next_combo_states = [tuple(replacement_next_combo_states)]
		#print(next_combo_states)

		#exit()
		#after the new combo state have been collected, intersect them with the minimized dfa states
		#if it intersects with a min dfa state
		#	replace it with the dfa state in next_combo_states
		#print("SUPERHERE")
	#exit()
	print()
	print('minimized dfa states')
	print(minimized_dfa_states)
	print()
	print('replacement next combo states')
	for i, state in enumerate(next_combo_states):
		#print(i, state)
		for j, minimized_dfa_combo_state in enumerate(minimized_dfa_states):
			if set(state.split('_')).intersection(set(minimized_dfa_combo_state.split('_'))) != set():
				#print(minimized_dfa_combo_state)
				replacement_next_combo_states.append(minimized_dfa_combo_state)

				print(replacement_next_combo_states)

		#print(next_combo_states)
		#print(col)
		#print(minimized_dfa_states)
	#print(replacement_next_combo_states)
	#print('end of next combo state')
	#print()
	#print('replacement combo states')
	#print(replacement_next_combo_states)
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

	#print(minimized_dfa_states)
	unadded_states = [ i for i in minimized_dfa_states]
	F = set()
	B = od([])
	while unadded_states != []:


		combo_state = unadded_states[0]
		del unadded_states[0]
		#print(combo_state)
		next_combo_states = nextComboState(A, combo_state, minimized_dfa_states)

		current_combo_state = next_combo_states[0][0]
		#print(current_combo_state)
		F = addAcceptingStatesToF(current_combo_state, F, combo_state, accepting_states)
		#print('combo states')
		#print(combo_state)
		#print(makeRow(B, combo_state, A, next_combo_states))
		#print('end of combo states')
		B[combo_state] = makeRow(B, combo_state, A, next_combo_states)
		#print('after adding')
		#print(unadded_states, next_combo_states)
		#print('1')
		#print(combo_state)
		#print(B[combo_state])
		print()
		#print(list(B.keys()))
		#print(unadded_states)
		#print(next_combo_states)
		unadded_states = appendNextComboStates(unadded_states, next_combo_states)
		#print(unadded_states)
		#print()
		# the next_combo_states contains self loops(B's keys) and some of minimized_dfa_states
		# the dict keeps only unadded_states + self loops
		# the self loops are deleted from unadded_states because they are in B's keys
		#print(unadded_states)

		#print()
		#print('unadded_states')
		#print(unadded_states)
		# need to keep all items of unadded_states in same order after the set intersection and set subtraction have been performs
		# enumerate the first locations of each state in unadded_states
		enumerated_unadded_states = od([])
		enumerated_unadded_states_keys = enumerated_unadded_states.keys()
		for i, state in enumerate(unadded_states):
			# only set the first time state has been visited from unadded_states
			if state not in enumerated_unadded_states_keys:
				enumerated_unadded_states[state] = i

		#print(enumerated_unadded_states)
		#print()
		B_keys = B.keys()
		#print('B')
		#print(B)
		#print(list(B_keys))
		#print()
		#print('2')
		#print(list(B.keys()))
		#print(unadded_states)
		#print()
		x = set(unadded_states)
		y = set(B_keys)

		#print(unadded_states)
		new_unadded_states = []
		#print(new_unadded_states)
		if list(x & y) != []:
			# make sure this is the length of the subtracted list
			subtracted_list = list(x - y)
			#print('subtracted list')
			#print(subtracted_list)
			length_of_subtracted_list = len(subtracted_list)
			new_unadded_states = [j for j in range(length_of_subtracted_list)]
			for state in subtracted_list:

				# use the original order of the states in unadded_states to put them in the same order
				# after deleting the states from B_keys
				new_unadded_states[enumerated_unadded_states[state]] = state
		else:
			new_unadded_states = unadded_states
		#print(new_unadded_states)
		unadded_states = new_unadded_states
		#print('finished')
		#print(unadded_states)
		#exit()
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
	#print(a, b)
	#print(c)
	#print(c != set())
	if c != set():
		return True
	return False
def findChildAndLength(parent, child):
	path_count = 0
	while child != parent[child]:
		child = parent[child]
		path_count += 1
	return child, path_count

def compressPaths(parents):

	indicies = [i for i, parent in enumerate(parents)]
	#print(indicies)
	for i in indicies:
		parent, path_count = findChildAndLength(parents, i)
		if path_count >= 2:
			parents[i] = parent
	return parents

def union(parent, pair):

	# union
	parent_node_0, path_count_0 = findChildAndLength(parent, pair[0])
	parent_node_1, path_count_1 = findChildAndLength(parent, pair[1])

	#parent[ parent_node_1 ] = parent_node_0
	if path_count_0 == 0 and path_count_1 == 1:
		parent[ parent_node_0 ] = parent_node_1

	elif path_count_0 == 1 and path_count_1 == 0:
		parent[ parent_node_1 ] = parent_node_0

	elif path_count_0 == 1 and path_count_1 == 1:
		parent[ parent_node_1 ] = parent_node_0
		parent[ pair[1] ] = parent_node_0

	else:
		parent[ parent_node_1 ] = parent_node_0
		
	return parent

def makeIslands(parent, island_parts, id_island_parts):

	pairs = generateUnionFindPairIndecies(island_parts)


	for k, pair in enumerate(pairs):

		if canMerge(pair, id_island_parts):
			#print('passes')
			# index pair indexes not the island parts
			#print(pair)
			#print(pairs[k])

			parent = union(parent, pairs[k])
		#print([i for i in range(len(parent))])
		#print(parent)
		#print()
# [0, 1, 2, 3, 5, 6, 7]
	# the distance from all children to their respective parents should = 1
	parent = compressPaths(parent)

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

'''
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
'''
graph = [
	[2],
	[2],
	[0]
]
'''
def convertToNFAStyle(dfa):

	new_nfa = []
	for state in dfa:
		row = []
		for next_state in state:
			row.append([next_state])
		new_nfa.append(row)
	return new_nfa

def convertStringsInDFAToNumbers(minimized_dfa, string_int):

	#print(minimized_dfa)
	#print(string_int)
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
'''
NFA = [
    [[0, 1], [0, 3]],
    [[0, 2], [1, 2]],
    [[3, 0], [0]],
    [[], []],

]
'''
# the largest path for each island id is the island
# use nfa to dfa converter to finish the process
# get rid of unused states
def minimizeDFA(dfa, alphabet, start_state, accepting_states):
	print(accepting_states)
	x = bfs(dfa, start_state, alphabet, accepting_states)
	print('visited list')
	print(x)
	print()
	#print(x)
	revised_graph = deleteNodes(dfa, x)

	print('nodes with no unreached states')
	[print(b) for b in revised_graph]
	print()

	#print(revised_graph)
	#exit()
	# collect all pairs of equvalent states
	# f = markWAcceptingState
	# g = markWithPreviouslyMarked
	table = tableFilling(dfa, accepting_states, markWAcceptingState, markWithPreviouslyMarked)
	print('table')
	[print(v) for v in table]
	print()
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

	print('coordinates of empty cells')
	print(island_parts)
	print()
	#print(transitiveProperty(island_parts))
	#print(island_parts)
	#print()
	#island_parts = [(0, 1), (2, 3), (3, 4), (5, 6), (7, 6)]
	#exit()
	#print(island_parts)
	#id_island_parts = {i : island_part for i, island_part in enumerate(island_parts)}
	# create longest sequences that satisfy the transitive property(the number of longest sequences = # of states in mimized dfa)
	parent = [ i for i, island_part in enumerate(island_parts) ]
	id_island_parts = { i : island_part for i, island_part in enumerate(island_parts) }
	#print(id_island_parts)

	#print(parent)
	#print(id_island_parts)
	islands = makeIslands(parent, island_parts, id_island_parts)
	print('indicies to coordinates of empty cells whose state represented by coordinates are equivalent')
	[print(c, islands[c]) for c in islands]
	print()
	#exit()
	#print(islands)
	#[print(parent_node, i) for i, parent_node in enumerate(parent)]
	equal_minimized_dfa_states = makeMinimizedDFAStates(islands, island_parts)

	print('minimized dfa states')
	print(equal_minimized_dfa_states)
	print()
	# get the states that are not equal
	#print(equal_minimized_dfa_states)
	# takes the list of combo equivalent states and creates a list of all states involved
	states_that_were_combined = set()
	for states in [ [ int(a) for a in i.split('_') ] for i in equal_minimized_dfa_states ]:
		for state in states:
			states_that_were_combined.add(state)

	print('states that were combined')
	print(list(states_that_were_combined))
	#print(set( i for i, edges in enumerate(graph) ) - states_that_were_combined)
	print()
	'''
	equivalent_states = []
	if equal_minimized_dfa_states != []:

		equivalent_states = reduce( (lambda x, y: x.union(y)), [ set(map(int, i.split('_'))) for i in equal_minimized_dfa_states ] )
	else:
		equivalent_states = set()

	print('equivalent states')
	print(equivalent_states)
	print()
	'''
	#print(equivalent_states)
	#print(equivalent_states)
	#print(set(i for i, edges in enumerate(graph)))
	remaining_states = [ str(i) for i in list( set( i for i, edges in enumerate(graph) ) - states_that_were_combined ) ]
	print('remaining_states')
	print(remaining_states)
	print()


	#print(equal_minimized_dfa_states)

	minimized_dfa_states = equal_minimized_dfa_states + remaining_states
	print('minimized dfa states')
	print(minimized_dfa_states)
	print()
	#exit()
	nfa_style = convertToNFAStyle(graph)
	print('dfa in nfa data structure')
	[print(a) for a in nfa_style]
	print()
	(DFA, F) = convertNFAToDFA(nfa_style, accepting_states, minimized_dfa_states)

	print('minimized dfa with non enumerated states')
	[print(i, DFA[i]) for i in DFA]
	print()
	print('accepting states')
	print(F)
	print()
	#print(minimized_dfa_states)
	string_int = {key : i for i, key in enumerate(list(DFA.keys()))}
	print('enumerated')
	print(string_int)
	print()
	#print(DFA)
	#print()
	number_minimized_DFA = convertStringsInDFAToNumbers(DFA, string_int)
	#[print(i, number_minimized_DFA[i]) for i, next_states in enumerate(number_minimized_DFA)]
	return number_minimized_DFA
'''
graph = [
	[1, 2],
	[0, 2],
	[0, 2]
]
F = {2}
'''
'''
graph = [
	[1, 3],
	[2, 3],
	[0, 3],
	[0, 3]
]
#F = {2}
'''
'''
graph = [
	[1, 2],
	[1, 2],
	[3, 0],
	[4, 0],
	[4, 0]
	
]
F = {0}
'''
graph = [
	[ 2, 4, 1],
	[ 2, 5, 5],
	[ 6, 3, 1],
	[ 3, 3, 3],
	[ 2, 0, 1],
	[ 2, 1, 1],
	[ 2, 3, 1]
]

accepting_states = [3]
alphabet = [0, 1, 2]
start_state = 0
final_minimized_dfa = minimizeDFA(graph, alphabet, start_state, accepting_states)
print('final minimized dfa')
[print(i, final_minimized_dfa[i]) for i, next_states in enumerate(final_minimized_dfa)]
