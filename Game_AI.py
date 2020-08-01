import sys
from random import randint

red =  1
blue = 2
green = 3
colors = [1,2,3]

def static_value_state(board, color, x, y, z ):      #scoring system
	number_positions = len(available_possible_position_simple(board, color, x, y, z))   # need to review to function to determine the good syntax
	leaf_score = 3 * number_positions
	return leaf_score


def move_format(last_move):			# changing the last move into a usable format
	parse_last_move = last_move.split(",")
	color = int(parse_last_move[0][1]) #get rid of "("
	x = int(parse_last_move[1])
	y = int(parse_last_move[2])
	z = int(parse_last_move[3][0]) # get rid of ")"	
	return (color, x, y, z)


def game_over(board):
	size = len(board)
	for x in range(0, size):
		size_row = len(board[x])
		for y in range(0, size_row):	
			if( board[x][y] == 0):
				return False
	return True


def game_over(board, color, x, y, z ):		#check if the last player lost the game because he has formed a triangle of different colors
	if board[x][y-1] != color and board[x-1][y] != color and board[x][y-1] != board[x-1][y]:
		return True
	elif board[x][y-1] != color and board[x+1][y-1] != color and  board[x][y-1] != board[x+1][y-1]: 
		return True
	elif board[x+1][y-1] != color and board[x+1][y] != color and board[x+1][y-1] != board[x+1][y]: 
		return True
	elif board[x+1][y] != color and board[x][y+1] != color and board[x+1][y] != board[x][y+1]:
		return True
	elif board[x][y+1] != color and board[x-1][y+1] != color and board[x][y+1] != board[x][y+1]: 
		return True
	else:
		return False

def available_possible_position_simple(board, color, x , y, z):   #generate a list of random position without the color associated to it.
	possible_moves = []
	move_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y],[x+1,y-1],[x-1,y+1]]
	# check all adjacent possibilities
	for i in range(len(move_list)):
		move_set = move_list[i]
		x_move = move_set[0]
		y_move = move_set[1]
		z_move = len(board[x_move]) - y_move - 1
		if is_valid(board, x_move, y_move, z_move):
			possible_moves.append((x_move, y_move, z_move))
	
	return possible_moves

def available_possible_position(board, last_move):   #generate a list of random position without the color associated to it.
	color, x, y, z = move_format(last_move)
	possible_moves = []
	move_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y],[x+1,y-1],[x-1,y+1]]
	# check all adjacent possibilities
	for i in range(len(move_list)):
		move_set = move_list[i]
		x_move = move_set[0]
		y_move = move_set[1]
		z_move = len(board[x_move]) - y_move - 1
		if is_valid(board, x_move, y_move, z_move):
			possible_moves.append((x_move, y_move, z_move))
	
	return possible_moves

def best_move(board, last_move):
	bestval = -1000
	best_complete_move = [0,0,0,0]  # move with color
	possible_moves = available_possible_position(board, last_move)
	out(possible_moves)         # check out of bound
	
	for move in possible_moves:  	# going through all the possible moves
		for color in colors:
			x , y , z = move
			place_move(board, color, x, y, z)
			move_score = minimax(board, color, x, y, z,  0 , False, -1000, 1000 )
			delete_move(board, color, x, y, z)
			if( move_score > bestval):
				best_complete_move = [color, x, y, z]
				bestval = move_score
	return best_complete_move


def minimax( board, color, x, y , z, depth , who_is_playing, alpha, beta ):
	if depth == 3 or game_over(board, color, x, y, z) == True:
		return static_value_state(board, color, x, y, z)

	if who_is_playing == True:
		best = -1000
		possible_moves = available_possible_position(board, last_move)

		for move in possible_moves:  	# going through all the possible moves
			for color in colors:
				x , y , z = move
				place_move(board, color, x, y, z)
				actual_score_M = minimax(board, color, x , y , z,  depth+1, False, alpha, beta)
				best = max(best, actual_score_M)
				alpha = max(alpha, best)
				delete_move(board, color, x, y, z)
				if beta <= alpha:
					break
			if beta <= alpha:
					break
		return best 
	elif who_is_playing == False :
		best = 1000
		possible_moves = available_possible_position(board, last_move)
		for move in possible_moves:  	# going through all the possible moves
			for color in colors:
				x , y , z = move
				place_move(board, color, x, y, z)
				actual_score_m = minimax(board, color, x , y , z,  depth+1, False, alpha, beta)
				best = min(best, actual_score_m)
				alpha = min(beta, best)
				delete_move(board, color, x, y, z)
				if beta <= alpha:
					break
			if beta <= alpha:
					break
		return best 

#intelligently choose a move
def choose_move(board, last_move):
	color, x_possibility, y_possibility, z_possibility = 0,0,0,0
	# board is empty, choose a random spot on the board
	if last_move == "null":
		color, x_possibility, y_possibility, z_possibility = generate_random_move(board, last_move)
	else:
		color, x_possibility, y_possibility, z_possibility = best_move(board, last_move)

	choice = "(" + str(color) + "," + str(x_possibility) + "," + str(y_possibility) + "," + str(z_possibility) + ")"
	return choice


# randomly generate moves on the board
def generate_random_move(board, last_move):
	x_possibility = randint(1, len(board)-2) # can't place at x = 0, and can't place at x = full height
	width = len(board[x_possibility])		 # get width of board at x, aka y_max
	y_possibility = randint(1, width-2)		 # generate random y_possibility at height = x
	color = randint(1,3)					 # generate random color to place down
	z_possibility = width - y_possibility - 1 # z value should just be width - y_possibility
	return (color, x_possibility, y_possibility, z_possibility)

def is_valid(board, x, y, z):
	thing = str(x) + "," + str(y) + "," + str(z)
	# check board at (x, y, z) is empty or not
	size = len(board[1]) - 2
	boundary = size + 2

	# check if position is in the playable region
	if x + y + z > boundary:
		return False

	# check if position is empty
	if board[x][y] != 0:
		return False

	return True

def place_move(board,c,x,y,z):
	board[x][y] = c

def delete_move(board, c, x, y, z):
	board[x][y] = 0

msg = "Given board " + sys.argv[1] + "\n" #Get input
board = msg.split("L")[0] #Get the board as a raw string
board = [[int(x) for x in list(line[:-1])] for line in board.split("[")[1:]] #Convert to a list of lists of ints
board = list(reversed(board)) #reverse the board
last_move = msg[12:].split("L")[1][8:-1] #Parse out last move
#perform intelligent search to determine the next move
chosen_move = choose_move(board, last_move)
#print to stdout for AtroposGame
sys.stdout.write(chosen_move);
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.
