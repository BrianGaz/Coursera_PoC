"""
Monte Carlo Tic-Tac-Toe Player
"""
    
import random
import poc_ttt_gui
import poc_ttt_provided as provided
    
# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    while board.check_win() == None:
        row = random.randrange(board.get_dim())
        col = random.randrange(board.get_dim())
        while board.square(row, col) != provided.EMPTY:
            row = random.randrange(board.get_dim())
            col = random.randrange(board.get_dim())
        board.move(row, col, player)
        player = provided.switch_player(player)
    
def mc_update_scores(scores, board, player):
        mc_trial(board, player)
        if board.check_win() == player:
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    if board.square(row, col) == player:
                        scores[row][col] += 1
                    elif board.square(row, col) == provided.switch_player(player):
                        scores[row][col] -= 1
                    else:
                        scores[row][col] += 0
        elif board.check_win() == provided.switch_player(player):
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    if board.square(row, col) == player:
                        scores[row][col] -= 1
                    elif board.square(row, col) == provided.switch_player(player):
                        scores[row][col] += 1
                    else:
                        scores[row][col] += 0
    
def get_best_move(board, scores):
    empty_squares = board.get_empty_squares()
    scores_list = []
    scores_coord = {}
    final_coords = []
    
    if empty_squares == []:
        return "No moves"
    
    for row,col in empty_squares:
        score = scores[row][col]
        scores_list.append(score)
        scores_coord[(row,col)] = score
    
    top_score = max(scores_list)
    for coord,score in scores_coord.items():
        if score == top_score:
            final_coords.append(coord)
    
    return random.choice(final_coords)
    
def mc_move(board, player, trials):
    global NTRIALS
    NTRIALS = trials
    scores = [[0 for i in range(board.get_dim())]
            for i in range(board.get_dim())]
    for i in range(NTRIALS):
        mc_update_scores(scores, board, player)
    return tuple(get_best_move(board, scores))
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
    
#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)