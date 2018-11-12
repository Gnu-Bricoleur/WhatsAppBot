import time
import pyautogui
import pytesseract

botAlive = True
receivedMessagePosition = (500, 655, 600, 680)
sendMessagePosition = (1160, 655, 1210, 680)

pyautogui.alert('After clicking on OK you will have 5 sec to give the focus to the WhatsApp window.')
time.sleep(5)
pyautogui.typewrite('Bot Activated !\n', interval=0.1)

while botAlive:
	screen = pyautogui.screenshot()
	latestMessageReceived = screen.crop(receivedMessagePosition)
	receivedMessage = pytesseract.image_to_string(latestMessageReceived)
	latestMessageSend = screen.crop(sendMessagePosition)
	sendMessage = pytesseract.image_to_string(latestMessageSend)
	for word in receivedMessage.split(' ') + sendMessage.split(' '):
		if word.lower() == 'kill':
			pyautogui.typewrite('*PAN\n', interval=0.1)
			time.sleep(1)
			pyautogui.typewrite('Bot Deactivated !\n', interval=0.1)
			botAlive = False
	time.sleep(1)

print "Bot exited without error"
	
