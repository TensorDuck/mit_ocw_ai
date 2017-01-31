# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
##
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost

    my idea:
    2 points - for every two-link chain
    3 points - for every three-link chain
    1000 points - for every 4-link chain

    Take difference between current player and opponent
    """
    # search for one points:
    current_player = board.get_current_player_id()
    other_player = board.get_other_player_id()

    if board.longest_chain(current_player) == 4:
        return 1000
    if board.longest_chain(other_player) == 4:
        return -1000

    total = 0
    # for current player
    for sets in board.chain_cells(current_player):
        for chain in sets:
            total += len(chain) ** 2
    for chain in list(board.chain_cells(other_player)):
        for chain in sets:
            total -= len(chain) ** 2

    return total





## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)
#run_game(human_player, quick_to_win_player)
## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_find_value(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, max_lvl):
    best_val = None
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    for move, new_board in get_next_moves_fn(board):
        val = -1 * alpha_beta_find_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn, alpha, beta, not max_lvl)
        #print "depth: %d, val: %d" % (depth,val)
        if best_val == None or val > best_val:
            best_val = val
        if max_lvl:
            alpha = best_val
        else:
            beta = best_val

        try:
            if (alpha is None) or (beta is None):
                #has not yet found both bounds, so anything goes!
                pass
            elif alpha + beta >= 0:
                #if alpha is maximum score assured
                #-beta is minimum score assured
                #Break if the minimum score assured is less than max assured score
                break
        except:
            print alpha
            print beta
            raise


    return best_val

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal, verbose=True):
    best_val = None
    alpha = None
    beta = None
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alpha_beta_find_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn, alpha, beta, False)

        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)
            alpha = best_val[0]
        #print "ab Possible Move: %d with rating %d" % (move, val)
    if verbose:
        try:
            print "AlphaBeta: Decided on column %d with rating %d" % (best_val[1], best_val[0])
        except:
            print "AlphaBeta, Column:"
            print best_val[1]
            print "AlphaBeta, Rating:"
            print best_val[0]

    return best_val[1]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)
#board = ConnectFourBoard()
#board.do_move(0)
#minimax(board, 4, focused_evaluate)
#alpha_beta_search(board, 4, focused_evaluate)


## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def check_free(board, chain):
    #checks if there is open space around
    if len(chain) == 1:
        return 0

    if len(chain) == 2:
        vector_x = chain[0][0] - chain[1][0]
        vector_y = chain[0][1] - chain[1][0]
        check = [True, True, True, True]
        check_idxs = []
        for i in range(-2,0):
            check_idxs.append((chain[0][0] + (i*vector_x), chain[0][1] + (i*vector_y)))
        for i in range(1,3):
            check_idxs.append((chain[1][0] + (i*vector_x), chain[1][1] + (i*vector_y)))
        for i in range(4):
            x_idx = check_idxs[i][0]
            y_idx = check_idxs[i][1]
            if x_idx < 0 or x_idx > 5 or y_idx < 0 or y_idx > 6:
                check[i] = False
            else:
                if board.get_cell(x_idx, y_idx) != 0:
                    check[i] == False
        use = []
        for i in range(3):
            use.append(check[i] and check[i+1])
        if True in use:
            return 2
        else:
            return 0

    if len(chain) == 3:
        vector_x = chain[0][0] - chain[1][0]
        vector_y = chain[0][1] - chain[1][0]
        check = [True, True]
        check_idxs = []
        check_idxs.append((chain[2][0] + vector_x, chain[2][1] + vector_y))
        check_idxs.append((chain[0][0] - vector_x, chain[0][1] - vector_y))
        for i in range(2):
            x_idx = check_idxs[i][0]
            y_idx = check_idxs[i][1]
            if x_idx < 0 or x_idx > 5 or y_idx < 0 or y_idx > 6:
                check[i] = False
            else:
                if board.get_cell(x_idx, y_idx) != 0:
                    check[i] == False
        if True in check:
            return 3
        else:
            return 0

    return 0


def better_evaluate(board):
    current_player = board.get_current_player_id()
    other_player = board.get_other_player_id()

    if board.longest_chain(current_player) == 4:
        return 1000
    if board.longest_chain(other_player) == 4:
        return -1000

    total = 0
    # for current player
    for chain in list(board.chain_cells(current_player)):
        chain_length = check_free(board, chain)
        if chain_length == 3:
            total += 100
        total += chain_length

    for chain in list(board.chain_cells(other_player)):
        chain_length = check_free(board, chain)
        if chain_length == 3:
            total -= 100
        total -= chain_length
    # ensure you don't override winning or losing
    if total >= 1000:
        total = 999
    if total <= -1000:
        total = -999
    return total

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])

def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True) # if only I could :(

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "Not Many At All"
WHAT_I_FOUND_INTERESTING = "It was fun to come up with scoring algorithms"
WHAT_I_FOUND_BORING = "Nothing, this one was short and sweet"
NAME = "Justin"
EMAIL = "wouldn't you like to know"
