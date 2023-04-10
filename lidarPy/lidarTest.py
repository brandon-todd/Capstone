from rplidar import RPLidar, RPLidarException
import math
import time
import numpy as np
data = []
loopcount=0
count=0
lidar = RPLidar('/dev/RPLIDAR')
lidar.clean_input
try:
	t = time.time()
	for scan in lidar.iter_scans():
		print(len(scan))
		loopcount+=1
		for i in range(len(scan)-1):
			print(scan[i][0])
			print(scan[i][1])
			print(scan[i][2])
			print('\n')
			count+=1
		if(loopcount>8):
			break
except RPLidarException:
	print('error')
except KeyboardInterrupt:
	pass
finally:
	print(time.time()-t)
	print(count)
	lidar.stop()
	lidar.disconnect()

