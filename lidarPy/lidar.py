from rplidar import RPLidar,RPLidarException
import math
import time
import RPi.GPIO as GPIO
#set up LED light to output (blink) when taking data)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
#light logic
lights = True
#keep while loop going
run = True

conf = []
angle = []
distance = []
while run:
	try:
		#conncect to lidar at /dev/RPLIDAR
		lidar = RPLidar('/dev/RPLIDAR')
		#clean the serial input
		lidar.clean_input()
		info = lidar.get_info()
		print(info)
		health = lidar.get_health()
		print(health)
		lidar.clean_input()
		#toggle light
		GPIO.output(25,lights)
		lights= not(lights)
		#go through a lidar scan and write data to log files
		for i,scan in enumerate(lidar.iter_scans()):
			#can only do max of 10 scans per second so break after 10 scans
			if (i>10):
				break
			#go through all measurements in each scan (should be 360 per scan)
			for j in range(len(scan)-1):
				#write log files in lidar(Timestamp in ms).txt
				filetxt = "/home/ubuntu/lidarLog/lidar"
				filetxt += str(round(time.time()))+".txt"
				try:
					#append to file with all data as Time: Conf: Angle: Distance: 
					#Confidence is reading from Lidar measure confidence in its measurement based on light intensity
					#Angle is in radians
					#Distance is in mm
					f = open(filetxt,"a")
					f.write("Time: "+str(round(time.time()*1000))+'\n')
					f.write("Conf: "+str(scan[j][0])+'\n')
					f.write("Angle: "+str(scan[j][1])+'\n')
					f.write("Distance: "+str(scan[j][2])+'\n')
				except:
					f= open(filetxt,"w")
					f.write("Time: "+str(round(time.time()*1000))+'\n')
					f.write("Conf: "+str(scan[j][0])+'\n')
					f.write("Angle: "+str(scan[j][1])+'\n')
					f.write("Distance: "+str(scan[j][2])+'\n')
				finally:
					f.close()
	except RPLidarException:
		print("LidarFailure")
	except KeyboardInterrupt:
		#keyboard interrupt Ctrl C stops program
		run = False
	finally:
		#stop the lidar and disconnect
		lidar.stop()
		lidar.stop_motor()
		lidar.disconnect()
