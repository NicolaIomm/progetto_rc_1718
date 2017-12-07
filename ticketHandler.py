#The ticektHandler simulate the ticket handler server
#Wait for a message from 

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tickets')

def buyTicket(ch, method, properties, body):
    print(body)

channel.basic_consume(buyTicket,
                      queue='tickets',
                      no_ack=True)



print('Service started. To exit press CTRL+C\nWaiting for someone to buy tickets...\n')
channel.start_consuming()