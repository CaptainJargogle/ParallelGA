import numpy
import pika
import threading
import json
from time import sleep
import gamod


class Slave:

    """ This is the Slave class where the fitness evaluation happens """

    def __init__(self, id,):
        
        self.equation_inputs = [4,-2,3.5,5,-11,-4.7]
        self.population= []
        self.individual= {}
        self.id = id
        
        
        #init population queue
        self.connection_slave =pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_recieve = self.connection_slave.channel()
        self.channel_recieve.queue_declare(queue='population')


        #init fitness queue
        self.connection_slave =pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_send= self.connection_slave.channel()
        self.channel_send.queue_declare(queue='fitness')

        




        



    
    def callback(self,ch, method, properties, body):
            #print(" [x] Received %r" % json.loads(body))
            
            self.individual= json.loads(body)
            #print("this is ", self.id, ", I recieved indiv" , self.individual["id"] )
            self.population.append(json.loads(body))
            fitness_val=gamod.calculate_fitness(self.equation_inputs, self.individual, self.id )
            self.send_fitness(fitness_val)
            
            
            


    def send_fitness(self, fval):
        """This Method is Sending the fitness evaluation to the Master"""

        
        self.channel_send.basic_publish(exchange='',
                            routing_key='fitness',
                            body= json.dumps(fval))

        

        


    def recieve_pop(self):
        """ The Method is going to recieve population chunks from the Master """
        self.channel_recieve.basic_consume(queue='population',
                        auto_ack=True,
                        on_message_callback=self.callback)   
        try:
            
            self.channel_recieve.start_consuming() 
            
        except KeyboardInterrupt:
            self.connection_slave.close()
            print ("connection closed")




    def run(self, ):
        """ This Method runs everything (Slave)"""

        print("Slave ", self.id, "is running" )
        
        recieve_thread=threading.Thread(target=self.recieve_pop)
        recieve_thread.start()
        #send_thread=threading.Thread(target=self.send_fitness)
        #send_thread.start()
        
