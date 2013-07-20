import argparse
from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
import sys

def main():
	parser = argparse.ArgumentParser(description='read sensor values from a Phidgets device')
	
	group = parser.add_mutually_exclusive_group(required=True)
	
	group.add_argument('-d', '--digital', metavar='<input id>', type=int, help='read from a digital input')
	group.add_argument('-a', '--analog', metavar='<sensor id>', type=int, help='read from an analog sensor')
	
	cli_args = parser.parse_args()
	
	try:
		device = InterfaceKit()
	except RuntimeError as e:
		print("Runtime Error: %s" % e.message)
		exit(2)
	
	try:
		device.openPhidget()
		device.waitForAttach(1000)
		
		if cli_args.digital != None:
			if cli_args.digital < device.getInputCount():
				print device.getInputState(cli_args.digital)
			else:
				parser.print_usage()
				print('%s: error: input id out of range (maximum is %d)' % (sys.argv[0], device.getInputCount()-1))
		elif cli_args.analog != None:
			if cli_args.analog < device.getSensorCount():
				print device.getSensorValue(cli_args.analog)
			else:
				parser.print_usage()
				print('%s: error: sensor id out of range (maximum is %d)' % (sys.argv[0], device.getSensorCount()-1))
		device.closePhidget()
	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		try:
			device.closePhidget()
		except PhidgetException as e:
			print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)
	exit(0)

if __name__ == '__main__':
	main()
