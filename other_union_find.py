from collections import OrderedDict as od
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
	print(parent_node_0, path_count_0, parent_node_1, path_count_1)
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

def getTransitions(parent_graph, state):
	return parent_graph['graph'][state]
# add 2 states to an island
graph = [
	# edge, next state
	[1, 2],
	[0, 3],
	[4, 5],
	[4, 5],
	[4, 5],
	[5, 5]
]
#parent_graph['parent']
# island_parts is a list of index pairs
parent_graph = od([
		('graph', graph),
		('parent', [ i for i, next_states in enumerate(graph) ])
	])

print(parent_graph['parent'])
parent_graph['parent'] = union(parent_graph, (1, 2))
#print(parent_graph['parent'])
parent_graph['parent'] = union(parent_graph, (0, 1))
print(parent_graph['parent'])
parent_graph['parent'] = union(parent_graph, (2, 3))
print(parent_graph['parent'])
parent_graph['parent'] = union(parent_graph, (2, 4))
print(parent_graph['parent'])
parent_graph['parent'] = union(parent_graph, (1, 0))
print(parent_graph['parent'])

print(getTransitions(parent_graph, 1))