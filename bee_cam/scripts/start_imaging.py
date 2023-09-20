from picamera2 import Picamera2
from time import sleep, perf_counter
from datetime import datetime, timedelta
import os
import sys

import subprocess
sleep(10)
def get_ip_address():
	try:
		ip = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
		return ip
	except subprocess.CalledProcessError:
		return  "Unable to get IP"
ip_address = get_ip_address()
print("IP; ", ip_address)


name = 'pi5'
size = (2304, 1296)
lens_position = 2.6

try:
	pid = str(os.getpid())
	pidfile = '/home/pi/imaging/kill.pid'
	with open(pidfile, 'w') as f:
		f.write(pid)
except:
	print('pid not written')

camera = Picamera2()
cam_config = camera.create_still_configuration({'size': size})
camera.configure(cam_config)
camera.exposure_mode = 'sports'
camera.set_controls({"LensPosition": lens_position})
camera.start()
sleep(5)

# set output dir
path_images = "/home/pi/imaging/images/"
date_folder = str(datetime.now().strftime("%Y-%m-%d"))
time_path = os.path.join(path_images, date_folder)
os.makedirs(time_path, exist_ok = True)

# Change working directory to save image files:
os.chdir(time_path)
print("Imaging...")

while True:
	time_current = datetime.now()
	time_current_split = str(time_current.strftime("%Y%m%d_%H%M%S"))
	try:
		camera.capture_file(name+'_'+time_current_split+'.jpg')
		print("Image acquired: ", time_current_split)
		sleep(1)
	except KeyboardInterrupt:
		print('\nexiting')
		sys.exit()
