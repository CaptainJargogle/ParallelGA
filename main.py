import threading
import master

import slave

import numpy 
import multiprocessing

import sys






if __name__ == "__main__":
    
    #init genetic algo stuff
    # Inputs of the equation.
    
    
    # Number of the weights we are looking to optimize.
    num_weights = 6
    
    """
    Genetic algorithm parameters:
        Mating pool size
        Population size
    """
    sol_per_pop = 8
    num_parents_mating = 4
    
    # Defining the population size.
    pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    
    offspring_size= (sol_per_pop-num_parents_mating,num_weights)
    
    #Creating the initial population.
    
    
    new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)
    num_generations = 5
    
    
    the_master=master.Master(sol_per_pop,new_population,num_generations,pop_size,offspring_size)

        
    slave1=slave.Slave("slave1")
    slave2=slave.Slave("slave2")
    #slave3=slave.Slave("slave3")
    print("Slave 1 Process")
    slave1_process=multiprocessing.Process(target=slave1.run(),args=(1,))
    slave1_process.start()
    print("Slave 2 second Process")
    slave2_process=multiprocessing.Process(target=slave2.run(),args=(1,))
    slave2_process.start()
    #print("Slave 3 Process")
    #slave3_process=multiprocessing.Process(target=slave3.run(),args=(1,))
    print("Master Process")
    master_process=multiprocessing.Process(target=the_master.run(), args=(1,))
    master_process.start()
    while (the_master.not_done_yet):
        continue
    slave1_process.terminate()
    slave2_process.terminate()
    master_process.terminate()
    print("THE END!!!")
    sys.exit()





    
    
    

    




