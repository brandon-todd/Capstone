import socket
import math
import time
import struct

run = True
while run:
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	serverSocket.setblocking(1)
	serverSocket.bind(('192.168.2.242',13000))
	reply,server_address = serverSocket.recvfrom(2048)
	try:
		print(int(reply.decode()))
		time1 = int(reply.decode())
		floatTime = float(reply.decode())
		floatTime = floatTime/1000
		roundTime = round(floatTime)
		try:
			fileName = '/home/ubuntu/wheelLog/wheelvelo' + str(roundTime) + '.txt'
			file = open(fileName,'r')
			print("file opened")
			data = file.readlines()
			index = 0
			while index<len(data):
				if data[index][6:len(str(time1))+5] == str(time1)[0:-1]:
					break
				else:
					index +=3
			replyData = data[index+1][6:-1].encode("utf-8")
			replyData2 = data[index+2][7:-1].encode("utf-8")
			#replyData = struct.pack('f',float(data[index+1][6:-1]))
			#replyData2 = struct.pack('f',float(data[index+2][7:-1]))
			serverSocket.sendto(replyData,server_address)
			serverSocket.sendto(replyData2,server_address)
			file.close()
		except FileNotFoundError:
			print("file not found\n")
			replyData = "50.0"
			serverSocket.sendto(replyData.encode("utf-8"),server_address)
			serverSocket.sendto(replyData.encode("utf-8"),server_address)
	except KeyboardInterrupt:
		run = False
	except socket.error:
		pass
	finally:
		serverSocket.close()
