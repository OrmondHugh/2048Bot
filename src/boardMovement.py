import readBoard

#Move the tile at (i1,j1) into the position of (i2,j2) and combine the tiles
def combine(board,i1,j1,i2,j2):
	testBoard[i2][j2] = testBoard[i2][j2] * 2
	testBoard[i1][j1] = ' '	

#Takes the board and the position of a tile as inputs and move the tile up by 1
def moveUp(board, i,j):
	board[i-1][j] = board[i][j]
	board[i][j] = ' '
	
	#If the tile we just moved up still has an empty space above, call moveUp again
	if ((not i == 1) and board[i-2][j] == ' '):
		moveUp(board, i-1, j)
	#If the tile is moving into and equal tile, combine them
	#Don't check if the tile was moved to the edge of the board
	elif i >= 2 and board[i-1][j] == board[i-2][j]:
		combine(board, i-1,j,i-2,j)

def moveRight(board, i, j):
	board[i][j+1] = board[i][j]
	board[i][j] = ' '
	
	if ((not j == 2) and board[i][j+2] == ' '):
		moveRight(board, i, j+1)
	elif j <= 1 and board[i][j+1] == board[i][j+2]:
		combine(board, i, j+1, i, j+2)

def moveDown(board, i,j):
	board[i+1][j] = board[i][j]
	board[i][j] = ' '

	if ((not i == 2) and board[i+2][j] == ' '):
		moveDown(board, i+1, j)
	elif i <= 1 and board[i+1][j] == board[i+2][j]:
		combine(board, i+1,j,i+2,j)
		
def moveLeft(board, i, j):
	board[i][j-1] = board[i][j]
	board[i][j] = ' '

	if ((not j == 1) and board[i][j-2] == ' '):
		moveLeft(board, i, j-1)
	elif j <= 5 and board[i][j-1] == board[i][j-2]:
		combine(board, i, j-1, i, j-2)
		
		
def move(direction):

	if direction == 'up':
		#Loop throught each tile, except the top row which cannot move up
		for i in range(1,4):
			for j in range(4):
				
				if not testBoard[i][j] == ' ':
					#If the tile above is equal to the tile being moved, combine the 2
					if testBoard[i][j] == testBoard[i-1][j]:
						combine(testBoard,i,j,i-1,j)
																		
					#If the tile above is a blank, move the current tile up
					elif testBoard[i-1][j] == ' ':
						moveUp(testBoard, i, j)
						
	elif direction == 'right':
		for j in range(2,-1,-1):
			for i in range(4):
				
				if not testBoard[i][j] == ' ':
					if testBoard[i][j] == testBoard[i][j+1]:
						combine(testBoard, i,j,i,j+1)
					elif testBoard[i][j+1] == ' ':
						moveRight(testBoard, i, j)
						
	elif direction == 'down':
		for i in range(2,-1,-1):
			for j in range(4):
				print("i,j: ",i,',',j)
				if not testBoard[i][j] == ' ':
					if testBoard[i][j] == testBoard[i+1][j]:
						combine(testBoard,i,j,i+1,j)																		
					elif testBoard[i+1][j] == ' ':
						moveDown(testBoard, i, j)
	
	elif direction == 'left':
		for j in range(1,4):
			for i in range(4):

				if not testBoard[i][j] == ' ':
					if testBoard[i][j] == testBoard[i][j-1]:
						combine(testBoard, i,j,i,j-1)
					elif testBoard[i][j-1] == ' ':
						moveLeft(testBoard, i, j)
	else:
		sys.exit("Invalid move direction")
