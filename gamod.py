import numpy



def calculate_fitness(equation_inputs,individal, id_thread):
    """ This method calculates the fitness function """
    ind_values= numpy.array(individal["values"])
    fitness = numpy.sum(ind_values*equation_inputs)
    message={'id': individal["id"], 'fitness': fitness, 'process': id_thread }
    
    return message

def select_mating_pool(pop,fitness, num_parents):
    """ This function returns the best individuals aka the parents selected for mating """

    
    parents= numpy.zeros((num_parents, pop.shape[1]))
    sorted_list= sorted(fitness, key= lambda i: i['fitness'], reverse=True)
    #print("sorted fitness: ", sorted_list)
    best_indivs=sorted_list[:num_parents]
    print(best_indivs)
    best_indivs_id=[]
    i=0
    for best in best_indivs:
        best_indivs_id.append(best["id"])
        parents[i, :]=pop[best_indivs_id[i], :]
        i=i+1
        
    print(best_indivs_id)
    print("parents : \n ", parents)
    
    return parents



def crossover(parents, offspring_size ):
    offsprings=numpy.empty(offspring_size)
    for k in range (offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k % parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k + 1) % parents.shape[0]

        genes_source = numpy.random.randint(low=0, high=2, size=offspring_size[1])
        for gene_idx in range(offspring_size[1]):
            if (genes_source[gene_idx] == 0):
                # The gene will be copied from the first parent.
                offsprings[k, gene_idx] = parents[parent1_idx, gene_idx]
            elif (genes_source[gene_idx] == 1):
                # The gene will be copied from the second parent.
                offsprings[k, gene_idx] = parents[parent2_idx, gene_idx]
    
    print ("offsprings: \n " , offsprings)
    
    return offsprings            


def scramble_mutation(offsprings):
    for idx in range (offsprings.shape[0]):
        mutation_gene1 = numpy.random.randint(low=0, high=numpy.ceil(offsprings.shape[1]/2 + 1), size=1)[0]
        mutation_gene2 = mutation_gene1 + int(offsprings.shape[1] / 2)
        genes_range = numpy.arange(start=mutation_gene1, stop=mutation_gene2)
        numpy.random.shuffle(genes_range)
        genes_to_scramble = numpy.flip(offsprings[idx, genes_range])
        offsprings[idx, genes_range] = genes_to_scramble
    print("After Mutation: \n", offsprings)
    return offsprings



def best_individual(pop, fitness):
    print(" i am inside best indiv")
    sorted_list= sorted(fitness, key= lambda i: i['fitness'], reverse=True)
    best_indiv_fitness= sorted_list[0]
    best_indiv_id= (best_indiv_fitness["id"])
    print ("the fitness: ", sorted_list )
    print ("the best indiv is : ", best_indiv_id)
    best_indiv=pop[best_indiv_id, :] 
    

    return best_indiv








    



    










































































































































































































































































































































































































































































































































































































































































































































































































































































































    


