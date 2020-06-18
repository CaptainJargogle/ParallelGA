import pika
import numpy
import threading
import json
from time import sleep
import gamod


#1 Connector per Process 
#1  Channel per Thread
class Master():
    """ This is the Master Class """

    def __init__(self, num_indiv, population,num_gen, pop_size, offspring_size):
        #initialize population
        self.not_done_yet= True
        self.last_gen= False
        self.still_running= True
        self.pop_size=pop_size
        self.population=population
        self.offspring_size=offspring_size
        self.best_indiv= None
        
        #initialize number of generations
        self.num_gen= num_gen

        #initilialize fitness_list
        self.fitness_list=[]
        self.num_indiv= num_indiv


        #init population queue
        
        self.connection_master = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_sending = self.connection_master.channel()
        self.channel_sending.queue_declare(queue="population")

        #init fitness queue
        self.connection_master =pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_recieving = self.connection_master.channel()
        self.channel_recieving.queue_declare(queue='fitness')


        


    

    
    def send_pop(self, num_individual):
        """ This Method the population to the slaves """
        for inv in range (num_individual):
            vals= self.population[inv,:]
            message={'id': inv, 'values': vals.tolist() }
            self.channel_sending.basic_publish(exchange='',
                                routing_key='population',
                                body= json.dumps(message) )

                                
                                
        
        
        



    def callback(self,ch, method, properties, body):
            """This Method is the callback, triggered when a message is recieved"""
            
            
            self.fitness_list.append(json.loads(body))
            #print("Master: here is the fitness i recieved", self.fitness_list)
            
                
            if (len(self.fitness_list) == self.num_indiv):           
                    if (self.last_gen):
                        self.best_indiv = gamod.best_individual(self.population, self.fitness_list)
                    else:
                        print ("Fitness List: ", self.fitness_list)
                        self.geneticOperators()
                        self.fitness_list=[]

            


    def recieve_fitness(self,):
        """ This Method recieves the fitness evaluation """
        
        print("just entered recieve!")
        self.channel_recieving.basic_consume(queue='fitness',
                        auto_ack=True,
                        on_message_callback=self.callback)
        
        try:
            self.channel_recieving.start_consuming()
            

        except KeyboardInterrupt:
            self.connection_master.close()
            print ("connection closed")
    
        
    
    def wait_for_Allresults(self,):
        print("waiting for the genertic operators")
        while (self.still_running):
            continue
        print("All results are in!")
        

    def geneticOperators(self, ):
        
        parents=gamod.select_mating_pool(self.population, self.fitness_list,4)
        offspring= gamod.crossover(parents, self.offspring_size)
        mutated_offspring=gamod.scramble_mutation(offspring)
        self.population=numpy.concatenate((parents,mutated_offspring),axis=0)
        
        print ("The new Generation is: \n", self.population)

        self.still_running= False
    
    


    def run(self,):

        """ This Method runs everything (Master) """

        
        print ("Master is running")
        recieve=threading.Thread(target=self.recieve_fitness)
        recieve.start() 
        
        for gen in range (self.num_gen):

            print("The Individuals are (gen : " , gen + 1 , ") \n", self.population)
            send=threading.Thread(target=self.send_pop, args=([self.num_indiv]))
            send.start()

            """ waits for event here"""
            self.wait_for_Allresults()
            send.join()

            print("I joined")
            print("done with gen: ", gen+1)

        self.last_gen = True    
        
        self.send_pop(self.num_indiv)



        print (" The best indiv is :", self.best_indiv)
        self.not_done_yet= False
        


        

            #genetic operators



        
        



        






