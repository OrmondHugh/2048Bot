import readBoard as rb
import pyautogui as gui
import copy
import State
import utility

import time

#Struct storing the path to a random node and the requency at which it occurs as a child
class pathStruct():
	def __init__(self, path, freq):
		self.path = path
		self.freq = freq

def search(state, depth):
	
	depth = depth + 1
	
	#Base Case
	#Once we have gone as deep as we are intending, return the bottom node's expected value
	if depth == 4:
		
		state.EV = utility.getExpectedValue(state, utility.getPossibilities(state))

		return state

	else:
		children = state.getChildren()
		
		#Assign the state to be returned to the first child by default
		try:
			returnState = copy.deepcopy(children[0])
		#If the state has no children, simply return the state
		except IndexError:
			return state
		
		returnState.EV = 0
		
		#Loop through the four possible moves
		for child in children:
			util = utility.getUtility(child.board, state.board)
			
			if util > 125:
				return child
			elif util < 55:
				continue
			
			possibilities = utility.getPossibilities(child)
			
			child.EV = utility.getExpectedValue(child, possibilities)
			
			#String to store the path we will return
			tmpPath = ''
			
			#List of pathStructs for finding the most common optimal path from the possibilites
			#ie the most likely path we should take
			possibilityPaths = []
			
			
			for possibility in possibilities:
				tmpState = copy.deepcopy(search(possibility, depth))
					
				#Count up the path we should follow for each possibility
				for p in possibilityPaths:
					if p.path == tmpState.path:
						p.freq += tmpState.probability
					else:
						tmpStruct = pathStruct(tmpState.path, 1)
						possibilityPaths.append(tmpStruct)
						
				if len(possibilityPaths) == 0:
					tmpStruct = pathStruct(tmpState.path, 1)
					possibilityPaths.append(tmpStruct)					
			
			#Find which path is the most likely
			tmpStruct = pathStruct('', -1)
			for p in possibilityPaths:
				if p.freq > tmpStruct.freq:
					tmpStruct = copy.deepcopy(p)			
					
			#Assign that path to the child we are checking
			child.path = tmpStruct.path
			
			#Average out the EVs of the possible states
			try:
				
				#If we must pass through a bad state to get to the end state, lower the end state's EV
				if util < 50:
					child.EV = child.EV / util
			
				if child.EV > returnState.EV:
					returnState = copy.deepcopy(child)
			#If there are no possibilities we can leave the EV at 0
			except ZeroDivisionError:
				pass
			
		return returnState
		

def performMove(state):

	for letter in state.path:
		if letter == 'u':
			gui.typewrite(['up'])
		elif letter == 'r':
			gui.typewrite(['right'])
		elif letter == 'd':
			gui.typewrite(['down'])
		elif letter == 'l':
			gui.typewrite(['left'])
			
if __name__ == '__main__':

	while(True):

		startTime = time.time()
		
		currentBoard = State.State(rb.readBoard(), '', False, 0, 0)

		#Amount of turns/layers of nodes deep we are
		depth = 0

		endState = search(currentBoard, depth)
		
		print("Preforming move with EV {0} and path of {1}".format(endState.EV, endState.path))
		performMove(endState)
		
		print("Move took %s seconds" % (time.time() - startTime))
