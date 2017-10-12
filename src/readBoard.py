import pyscreenshot as ss
import pyautogui as gui
from PIL import Image
import sys

def evaluateSquare(squareHexValue):
	#Return the numeric value of the square
	
	return {
	    '#eee4da': 2,
	    '#ede0c8': 4,
	    '#f2b179': 8,
	    '#f59563': 16,
	    '#f67c5f': 32,
	    '#f65e3b': 64,
	    '#edcf72': 128,
	    '#edcc61': 256,
	    '#edc850': 512,
	    '#edc53f': 1024,
	    '#edc22e': 2048,
	    '#cdc1b4': ' ',
	    '#cdc0b4': ' ',
	    '#cdc1b3': ' ',
	    '#cdc1b2': ' ',
	    '#cec2b3': ' ',
	    '#cec1b3': ' ',
	    '#cec1b2': ' '
	}.get(squareHexValue)


def readBoard():
	#Click away from the python prompt to 2048 so the correct window is read and commands can be executed
	gui.click(100,300)

	#List which will store the contents of the board
	board = [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]

	boardScreenShot = ss.grab(bbox=(717, 355, 1186, 824))
	
	#Loop through each of the 16 squares, take one pixil from each and
	#find the value based on it's hex value
	#Then fill the board with the corrisponding value
	for y in range(4):
		for x in range(4):
			
			pixel = boardScreenShot.copy()
			
			#Grab a pixel from the tile
			x1 = 13 + (x * 121)
			y1 = 10 + (y * 121)
			x2 = 14 + (x * 121)
			y2 = 11 + (y * 121)
			pixel = pixel.crop((x1,y1,x2,y2))
			
			#Get the RGB of the colour
			colours = list(pixel.getdata())
			
			#Convert this RGB value to a html type hex colour
			hexVal = '#{:02x}{:02x}{:02x}'.format(colours[0][0], colours[0][1], colours[0][2])
			
			#print("Current hexVal: {}".format(hexVal))
			
			value = evaluateSquare(hexVal)
			#print("Value: {}".format(value))
			
			if value is None:
				sys.exit("Tiles could not be read")
			
			board[y][x] = value
			
	return board
