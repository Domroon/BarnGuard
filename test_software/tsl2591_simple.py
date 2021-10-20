from python_tsl2591 import tsl2591
import time

def main():
	tsl = tsl2591() # initialize

	#full, ir = tsl.get_full_luminosity()
	#lux = tsl.calculate_lux(full, ir)

	while True:
		#print("ALL VALUES:")
		#print(full, ir)
		readings = tsl.get_current()
		print(f'{round(readings["lux"], 3)} lux')
		#print(tsl.get_current())
		#print("LUX, FULL, IR")
		#print(lux, full, ir)
		time.sleep(2)


if __name__ == "__main__":
	main()
