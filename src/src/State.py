import readBoard as rb
import copy

class State():

	def __init__(self, board, path, fourSpawned, probability, EV):
		self.board = board
		self.path = path
		self.fourSpawned = fourSpawned
		self.probability = probability
		self.EV = EV

	#Move the tile at (i1,j1) into the position of (i2,j2) and combine the tiles
	def combine(self,i1,j1,i2,j2):
		self.board[i2][j2] = self.board[i2][j2] * 2
		self.board[i1][j1] = ' '

	#Takes the board and the position of a tile as inputs and move the tile up by 1
	def moveUp(self, i,j):
		self.board[i-1][j] = self.board[i][j]
		self.board[i][j] = ' '

		#If the tile we just moved up still has an empty space above, call moveUp again
		if ((not i == 1) and self.board[i-2][j] == ' '):
			self.moveUp(i-1, j)
		#If the tile is moving into and equal tile, combine them
		#Don't check if the tile was moved to the edge of the board
		elif i-2 >= 0 and self.board[i-1][j] == self.board[i-2][j]:
			self.combine(i-1,j,i-2,j)

	def moveRight(self, i, j):
		self.board[i][j+1] = self.board[i][j]
		self.board[i][j] = ' '

		if ((not j == 2) and self.board[i][j+2] == ' '):
			self.moveRight(i, j+1)
		elif j + 2 <= 3 and self.board[i][j+1] == self.board[i][j+2]:
			self.combine(i, j+1, i, j+2)

	def moveDown(self, i,j):
		self.board[i+1][j] = self.board[i][j]
		self.board[i][j] = ' '

		if ((not i == 2) and self.board[i+2][j] == ' '):
			self.moveDown(i+1, j)
		elif i+2 <= 3 and self.board[i+1][j] == self.board[i+2][j]:
			self.combine(i+1,j,i+2,j)

	def moveLeft(self, i, j):
		self.board[i][j-1] = self.board[i][j]
		self.board[i][j] = ' '

		if ((not j == 1) and self.board[i][j-2] == ' '):
			self.moveLeft(i, j-1)
		elif j - 2 <= 3 and self.board[i][j-1] == self.board[i][j-2]:
			self.combine(i, j-1, i, j-2)
			
	def move(self,direction):
	
		if direction == 'up':
			#Loop throught each tile, except the top row which cannot move up
			for i in range(1,4):
				for j in range(4):
	
					if not self.board[i][j] == ' ':
						#If the tile above is equal to the tile being moved, combine the 2
						if self.board[i][j] == self.board[i-1][j]:
							self.combine(i,j,i-1,j)
	
						#If the tile above is a blank, move the current tile up
						elif self.board[i-1][j] == ' ':
							self.moveUp(i, j)
	
		#Repeat the same for the case of other directions
		elif direction == 'right':
			for j in range(2,-1,-1):
				for i in range(4):
	
					if not self.board[i][j] == ' ':
						if self.board[i][j] == self.board[i][j+1]:
							self.combine(i,j,i,j+1)
						elif self.board[i][j+1] == ' ':
							self.moveRight(i, j)
	
		elif direction == 'down':
			for i in range(2,-1,-1):
				for j in range(4):
					
					if not self.board[i][j] == ' ':
						if self.board[i][j] == self.board[i+1][j]:
							self.combine(i,j,i+1,j)																		
						elif self.board[i+1][j] == ' ':
							self.moveDown(i, j)
	
		elif direction == 'left':
			for j in range(1,4):
				for i in range(4):
	
					if not self.board[i][j] == ' ':
						if self.board[i][j] == self.board[i][j-1]:
							self.combine(i,j,i,j-1)
						elif self.board[i][j-1] == ' ':
							self.moveLeft(i, j)
		else:
			sys.exit("Invalid move direction")	
		
	#Returns all possible child states of the current state, as as result of
	#moving the 4 directions, and for each direction all the possible tile spawnings
	def getChildren(self):
		children = []
		
		directions = ['up', 'right', 'left', 'down']
		
		#Find all the possibilities 
		for direction in directions:
			#Reset tmpState back to the current state for each child and perform the move
			tmpState = copy.deepcopy(self)
			tmpState.move(direction)
			
			#If the move does not change anything, there is no point considering it
			if tmpState.board != self.board:
				#Add the direction we moved to get to this state to the path
				tmpState.path += direction[0]			
						
				children.append(tmpState)
								
		return children
			
if __name__ == '__main__':
	
	currentBoard = State(rb.readBoard(),'',False, 0, 0)
	
	currentBoard.move('left')
	
	for i in range(4):
		for j in range(4):
			print(currentBoard.board[i][j], end = ' ')

		print("\n")