import smbus2
import bme280
import time

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

while True:
	# the sample method will take a single reading and return a
	# compensated_reading object
	data = bme280.sample(bus, address, calibration_params)

	# the compensated_reading class has the following attributes
	print(f"data_id: {data.id}")
	print(f"data_timestamp: {data.timestamp}")
	print(f"temperature: {data.temperature} °C")
	print(f"pressure: {data.pressure} hPa")
	#print(f"humidity: {data.humidity}")

	# there is a handy string representation too
	#print(data)
	print("---------------------")
	time.sleep(1)
