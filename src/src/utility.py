import readBoard as rb
import State
import copy

def getPossibilities(state):

	possibilities = []
	
	#Loop through each tile to find the spaces that can be filled by a spawning tile
	for i in range(4):
		for j in range(4):
			#If we find an empty space, add a child to children where a two is spawned, and a child where a four is spawned
			if state.board[i][i] == ' ':
				for value in range(2,5,2):
					child = copy.deepcopy(state)
					if value == 4:
						child.fourSpawned == True
					child.board[i][j] = value

					possibilities.append(child)
	
	#Assign the probability of each state occuring to it's object			
	for node in possibilities:
		if node.fourSpawned:
			node.probability = 0.1 / len(possibilities)
			
		else:
			node.probability = 0.9 / len(possibilities)
		
	return possibilities

def getUtility(board, parentBoard):
	utility = 0

	#Count the empty spaces
	emptySpacesCount = 0
	for i in range(4):
		for j in range(4):
			if board[i][j] == ' ':
				emptySpacesCount = emptySpacesCount + 1

	#A full board is very likely to either be a losing state, or be close to one
	if emptySpacesCount == 0:
		return 0

	#50 of the total utility is allocated to how clear the board is.
	#A full 50 is awarded if there is at least 7 clear squares, if there are less utilitly
	#is added based on how much of the board is clear
	if emptySpacesCount == 0:
		return 0
	elif emptySpacesCount >= 7:
		utility = utility + 60.0
	else:
		utility = utility + 60.0*(emptySpacesCount/7)


	#Find the biggest tile. If it is in the top right, add 0.3 to utility
	biggest =  0
	for i in range(4):
		for j in range(4):
			if board[i][j] != ' ' and board[i][j] > biggest:
				biggest = board[i][j]

	if board[0][3] == biggest:
		utility = utility + 40.0
		#If we also have a full top line of different values, add more utility
		if board[0][2] != ' 'and board[0][2] != board[0][3]:
			utility = utility + 10.0
			if board[0][1] != ' 'and board[0][1] != board[0][2]:
				utility = utility + 10.0
				if board[0][0] != ' 'and board[0][0] != board[0][1]:
					utility = utility + 10.0
			#Give utility for making the main tiles at the top bigger
			if board[0][3] == parentBoard[0][3] * 2:
				utility = utility + 35.0
			if board[0][2] == parentBoard[0][2] * 2:
				utility = utility + 30.0
			if board[0][1] != ' ' and board[0][1] == parentBoard[0][1] * 2:
				utility = utility + 25.0
			if board[0][0] != ' ' and board[0][0] == parentBoard[0][0] * 2:
				utility = utility + 15.0
				
				
	
	return utility

def getExpectedValue(state, possibilities):
	EV = 0
	
	for child in possibilities:
		
		EV = EV + (child.probability * getUtility(child.board, state.board))
				
	return EV


if __name__ == '__main__':
	
	currentBoard = State.State(rb.readBoard(), '', False, 0, 0)
	
	children = currentBoard.getChildren()
	
	for child in children:
		child.EV = getExpectedValue(child)
	
		print("Direction: ", child.path)
		print("Utility: ", child.EV)