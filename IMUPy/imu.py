import serial
import time
import RPi.GPIO as GPIO
#set up led light for output to blink to show taking data
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)

count = 0
#connect to the serial port the IMU is plugged in to (may change from USB1 in future
ser = serial.Serial(port='/dev/ttyUSB1',baudrate=115200,parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_TWO, bytesize = serial.EIGHTBITS,timeout = None)
print(ser.isOpen())
commaCount = 0
nums = ''
#acceptable numbers to read in from serial input
acceptable = "0123456789-."
numberedData = []
accel = []
gyro = []
output = []
i = 0
#stay in while loop
run = True
#lights turn on and off logic
lights = True
while run:
	try:
		#every 50 times through lights should blink (roughly 1 sec because of 50Hz imu frequency)
		if count % 50 == 0:
			GPIO.output(21,lights)
			lights= not(lights)
			count=0
		t = round(time.time()*1000)
		#get time in miliseconds and if mod 2 then take data for (50Hz frequency)
		if (t/10)%2 == 0:
			count+=1
			#read in serial bytes
			bytesToRead = ser.readline()
			#decode from bytes format
			data = bytesToRead.decode()
			#first 7 characters are unusable (VN200 something like that)
			data = str(data[7:])
			#error checking print the data
#			print(data)
			#if the length of the data is less than 44 dont take that data set (two places in front of decimal two behind for 11 data points)
			#sometimes the read will give you a partial read so we do not want to parse that partial read and get data in the wrong format
			if len(data) < 44:
				break
			#parse the data
			while i < len(data)-1:
				while(data[i] != ',' and i <= len(data)-2):
					if data[i] in acceptable:
						nums+=data[i]
					else:
						pass
					i+=1
				i+=1
				numberedData.append(float(nums))
				nums = ''
			i = 0
			#accelerometer data is x,y,z(some order) and lies in the 3:6 part of the array
			accel = numberedData[3:6]
			#gyro data is x,y,z and lies in 6:9 of the array
			gyro = numberedData[6:9]
			#output is going to be array of [time in milisecond,[x,y,z accel],[x,y,z gyro]]
			output.append(t)
			output.append(accel)
			output.append(gyro)
			dateObj = time.gmtime()
			month = dateObj.tm_mon
			day = dateObj.tm_mday
			hour = dateObj.tm_hour
			min = dateObj.tm_min
			year = dateObj.tm_year
			f = open("/home/ubuntu/IMULog/text.txt",'w')
			try:
				#open text file in imuMonth:Day:Year:Hour:Minute.txt format to log data
				filetxt = "/home/ubuntu/IMULog/imu" + str(month)+':'+str(day)+':'+ str(year) +':' + str(hour)+':'+str(min)+'.txt' 
				#append to file
				f = open(filetxt,'a')
				f.write(str(output)+'\n')
			except FileNotFoundError:
				filetxt = "/home/ubuntu/IMULog/imu" + str(month)+':'+str(day)+':' + str(year) + ':' + str(hour) + ':' + str(min)+'.txt'
				f = open(filetxt,'w')
				f.write(str(output)+'\n')
			finally:
				#close file
				f.close()
			numberedData = []
			output = []
		else:
			pass
	except KeyboardInterrupt:
		#keyboard Interrup Ctrl C quits program
		run = False
#close serial port
ser.close()
