from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def iterate_over_constraints(state, all_constrained, current_variable, current_value):
    # iterate over a list of constraints, where the ith is the current variable
    # then return False if something fails, and if all suceeds, return True
    # Also return a list of variables checked
    list_of_variables_checked = []
    for the_constraint in all_constrained:
        #first determine which one is the one we need to check
        variable_check_name = the_constraint.get_variable_j_name()
        #  assertion checks to make sure
        assert current_variable.get_name() != variable_check_name
        assert the_constraint.get_variable_i_name() == current_variable.get_name()
        check_variable = state.get_variable_by_name(variable_check_name)
        list_of_variables_checked.append(check_variable)
        #make list of all values to remove
        remove_value = []
        for value in check_variable.get_domain():
            if not the_constraint.check(state, value_i=current_value, value_j=value):
                remove_value.append(value)
        for value in remove_value: # remove values now
            check_variable.reduce_domain(value)
        if check_variable.domain_size() == 0:
            return False, list_of_variables_checked
    return True, list_of_variables_checked

def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.

    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    current_variable = state.get_current_variable()
    if current_variable is None:
        return True
    assert current_variable.is_assigned()
    current_value = current_variable.get_assigned_value() # get current value
    all_constrained = state.get_constraints_by_name(current_variable.get_name()) #the i-th state is always the current state
    result, list_of_variables_checked = iterate_over_constraints(state, all_constrained, current_variable, current_value)
    if not result:
        return result

    return True

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    current_variable = state.get_current_variable()
    if current_variable is None:
        return True
    assert current_variable.is_assigned()
    singleton_queue = [] #
    singleton_visited_name_list = [] # stirng for easy comparison
    #just check the ones that are potentially modified
    singleton_queue.append(current_variable)
    go = True
    current_idx = 0
    while go: # my really bad list
        singleton_variable = singleton_queue[current_idx]
        singleton_visited_name_list.append(singleton_variable.get_name())
        if singleton_variable.is_assigned():
            singleton_value = singleton_variable.get_assigned_value()
        else:
            singleton_value = singleton_variable.get_domain()[0] # not yet assigned
        all_constrained = state.get_constraints_by_name(singleton_variable.get_name()) #the i-th state is always the current state
        result, list_of_variables_checked = iterate_over_constraints(state, all_constrained, singleton_variable, singleton_value)
        if not result: # if result is False, return False immediately
            return result
        # if here, result was True, so no failure yet
        # check for list of singletons, and add if not already visited
        for var in list_of_variables_checked:
            if (not var.is_assigned()) and var.domain_size() == 1:
                if not var.get_name() in singleton_visited_name_list:
                    # add to the queue
                    singleton_queue.append(var)

        # see if we have reached the end of the queue
        current_idx += 1
        if current_idx >= len(singleton_queue):
            go = False
    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    return hamming_distance(list1, list2)

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    return homogeneous_disorder(yes, no)

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 10
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 10
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 10
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn
