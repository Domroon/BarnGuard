
#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

def read():
	ina = INA219(SHUNT_OHMS, address=0x40)
	ina41 = INA219(SHUNT_OHMS, address=0x41)
	ina44 = INA219(SHUNT_OHMS, address=0x44)
	ina.configure()
	ina41.configure()
	ina44.configure()

	voltage = ina.supply_voltage() #+ ina.voltage()
	power = voltage * ina.current()/1000
	
	voltage41 = ina41.supply_voltage() #+ ina41.voltage()
	power41 = voltage41 * ina41.current()/1000

	voltage44 = ina44.supply_voltage()
	power44 = voltage44 * ina44.current()/1000
	#print("Bus Voltage: %.3f V" % ina.voltage())
	try:
		print("SOLAR (CHARGE)")
		print("0x40 Current: %.3f mA" % ina.current())
		print("0x40 Voltage: %.3f V" % voltage)
		print("0x40 Power: %.3f W" % power)
		print(" ")
		print("POWERBANK (CONSUMPTION)")
		print("0x41 Current: %.3f mA" % ina41.current())
		print("0x41 Voltage: %.3f V" % voltage41)
		print("0x41 Power: %.3f W" % power41)
		print(" ")
		print("BATTERIE PACK")
		print("0x44 Current: %.3f mA" % ina44.current())
		print("0x44 Voltage: %.3f V" % voltage44)
		print("0x44 Power: %.3f W" % power44)
	#	print("Bus Current: %.3f mA" % ina.current())
	#	print("Power: %.3f W" % power)
	#	print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
	#	print("Supply voltage: %.3f V" % voltage)
	except DeviceRangeError as e:
		# Current out of device range with specified shunt resistor
		print(e)


def main():
	while True:
		read()
		time.sleep(2)
		print("-----------------------")


if __name__ == "__main__":
	main()

