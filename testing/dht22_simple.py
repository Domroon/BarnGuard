import time
import board
import adafruit_dht

def main():
	dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=True)

	while True:
		try:
			temperature_c = dhtDevice.temperature
			humidity = dhtDevice.humidity
			print(f'Humidity: {humidity} %')
			print(f'Temp: {temperature_c} °C')
		except RuntimeError as error:
			print(error.args[0])
			time.sleep(2)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error

		time.sleep(2)


if __name__ == "__main__":
	main()
