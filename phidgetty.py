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
	
	parser.add_argument('-t', '--temperature-sensor', action='store_const', const=True, default=False, help='device is a temperature sensor, output in degrees celcius. must be reading an analog sensor')
	parser.add_argument('-m', '--precision-light-sensor-multiplier', metavar='<multiplier>', type=float, help='\'m\' value from the underside of the precision light sensor. must be reading an analog sensor')
	parser.add_argument('-b', '--precision-light-sensor-boost', metavar='<boost>', type=float, help='\'b\' value from the underside of the precision light sensor. must be reading an analog sensor')
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
				if cli_args.temperature_sensor == True:
					print (float(device.getSensorValue(cli_args.analog)) * 0.2222) - 61.1111 
				elif (cli_args.precision_light_sensor_multiplier == None) != (cli_args.precision_light_sensor_boost == None):
					parser.print_usage()
					print('%s: error: you must supply both precision light sensor arguments')
				elif cli_args.precision_light_sensor_multiplier != None and cli_args.precision_light_sensor_boost != None:
					print (cli_args.precision_light_sensor_multiplier * float(device.getSensorValue(cli_args.analog)) + cli_args.precision_light_sensor_boost)
				else:
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
