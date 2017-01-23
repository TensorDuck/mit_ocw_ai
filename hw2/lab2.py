# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = "False"

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = "False"

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = "True"

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = "True"

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = "True"

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = "False"

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
import copy

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

class data_node(object):
    def __init__(self, list_object, left_point=None, right_point=None):
        self.data = list_object
        self.left_point = left_point
        self.right_point = right_point

    def set_right_node(self, node_to_set):
        self.right_point = node_to_set

    def set_left_node(self, node_to_set):
        self.left_point = node_to_set

    def print_statement(self):
        print self.data.path
        print self.data.length

    def print_heuristic_statement(self, target):
        print self.data.path
        print self.data.heuristic(target)

class data_queue(object):
    def __init__(self, debug=False):
        self.beginning = None
        self.ending = None
        self.debug = debug

    def add_data_node(self, node_to_add):
        if (self.ending is None) and (self.beginning is None):
            # completely empty queue
            self.beginning = node_to_add
            self.ending = node_to_add
        else:
            self.ending.set_right_node(node_to_add)
            node_to_add.set_left_node(self.ending)
            self.ending = node_to_add

    def get_next(self):
        if self.beginning is None:
            return_node = None
            if self.debug:
                print "ERROR: QUEUE IS EMPTY, CANNOT RETRIEVE DATA"
        else:
            return_node = self.beginning
            self.beginning = self.beginning.right_point
            if not self.beginning is None:
                self.beginning.set_left_node(None)
            if self.beginning is None:
                self.ending = None
                if self.debug:
                    print "QUEUE IS EMPTY"
            return_node.set_right_node(None)

        return return_node

    def cull_to_size(self, N):
        if self.length <= N:
            pass
        else:
            current = self.beginning
            for i in range(N-1):
                current = current.right_point

            current.right_point.set_left_node(None)
            current.right_point = None

    def print_all(self):
        go = True
        current = self.beginning
        while go:
            if current is not None:
                current.print_statement()
                current = current.right_point
            else:
                go = False

    @property
    def length(self):
        go = True
        current = self.beginning
        if current is None:
            return 0
        else:
            count = 1
        while go:
            if current.right_point is None:
                go = False
            else:
                current = current.right_point
                count += 1
        return count



class data_sorted_queue(data_queue):
    "Queue is sorted so that smallest path lens come first"
    def __init__(self, debug=False, use_length=True, use_heuristic=False, target=None):
        super(data_sorted_queue, self).__init__()
        self.target = target
        self.use_length = use_length
        self.use_heuristic = use_heuristic
        if self.use_heuristic:
            assert not self.target is None

    def add_data_node(self, node_to_add):
        if (self.ending is None) and (self.beginning is None):
            # completely empty queue
            self.beginning = node_to_add
            self.ending = node_to_add

        else:
            # different part, search from back as new paths likely longer
            left_one = self.ending
            right_one = None
            go = True
            while go:
                left_value = 0
                new_value = 0
                if self.use_length:
                    left_value += left_one.data.length
                    new_value += node_to_add.data.length
                if self.use_heuristic:
                    left_value += left_one.data.heuristic(self.target)
                    new_value += node_to_add.data.heuristic(self.target)
                if left_value < new_value:
                    go = False
                else:
                    right_one = left_one
                    left_one = left_one.left_point
                if left_one is None:
                    go = False
            if left_one is None:
                self.beginning = node_to_add
            elif right_one is None:
                self.ending = node_to_add
            if not right_one is None:
                right_one.set_left_node(node_to_add)
            if not left_one is None:
                left_one.set_right_node(node_to_add)
            node_to_add.set_left_node(left_one)
            node_to_add.set_right_node(right_one)

    def print_all_heuristic(self, target):
            go = True
            current = self.beginning
            while go:
                if current is not None:
                    current.print_heuristic_statement(target)
                    current = current.right_point
                else:
                    go = False
class data_stack(object):
    def __init__(self, debug=False):
        self.beginning = None
        self.debug = debug

    def add_data_node(self, node_to_add):
        if (self.beginning is None):
            # completely empty queue
            self.beginning = node_to_add
        else:
            self.beginning.set_left_node(node_to_add)
            node_to_add.set_right_node(self.beginning)
            self.beginning = node_to_add

    def get_next(self):
        if self.beginning is None:
            return_node = None
            if self.debug:
                print "ERROR: QUEUE IS EMPTY, CANNOT RETRIEVE DATA"
        else:
            return_node = self.beginning
            self.beginning = self.beginning.right_point
            if not self.beginning is None:
                self.beginning.set_left_node(None)
            if self.beginning is None:
                if self.debug:
                    print "QUEUE IS EMPTY"
            return_node.set_right_node(None)

        return return_node

