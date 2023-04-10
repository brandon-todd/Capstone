from irobot_create_msgs.msg import WheelVels
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
import time
import math
import threading
#typical ros node to interface with wheel velo odometer readings
class WheelVelo(Node):
	def __init__(self):
		super().__init__('wheelvelo')
		self.wheel_velo_subscriber = self.create_subscription(
			WheelVels,
			'/wheel_vels',
			self.wheel_velo_callback,
			qos_profile_sensor_data)
	def wheel_velo_callback(self, wv: WheelVels):
		f = open("test.txt","w")
		dateObj = time.gmtime()
		month = dateObj.tm_mon
		day = dateObj.tm_mday
		hour = dateObj.tm_hour
		min = dateObj.tm_min
		year = dateObj.tm_year
		output = []
		#output file should be array of [time in ms,wheel velocity left,wheel velocity right]
		output.append(round(time.time()*1000))
		output.append(wv.velocity_left)
		output.append(wv.velocity_right)
		try:
			#write log files as wheelveloMonth:Day:Year:Hour:Minute.txt
			filetxt = "/home/ubuntu/wheelLog/wheelvelo"
			filetxt += str(month)+':'+str(day)+':'+ str(year) +':' + str(hour)+':'+str(min)+'.txt'
			#append to file
			f = open(filetxt,"a")
			f.write(str(output)+'\n')
		except:
			f = open(filetxt,"w")
			f.write(str(output)+'\n')
		finally:
			f.close()

def main(args=None):
	rclpy.init(args=args)
	node = WheelVelo()
	#attempt to run at 50 Hz
	thread = threading.Thread(target=rclpy.spin(node,),daemon=True)
	rate = node.create_rate(50)
	try:
		while rclpy.ok():
			rate.sleep()
	except KeyboardInterrupt:
		pass

	node.destoy_node()
	rclpy.shutdown()

if __name__ == '__main__':
    main()
