import picamera
import time


def main():
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		time.sleep(1)
		filename = "my_video.h264"
		camera.start_recording(filename)
		camera.wait_recording(10)
		camera.stop_recording()
		print(f'Captured "{filename}"')

if __name__ == "__main__":
	main()