class path_list(object):
    def __init__(self, graph, path):
        self.graph = graph
        self.path = path
        if isinstance(path, list):
            size = len(path)
        else:
            raise IOError("ERROR: MUST INITIALIZE WITH A PATH LIST")

    def add_next_node(self, node):
        last = self.path[len(self.path)-1]
        if self.graph.are_connected(last, node):
            self.path.append(node)
        else:
            raise IOError("Given path is invalid, some nodes not connected")

    @property
    def length(self):
        if self.size > 1:
            length = 0
            for i in range(self.size-1):
                start = self.path[i]
                end = self.path[i+1]
                if self.graph.are_connected(start, end):
                    length += self.graph.get_edge(start, end).length
                else:
                    print self.path
                    raise IOError("Given path is invalid, some nodes not connected")
            return length
        else:
            return 0

    def heuristic(self, target):
        length = None
        if self.size > 0:
            length = self.graph.get_heuristic(self.path[self.last_idx], target)
        return length

    @property
    def size(self):
        return len(self.path)

    @property
    def last_idx(self):
        return len(self.path) - 1



def bfs(graph, start, goal, debug=False, optimal=False):
    best_path = None

    # initialize the queue
    queue = data_queue()
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    queue.add_data_node(this)
    next_up = queue.get_next()
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True

    # begin iterating
    while go:
        old_path_object = next_up.data #path_list object
        old_path = old_path_object.path #list of nodes forthe path
        next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
        for connection in next_connections:
            if connection == goal:
                if not optimal:
                    go = False
                next_path = copy.copy(old_path)
                next_path.append(connection)
                if not isinstance(next_path, list):
                    print next_path
                    raise Exception
                path_object = path_list(graph, next_path)
                if best_path is None:
                    best_path = path_object
                else:
                    if best_path.length > this.length:
                        best_path = path_object
            else:
                if not connection in old_path: #only do if no repeat
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    this = data_node(path_object)
                    queue.add_data_node(this)

        # check if next thing is empty. If so, terminate loop, else keep searching
        next_up = queue.get_next()
        if next_up is None:
            if debug:
                print "Ending the Loop"
            go = False

    if best_path is None:
        return []
    else:
        return best_path.path


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal, debug=False, optimal=False):
    best_path = None

    agenda = data_stack()
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    agenda.add_data_node(this)
    next_up = agenda.get_next()
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True

    while go:
        old_path_object = next_up.data #path_list object
        old_path = old_path_object.path #list of nodes forthe path
        next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
        for connection in next_connections:
            if connection == goal:
                if not optimal:
                    go = False
                next_path = copy.copy(old_path)
                next_path.append(connection)
                if not isinstance(next_path, list):
                    print next_path
                    raise Exception
                path_object = path_list(graph, next_path)
                if best_path is None:
                    best_path = path_object
                else:
                    if best_path.length > this.length:
                        best_path = path_object
            else:
                if not connection in old_path: #only do if no repeat
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    this = data_node(path_object)
                    agenda.add_data_node(this)

        # check if next thing is empty. If so, terminate loop, else keep searching
        next_up = agenda.get_next()
        if next_up is None:
            if debug:
                print "Ending the Loop"
            go = False

    if best_path is None:
        return []
    else:
        return best_path.path



## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal, debug=False, optimal=False):
    best_path = None

    agenda = data_stack()
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    agenda.add_data_node(this)
    next_up = agenda.get_next()
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True
    while go:
        old_path_object = next_up.data #path_list object
        old_path = old_path_object.path #list of nodes forthe path
        current_node = old_path[old_path_object.last_idx]
        next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
        # sort by heuristic, then add to the stack
        connections_h_list = []
        for connection in next_connections:
            connections_h_list.append(graph.get_heuristic(connection, goal))
        next_connections_unsorted = copy.copy(next_connections)
        connects_h_list_sorted = [] #sorted s.t. greatest values come first
        sorting = True
        while sorting:
            max_val = max(connections_h_list)
            for sort_idx, sort_val in enumerate(connections_h_list):
                if sort_val == max_val:
                    connects_h_list_sorted.append(next_connections[sort_idx])
                    del connections_h_list[sort_idx]
                    del next_connections[sort_idx]
                    break
            if len(connections_h_list) == 0:
                sorting = False
        assert len(connects_h_list_sorted) == len(next_connections_unsorted)
        for connection in connects_h_list_sorted:
            if connection == goal:
                if not optimal:
                    go = False
                next_path = copy.copy(old_path)
                next_path.append(connection)
                if not isinstance(next_path, list):
                    print next_path
                    raise Exception
                path_object = path_list(graph, next_path)
                if best_path is None:
                    best_path = path_object
                else:
                    if best_path.length > this.length:
                        best_path = path_object
            else:
                if not connection in old_path: #only do if no repeat
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    this = data_node(path_object)
                    agenda.add_data_node(this)

        # check if next thing is empty. If so, terminate loop, else keep searching
        next_up = agenda.get_next()
        if next_up is None:
            if debug:
                print "Ending the Loop"
            go = False

    if best_path is None:
        return []
    else:
        if graph.is_valid_path(best_path.path):
            return best_path.path
        else:
            raise Exception

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    best_path = None

    # initialize the queue
    queue = data_sorted_queue(use_length=False, use_heuristic=True, target=goal)
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    queue.add_data_node(this)
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True

    # begin iterating
    new_queue = queue
    while go:
        old_queue = new_queue
        new_queue = data_sorted_queue(use_length=False, use_heuristic=True, target=goal)
        next_up = old_queue.get_next()
        if next_up is None:
            inner_go = False
            go = False
        else:
            inner_go = True
        while inner_go:
            old_path_object = next_up.data #path_list object
            old_path = old_path_object.path #list of nodes forthe path
            next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
            for connection in next_connections:
                if connection == goal:
                    go = False
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    if best_path is None:
                        best_path = path_object
                    else:
                        if best_path.length > this.length:
                            best_path = path_object
                else:
                    if not connection in old_path: #only do if no repeat
                        next_path = copy.copy(old_path)
                        next_path.append(connection)
                        if not isinstance(next_path, list):
                            print next_path
                            raise Exception
                        path_object = path_list(graph, next_path)
                        this = data_node(path_object)
                        new_queue.add_data_node(this)
            # check if next thing is empty. If so, terminate loop, else keep searching
            next_up = old_queue.get_next()
            if next_up is None:
                inner_go = False
        # now remove connections from new_queue until you get to beam_width
        new_queue.cull_to_size(beam_width)
    if best_path is None:
        return []
    else:
        return best_path.path


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    pl = path_list(graph, node_names)
    return pl.length


