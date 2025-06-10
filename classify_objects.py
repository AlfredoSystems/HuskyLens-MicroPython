#This example is based on code from SparkFun https://github.com/sparkfun/qwiic_huskylens_py

from XRPLib.defaults import *
import qwiic_huskylens 
import sys
import time

# Create instance of device
myHuskylens = qwiic_huskylens.QwiicHuskylens() 

def classifyObjects():
	print("\nHuskylens Object Classification\n")

	# Check if it's connected
	if myHuskylens.is_connected() == False:
		print("The device isn't connected to the system. Try power cycleing the robot, or unplug and replug the qwiic connector",
			file=sys.stderr)
		return

	# Initialize the device
	if myHuskylens.begin() == False:
		print("The device isn't connected to the system. Try power cycleing the robot, or unplug and replug the qwiic connector",
			file=sys.stderr)
		return

	# Set Husky Algorithm to Object Classification
	if myHuskylens.set_algorithm(myHuskylens.kAlgorithmObjectClassification) == False: # The device has several algorithms, we want to use object classification
		print("Failed to set algorithm. Please try running again.", file=sys.stderr)

	robotShouldTrain = waitForButtonPress() # returns True if button gets pressed
	objectsToLearn = 2

	#if the button got pressed start training, otherwise go straight to running.
	if (robotShouldTrain == True):
		print("Button pressed. Starting training...")
		time.sleep(2)
		myHuskylens.forget() # Forget all the objects that the device has already learned
		for i in range(1, objectsToLearn + 1):
			train_object(i)

	# Main loop
	while True:
		myClassifications = myHuskylens.get_objects_of_interest()

		if len(myClassifications) == 0:
			print("No objects found")
			drivetrain.arcade(0,0)

		else:
			for classification in myClassifications:

				print ("object ID: " + str(classification.id))

				if (classification.id == 4):
					#drive straight
					drivetrain.arcade(0.5,0)

				elif (classification.id == 3):
					#turn right
					drivetrain.arcade(0,-0.5)
					
				elif (classification.id == 2):
					#turn left
					#drivetrain.arcade(0,0.5)
					drivetrain.arcade(0,0)

				elif (classification.id == 1):
					#stop
					drivetrain.arcade(0,0)

		time.sleep(0.1)

# ---------------- helper functions ---------------- #

def waitForButtonPress():
	waitTime = 5 #seconds

	print(f"Press the button to begin training, skipping training in {waitTime} seconds")

	startTime = time.ticks_ms()
	while (time.ticks_ms() - startTime < (waitTime*1000)):

		if(time.ticks_ms() % 200 < 100):
			board.led_on()
		else:
			board.led_off()

		if board.is_button_pressed() == 1:  # Button pressed (HIGH)
			board.led_off()
			return True
		
		time.sleep(0.01)

	board.led_off()
	return False

def train_object(object_num):
	print(f"Let's teach the HuskyLens object #{object_num}.")
	print("Place the object in front of the camera.")
	print("When the object is in view and in the square, press the user button to continue.")
	board.wait_for_button()

	myHuskylens.learn_new()
	print("Object learned!")

	print("Now move the object around so the HuskyLens can track it at different angles.")
	print("Training for 15 seconds...")

	startTime = time.ticks_ms()
	while (time.ticks_ms() - startTime < 15000):
		myHuskylens.wait_for_objects_of_interest()
		myHuskylens.learn_same()
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		classifyObjects()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)