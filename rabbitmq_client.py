#!/usr/bin/env python

__author__ = "Benny Ong"

import sys
import getopt
import pika
import pika.channel
import pika.exceptions
import signal
import json


stats_history = { "cpu": {"max": 0.0, "min": float("inf"), "current": 0.0},
				  "net": dict()}
				  
class StatsClientChannelHelper:
	"""
	This helper class is used to manage a channel and invoke event handlers when
	signals are intercepted
	"""
	def __init__(self, channel):
		"""
		Create a new StatsClientChannelEvents object

		:param channel: (pika.channel.Channel) The channel object to manage
		:raises ValueError: if channel does not appear to be valid
		:return: None
		"""
		if isinstance(channel, pika.channel.Channel):
			self.__channel = channel
		else:
			raise ValueError("No valid channel to manage was passed in")

	def stop_stats_client(self, signal=None, frame=None):
		"""
		Stops the pika event loop for the managed channel

		:param signal: (int) A number if a intercepted signal caused this handler
					   to be run, otherwise None
		:param frame: A Stack Frame object, if an intercepted signal caused this
					  handler to be run
		:return: None
		"""
		self.__channel.stop_consuming()	
		print "Exiting stats client view app"
		sys.exit()
		

# Print out usage format for command line arguments
def usage():
	print "Usage: pistatsview -b message broker [-p virtual host] [-c login:password] -k routing key"

# Stat message callback
def on_new_msg(channel, delivery_info, msg_properties, msg):
	"""
	Event handler that processes new messages from the message broker

	For details on interface for this pika event handler, see:
	https://pika.readthedocs.org/en/0.9.14/examples/blocking_consume.html

	:param channel: (pika.Channel) The channel object this message was received
					from
	:param delivery_info: (pika.spec.Basic.Deliver) Delivery information related
						  to the message just received
	:param msg_properties: (pika.spec.BasicProperties) Additional metadata about
						   the message just received
	:param msg: The message received from the server
	:return: None
	"""

	#print "on_new_msg"
	# Parse the JSON message into a dict
	try:
		listofalarms = json.loads(chat_msg)
		print listofalarms
		print 

		for alarms in listofalarms:
			alarm_string = str(alarms)
			if "Alarm" in alarm_string:
				print alarm_string[15:].replace("'}","")
					

	except ValueError, ve:
		# Thrown by json.loads() if it could not parse a JSON object
		print "Warning: Discarding Message: received message could not be parsed"

# Main function 
def main(argv):
	try:
		opts, args = getopt.getopt(argv, "b:p:c:k:")
	except getopt.GetoptError:
		print "Error: input arguments not formatted correctly"
		usage()
		sys.exit(2)

	broker = None
	vhost = "sandbox"
	login = "ECE4564-Fall2014"
	password = "13ac0N!"
	rkey = None

	if "-b" not in (opt[0] for opt in opts) or "-k" not in (opt[0] for opt in opts):
		print "Must provide flags and arguments for both message broker and routing key."
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-b":
			broker = arg
			print "Entered " + broker + " for message broker."
		elif opt == "-p":
			print "Entered " + vhost + " for virtual host."
		elif opt == "-c":
			if arg.find(":") == -1:
				print "Credentials must be formatted as login:password"
				usage()
				sys.exit(2)

			credentials = arg.split(":")
			login = credentials[0]
			password = credentials[1]
			print "Entered " + credentials[0] + " for user name credentials."
		elif opt == "-k":
			rkey = arg
			print "Entered " + rkey + " for routing key."
			
	message_broker = None
	channel = None
	try:
		# Connect to message broker
		message_broker = pika.BlockingConnection(
			pika.ConnectionParameters(host=broker,
			virtual_host=vhost,
			credentials=pika.PlainCredentials(login, password,True)))
		
		print "Connected to message broker"
		channel = message_broker.channel()
		channel.exchange_declare(exchange="pi_utilization",
												type="direct")
			
		signal_num = signal.SIGINT
		# Create eventg handler if signal is caught
		try:
			channel_manager = StatsClientChannelHelper(channel)
			signal.signal(signal_num, channel_manager.stop_stats_client)
			signal_num = signal.SIGTERM
			signal.signal(signal_num, channel_manager.stop_stats_client)
			
		except ValueError, ve:
			print "Warning: Graceful shutdown may not be possible: Unsupported signal: " + signal_num
										
		
		# Create a queue to receive messages
		my_queue = channel.queue_declare(exclusive=True)
		
		# Bind the queue to the stats exchange
		channel.queue_bind(exchange="pi_utilization",
									queue=my_queue.method.queue,
									routing_key=rkey)
							
		# Setup callback for when a subscribed message is received
		channel.basic_consume(on_new_msg, queue=my_queue.method.queue, no_ack=True)
		print "New message from broker"
		
		channel.start_consuming()
		
	except pika.exceptions.AMQPError, ae:
		print "Error: An AMQP error has occured: " + ae.message
		
	except pika.exceptions.ChannelError, ce:
		print "Error: A channel error has occured: " + ce.message
		
	except Exception, eee:
		print "Error: An unexpected exception has occured: " + eee.message

	finally: 
		if channel is not None: 
			channel.close()
		if message_broker is not None:
			message_broker.close()
		
		
if __name__ == "__main__":
	main(sys.argv[1:])
