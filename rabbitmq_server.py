
import json
import subprocess
import time
import argparse
import pika
import sys

#argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-b", nargs='?', default="netapps.ece.vt.edu")
parser.add_argument("-p", nargs='?', default="/2014/fall/sentry")
parser.add_argument("-c", nargs='?', default="sentry:ev3r*W@tchful09")
parser.add_argument("-k", nargs='?', default="bennybene")
arg = vars(parser.parse_args())

ipaddress = arg["b"]
vhost = arg["p"]
userpass = arg["c"]
routingkey = arg["k"]

#makes sure credentials are formatted correctly
try:
	username = userpass.split(":")[0]
	password = userpass.split(":")[1]

except Exception, e:
	print "Invalid format for credentials"
	sys.exit(2)	

print ipaddress, vhost, username, password

try:
	#connect to message broker
	msg_broker = pika.BlockingConnection(
		pika.ConnectionParameters(host=ipaddress,
								  virtual_host=vhost,
								  credentials=pika.PlainCredentials(username,
																	password,
																	True)))
		#setup the exchange
	channel = msg_broker.channel()
	channel.exchange_declare(exchange="alarms", 
					         type="direct")

#errors
except pika.exceptions.AMQPError, ae:
	print "Error: An AMQP error has occured: " + ae.message
	sys.exit(2)	
except pika.exceptions.ChannelError, ce:
	print "Error: A channel error has occured: " + ce.message
	sys.exit(2)
except Exception, e:
	print "Unable to connect to the message broker"
	sys.exit(2)


# loops through to calculate throughput and utilization every second
# publishes to message broker
while 1:

	seconds = time.strftime("%S")

	# calculates uptime and idletime
	procuptime = subprocess.check_output(["cat", "/proc/uptime"])
	uptimearray = procuptime.split(' ')
	uptime = float(uptimearray[0])
	idletime = float(uptimearray[1])

	# retrieves the information from proc/net/dev
	procnetdev = subprocess.check_output(["cat", "/proc/net/dev"])
	wlan0index = procnetdev.find("wlan0:")
	loindex = procnetdev.find("lo:")
	eth0index = procnetdev.find("eth0:")
	wlan0 = procnetdev[wlan0index:loindex]
	lo = procnetdev[loindex:eth0index]
	eth0 = procnetdev[eth0index:]
	wlan0array = wlan0.split()
	loarray = lo.split()
	eth0array =eth0.split()
	wlan0array.remove("wlan0:")
	loarray.remove("lo:")
	eth0array.remove("eth0:")

	# parses for total bytes per network interface
	wlan0bytesrx = int(wlan0array[0])
	wlan0bytestx = int(wlan0array[8])
	lobytesrx = int(loarray[0])
	lobytestx = int(loarray[8])
	eth0bytesrx = int(eth0array[0])
	eth0bytestx = int(eth0array[8])
	totalbytes = lobytesrx + lobytestx + eth0bytesrx + eth0bytestx + wlan0bytestx + wlan0bytesrx

	# waits for one second
	time.sleep(1)

	# calculates second uptime and idletime
	procuptime2 = subprocess.check_output(["cat", "/proc/uptime"])
	uptimearray2 = procuptime2.split(' ')
	uptime2 = float(uptimearray2[0])
	idletime2 = float(uptimearray2[1])
	
	# retrieves the information from proc/net/dev 2
	procnetdev2 = subprocess.check_output(["cat", "/proc/net/dev"])
	wlan02 = procnetdev2[wlan0index:loindex]
	lo2 = procnetdev2[loindex:eth0index]
	eth02 = procnetdev2[eth0index:]
	wlan0array2 = wlan02.split()
	loarray2 = lo2.split()
	eth0array2 =eth02.split()
	wlan0array2.remove("wlan0:")
	loarray2.remove("lo:")
	eth0array2.remove("eth0:")

	# parses for total bytes per network interface 2
	wlan0bytesrx2 = int(wlan0array2[0])
	wlan0bytestx2 = int(wlan0array2[8])
	lobytesrx2 = int(loarray2[0])
	lobytestx2 = int(loarray2[8])
	eth0bytesrx2 = int(eth0array2[0])
	eth0bytestx2 = int(eth0array2[8])
	totalbytes2 = lobytesrx2 + lobytestx2 + eth0bytesrx2 + eth0bytestx2 + wlan0bytestx2 + wlan0bytesrx2

	#calculates idle change and uptime change
	idlechange = idletime2 - idletime
	uptimechange = uptime2 - uptime
	
	#calculates utilization and throughput
	utilization = 0
	if uptimechange != 0:
		utilization = 1 - idlechange/uptimechange
	throughput = totalbytes2 - totalbytes

	#format of message
	message = {"net": {
				"wlan0": {
					"rx": wlan0bytesrx+wlan0bytesrx2,
					"tx": wlan0bytestx+wlan0bytestx2
						 },
				"lo": {
					"rx": lobytesrx+lobytesrx2,
					"tx": lobytestx+lobytestx2
					  },
				"eth0": {
					"rx": eth0bytesrx+eth0bytesrx2,
					"tx": eth0bytestx+eth0bytestx2
				 		}
				      },
		   	   "cpu": utilization
		      }

    #json
	chat_msg = json.dumps(message, indent=4)
	print chat_msg

	#publishes to broker
	try:
	   	channel.basic_publish(exchange="alarms",
							  routing_key=routingkey,
							  body=chat_msg)
	except Exception, e:
		print "Something went wrong trying to publish the message"

#close connection
msg_broker.close()



