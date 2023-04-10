#mapSocket.py in ~/capstone directory on Turtlebot4
import socket
from rplidar import RPLidar,RPLidarException
import math
import time
import struct
run = True
conf = []
angle=[]
distance=[]
while run:
	#udp socket connection turtlebot located at 192.168.2.242 ip currently (ip address is on screen off turtlebot)
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	serverSocket.bind(('192.168.2.242',12000))
	try:
		#receive data from the client to establish connection and get ip address of client
		reply,server_address = serverSocket.recvfrom(2048)
		#turlebot lidar located at /dev/RPLIDAR
		lidar = RPLidar('/dev/RPLIDAR')
		#clean input and get basic info to show lidar working
		lidar.clean_input()
		info = lidar.get_info()
		print(info)
		health = lidar.get_health()
		print(health)
		lidar.clean_input()
		#perform scan and iterate through scan data
		for i,scan in enumerate(lidar.iter_scans()):
			if (i> 10):
				break
			for j in range(len(scan)-1):
				#struct is ifff (int float float) with confidence, angle (degrees), distance(mm), time (miliseconds)
				data = struct.pack('iffq',scan[j][0],scan[j][1],scan[j][2],round(time.time()*1000))
				#send data to client
				serverSocket.sendto(data,server_address)
	#except some lidar issue and print lidar failure 
	except RPLidarException:
		print("LidarFailure")
	#keyboard interrupt stops the script
	except KeyboardInterrupt:
		run = False
	finally:
		#finally disconnect from lidar as well as socket
		lidar.stop()
		lidar.stop_motor()
		lidar.disconnect()
		#code to say we are done sending data
		exitCode = struct.pack('iffq',0,0.0,0.0,0)
		serverSocket.sendto(exitCode,server_address)
		serverSocket.close()
