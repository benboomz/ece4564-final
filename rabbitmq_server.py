
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

	with open('sleephistory.json', 'r+') as json_data:
		sleephistory = json.load(json_data)

	message.append(sleephistory)
	
	#json
	chat_msg = json.dumps(message, indent=4)
	print chat_msg

	time.sleep(1)
	
	#publishes to broker
	try:
	   	channel.basic_publish(exchange="alarms",
							  routing_key=routingkey,
							  body=chat_msg)
	except Exception, e:
		print "Something went wrong trying to publish the message"

#close connection
msg_broker.close()



