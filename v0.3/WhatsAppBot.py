import time
import pyautogui
import pytesseract
from PIL import Image, ImageDraw

DEBUG = False

def WhatsAppPrint(text):
	if DEBUG :
		print text
	else :
		pyautogui.typewrite(text + str("\n"), interval=0.1)

#Initialization of the Bot
botAlive = True
receivedMessageLeftBottom = (500, 680)		#heavily depends on screen resolution and window size, 
sendMessageRightBottom = (1260, 680)		#should make a function to allow you pointing with the mouse where this coordinates are

pyautogui.alert('After clicking on OK you will have 2 sec to give the focus to the WhatsApp window.')
time.sleep(2)

#Functions --put in a separate file if this gets big
def readMessage():
	global receivedMessageLeftBottom, sendMessageRightBottom
	
	if DEBUG :
		screen = Image.open("2.png")
	else :
		screen = pyautogui.screenshot()
		screen.save("debug.png")
	
	if screen.getpixel(receivedMessageLeftBottom) == (255, 255, 255):	#the last message is a received message
		messageBox = findMessageSize(receivedMessageLeftBottom, screen)
	elif screen.getpixel(sendMessageRightBottom) == (220, 248, 198):		#the last message is a send message
		messageBox = findMessageSize(sendMessageRightBottom, screen)
	else:
		print "An error happend: unable to find the last message on the screenshot"
		print screen.getpixel(receivedMessageLeftBottom)
		print screen.getpixel(sendMessageRightBottom)
	latestMessage = screen.crop(messageBox)
	draw = ImageDraw.Draw(latestMessage)
	x0, y0, x1, y1 = messageBox
	colour = screen.getpixel((x0 + 7, y0 + 7))
	draw.rectangle([x1 - x0 - 55, y1 - y0 - 20, x1 - x0, y1 - y0],fill = colour)
	del draw
	sizeX, sizeY = latestMessage.size
	latestMessageResized = latestMessage.resize((sizeX*4, sizeY*4), Image.BICUBIC)    
	if DEBUG :
		latestMessage.save("message.png")
		print pytesseract.image_to_string(latestMessageResized, config='-psm 6')
	return pytesseract.image_to_string(latestMessageResized, config='-psm 6')

def findMessageSize(xy, screen):
	x, y = xy
	colour = screen.getpixel((x, y))
	if colour == (255, 255, 255):		#different direction if it is a send or received message
		inc = 1
	else :
		inc = -1
	i = x
	while screen.getpixel((i, y)) == colour:
		i += inc
	j = y
	while screen.getpixel((x, j)) == colour:
		j -= 1
	if colour == (255, 255, 255):
		return (x, j + 25, i, y)	#+25 to suppress name and number
	else:
		return (i, j, x, y)

#Main loop of the bot
oldText = readMessage()
while botAlive:
	text = readMessage()
	if text != oldText:
		WhatsAppPrint(text)
	oldText = text
	time.sleep(1)

print "Bot exited without error"

