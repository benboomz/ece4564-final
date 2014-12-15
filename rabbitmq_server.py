import json
import subprocess
import time
import argparse
import pika
import sys

#argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-b", nargs='?', const="netapps.ece.vt.edu")
parser.add_argument("-p", nargs='?', default="/", const="sandbox")
parser.add_argument("-c", nargs='?', default="guest:guest", const="ECE4564-Fall2014:13ac0N!")
parser.add_argument("-k", nargs='?', const="bennybene")
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
	channel.exchange_declare(exchange="pi_utilization", 
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


# publishes to message broker
while 1:
	# waits for one second
	time.sleep(1)

	time.ctime()
	currenttime = time.strftime('%m/%d/%Y%l:%M %p')
	with open("alarms.txt") as f:
		alarmlist = f.readlines()

	message = []
	count = 1
	for alarms in alarmlist:
		if alarms  > currenttime:
			message.append({"Alarm " + str(count): alarms.strip()})
			count = count + 1

	#json
	chat_msg = json.dumps(message, indent=4)
	print chat_msg


	#publishes to broker
	try:
	   	channel.basic_publish(exchange="pi_utilization",
							  routing_key=routingkey,
							  body=chat_msg)
	except Exception, e:
		print "Something went wrong trying to publish the message"

#close connection
msg_broker.close()



