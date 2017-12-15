#Use createQueue(q) to create a queue named q
#Use publish(message, q) to publish the message m on the queue q
#The ticketHandler's queue is called ticekts, so you must use the sam name
#To us ethe function import this module

import pika

def createQueue(q):
	connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
	channel = connection.channel()
	channel.queue_declare(queue = q, durable = True)

	#return the connection to close and the channel 
	return (connection, channel)

def publish(c, m, q):
	c.basic_publish(exchange='', routing_key = q, body = m,  properties=pika.BasicProperties(delivery_mode = 2))

def closeConnection(c):
	c.close()

#Example 
#(co, ch) = createQueue('ticekts')
#publish(ch, 'Utente X ha acquistato un biglieto per Concerto Y', 'tickets')
#closeConnection(co)

