#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_huskylens_ex8_object_classification.py
#
# This example shows how to set the Huskylens up for object classification.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, February 2025
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#===============================================================================

from XRPLib.defaults import *
import qwiic_huskylens 
import sys
import time

# Create instance of device
myHuskylens = qwiic_huskylens.QwiicHuskylens() 

def millis():
	return time.time_ns() // 1000000 #only works in MicroPython
	
def runExample():
	print("\nQwiic Huskylens Example 8 - Object Classification\n")

	# Check if it's connected
	if myHuskylens.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection",
			file=sys.stderr)
		return

	# Initialize the device
	if myHuskylens.begin() == False:
		print("Failed to initialize the device. Please check your connection", file=sys.stderr)
		return

	if not userButtonAwaitedForSeconds(5):
		print("Button not pressed. Skipping training.")
	else:
		print("Button pressed. Starting training...")
		myHuskylens.forget() # Forget all the objects that the device has already learned
		for i in range(1, 5):
			train_object(i)


	if myHuskylens.set_algorithm(myHuskylens.kAlgorithmObjectClassification) == False: # The device has several algorithms, we want to use object classification
		print("Failed to set algorithm. Please try running again.", file=sys.stderr)

	# The block will not move with the object, but the ID will be the closest match the algorithm can make to an ID we have taught it
	while True:
		# This function will return a list of objects of interest that the device sees
		# In object classification mode, these objects will have the ID of one of the objects we have learned
		myClassifications = myHuskylens.get_objects_of_interest()
		if len(myClassifications) == 0:
			print("No objects found")
		else:
			for classification in myClassifications:
				print ("object ID: " + str(classification.id))

		time.sleep(0.1)

def userButtonAwaitedForSeconds(seconds):
	print("Press the button to begin training, skipping training in...")
	pressed = False
	for i in range(seconds, 0, -1):
		board.led_on()
		print(f"{i}...")
		time.sleep(0.25)
		if board.is_button_pressed() == 1:  # Button pressed (HIGH)
			pressed = True
			break
		board.led_off()
		time.sleep(0.75)
		if board.is_button_pressed() == 1:
			pressed = True
			break

	board.led_off()
	return pressed

def train_object(object_num):
	print(f"Let's teach the HuskyLens object #{object_num}.")
	print("Place the object in front of the camera.")
	print("When the object is in view and in the square, enter anything to continue.")
	input()

	myHuskylens.learn_new()
	print("Object learned!")

	print("Now move the object around so the HuskyLens can track it at different angles.")
	print("Training for 15 seconds...")

	startTime = millis()
	while (millis() - startTime < 15000):
		myHuskylens.wait_for_objects_of_interest()
		myHuskylens.learn_same()
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)