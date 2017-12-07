#Use createQueue(q) to create a queue named q
#Use publish(message, q) to publish the message m on the queue q
#The ticketHandler's queue is called ticekt, so you must use the sam name
#To us ethe function import this module

import pika

channel = connection.channel()
channel.queue_declare('hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

connection.close()

def createQueue(q):
	connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
	channel = connection.channel()
	channel.queue_declare(q)
	return channel

def publish(m, q):
	channel.basic_publish(exchange='', routing_key = q, body = m)