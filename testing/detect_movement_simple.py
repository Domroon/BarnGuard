import RPi.GPIO as GPIO
import time
from datetime import datetime as DateTime

def main():
	GPIO.setmode(GPIO.BCM)
	pin=24
	GPIO.setup(pin, GPIO.IN)

	movement= 0
	active = 0

	try:
		while True:
			movement = GPIO.input(24)

			if movement == 1 and active == 0:
				print("Bewegung erkannt")
				print(DateTime.now())
				active = 1
			elif movement == 0 and active == 1:
				print("Keine Bewegung")
				active = 0

			time.sleep(0.1)

	except KeyboardInterrupt:
		GPIO.cleanup()


if __name__ == "__main__":
	main()