def branch_and_bound(graph, start, goal):
    best_path = None

    agenda = data_sorted_queue()
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    agenda.add_data_node(this)
    next_up = agenda.get_next()
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True

    while go:
        old_path_object = next_up.data #path_list object
        old_path = old_path_object.path #list of nodes forthe path
        next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
        for connection in next_connections:
            if connection == goal:
                go = False
                next_path = copy.copy(old_path)
                next_path.append(connection)
                if not isinstance(next_path, list):
                    print next_path
                    raise Exception
                path_object = path_list(graph, next_path)
                if best_path is None:
                    best_path = path_object
                else:
                    if best_path.length > this.length:
                        best_path = path_object
            else:
                if not connection in old_path: #only do if no repeat
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    this = data_node(path_object)
                    agenda.add_data_node(this)

        # check if next thing is empty. If so, terminate loop, else keep searching
        next_up = agenda.get_next()
        if next_up is None:
            go = False

    if best_path is None:
        return []
    else:
        return best_path.path
def a_star(graph, start, goal):
    best_path = None
    extended_set = [start]
    agenda = data_sorted_queue(use_length=True, use_heuristic=True, target=goal)
    path_object = path_list(graph, [start])
    this = data_node(path_object)
    agenda.add_data_node(this)
    next_up = agenda.get_next()
    if start == goal:
        best_path = path_object
        go = False
    else:
        go = True

    while go:
        old_path_object = next_up.data #path_list object
        old_path = old_path_object.path #list of nodes forthe path
        current_node_to_see = old_path[old_path_object.last_idx]
        next_connections = graph.get_connected_nodes(old_path[old_path_object.last_idx])
        for connection in next_connections:
            if connection == goal:
                go = False
                next_path = copy.copy(old_path)
                next_path.append(connection)
                if not isinstance(next_path, list):
                    print next_path
                    raise Exception
                path_object = path_list(graph, next_path)
                if best_path is None:
                    best_path = path_object
                else:
                    if best_path.length > this.length:
                        best_path = path_object
            else:
                if not connection in extended_set:
                    #only do if not in extended_set
                    #checking if repeat in path is redundant
                    try:
                        assert graph.are_connected(old_path[-1],connection)
                    except:
                        print current_node_to_see
                        print old_path
                        print next_connections
                        print connection
                    extended_set.append(connection)
                    next_path = copy.copy(old_path)
                    next_path.append(connection)
                    if not isinstance(next_path, list):
                        print next_path
                        raise Exception
                    path_object = path_list(graph, next_path)
                    this = data_node(path_object)
                    agenda.add_data_node(this)

        # check if next thing is empty. If so, terminate loop, else keep searching
        next_up = agenda.get_next()
        if next_up is None:
            go = False

    if best_path is None:
        return []
    else:
        return best_path.path


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    admissable = True
    for node in graph.nodes:
        path = branch_and_bound(graph, node, goal)
        path_obj = path_list(graph, path)
        if path_obj.length < graph.get_heuristic(node, goal):
            admissable = False
            break
    return admissable

def is_consistent(graph, goal):
    consistent = True
    found_edges = False
    for edge in graph.edges:
        found_edges = True
        h1 = graph.get_heuristic(edge.node1, goal)
        h2 = graph.get_heuristic(edge.node2, goal)
        diff = h1-h2
        if diff < 0:
            diff *= -1.
        if diff > edge.length:
            consistent = False
            break
    if not found_edges:
        print "No edges found"
    return consistent

HOW_MANY_HOURS_THIS_PSET_TOOK = 'far too many'
WHAT_I_FOUND_INTERESTING = 'designing queue and stack classes, making sorted queue, how everything relates'
WHAT_I_FOUND_BORING = 'very tedious amounts of implementation. Very repetetive at some point'
