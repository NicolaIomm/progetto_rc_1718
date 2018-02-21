#The ticektHandler simulate the ticket handler server
#Wait for a message from 

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue = "TICKETS"

channel.queue_declare(queue, durable = True)

def buyTicket(ch, method, properties, body):
    print(body.decode())    # print(body)
    #time.sleep(body.count(b'.')) 
    #ch.basic_ack(delivery_tag = method.delivery_tag)

#channel.basic_qos(prefetch_count=1)
channel.basic_consume(buyTicket,
                      queue,
                      no_ack = True)



print('Service started. To exit press CTRL+C\nWaiting for someone to buy tickets...\n')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Service stopped. Bye !")
