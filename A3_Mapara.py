'''
Name: Maha Mapara
CS 131-A3: Genetic Algorithm
Due date: 10/27/21
'''

#libraries used
import random
import math
import pandas as pd
from matplotlib import pyplot as plt

############
class GA:

    def __init__(self, pop, gene_weight, gene_imp):
        '''
        Purpose: Creates a new GA object

        Arguments:
            pop = an array of arrays or list of lists. Each array/list inside is an individual/backpack represented by 1's and 0's of length 12
            gene_weight = a dictionary where the key is the box number(gene) and the value is the weight of that box
            gene_imp = a dictionary where the key is the box number(gene) and the value is the importance of that box
        '''

        self.pop = pop
        self.gene_weight = gene_weight
        self.gene_imp = gene_imp

    def reader(self, indiv):
        '''
        Purpose: To convert the 1/0 genotype of an individual/backpack to the box number/gene

        Arguments:
            indiv: a list of 1/0s of length 12

        Returns:
            indiv_g: a list of the box/gene ID/numbers in the individual/backpack
        '''

        indiv_g = [] #initialize empty list
        for i in range(len(indiv)):
            if indiv[i] == 1:
                indiv_g.append(i+1) #if at position i, value is 1, add 1 and then we have the bix number associated with that gene

        return indiv_g

    def fit_func(self, indiv):
        '''
        Purpose: To give the fitness of an individual/backpack

        Arguments:
            indiv: a list of 1/0s of length 12

        Returns:
            imp: the sum of the importance of each gene/box in the individual/backpack
        '''

        indiv_g = self.reader(indiv) #convert chromosome to list compatible with dictionary use

        #initialize weight and importance vars
        weight = 0
        imp = 0

        for i in range(len(indiv_g)):
            weight += self.gene_weight.get(indiv_g[i]) #get total weight of an individual/backpack using gene_weight dictionary

        if weight > 250: #check for constraint. If it doesn't meet it, fitness is zero
            return 0
        else:
            for i in range(len(indiv_g)):
                imp += self.gene_imp.get(indiv_g[i]) #get total importance of an indiv/backpack using gene_imp dictionary
            return imp


    def culling(self):
        '''
        Purpose: Perform a method for population selection which based on the fitness of each individual in the population,
                    ranks them in descending order and selects the top 50% of individuals.

        Returns:
            fit_pop[g]: a random individual from the culled population
        '''
        #initialize lists and dictionary needed
        fit_score = []
        fit_pop_ind = []
        store = {}
        fit_pop = []

        #create dictionary(store) that has the index position of each individual in population as the key and the inidividual's fitness as the value
        for i in range(len(self.pop)):
            fit_score.append(self.fit_func(self.pop[i])) #getting fitness of each indiv in population
            store.update([(i, fit_score[i])]) #adding index and associated fitness to dictionary called store

        #cull and get fitness of the culled population
        fit_score = sorted(fit_score, reverse = True) #sort fit_score by descending order of fitness value
        cull_size = math.ceil(len(fit_score)/2) #get size of culled population (50% of starting population). ceil rounds it up if not whole number
        fit_culled = fit_score[0: cull_size] #choose the fitness values upto the cull_size

        #get index if inidividuals from pop based on fitness values from fit_culled and append to fit_pop_ind
        for f in range(len(fit_culled)):
            fit_pop_ind.append([k for k, v in store.items() if v == fit_culled[f]][0])

        #use index of individuals from fit_pop_ind to get individuals in the culled population
        for n in range(len(fit_pop_ind)):
            ind = fit_pop_ind[n]
            fit_pop.append(pop[ind])

        g = random.randint(0, len(fit_pop)-1) #to get a random individual from the culled population

        return fit_pop[g] #returns one random individual from culled population


    def reproduce(self, x, y):
        '''
        Purpose: To create an individual (child) using two individuals (parents)

        Arguments:
            x: a list of 1s and 0s of length 12
            y: a list of 1s and 0s of length 12

        Returns:
            x1: an individual(list of 1s and 0s of length 12) which is a mixture of x and y
        '''

        n = len(x)#get length of inidividual x (always 12)
        c = random.randint(0,n) #get randm number b/w 0 and n

        x1 = x[0:c] #index x from 0 to c
        y2 = y[c:n] #index y from c to n
        x1.extend(y2) #put them together
        return x1

    def mutate(self, child):
        '''
        Purpose: A fringe operator that makes a single random change to an individual's chromosome

        Arguments:
            child: a list of 1s and 0s of length 12

        Returns:
            child: a list of 1s and 0s of length 12 different from the child argument by one gene
        '''

        i = random.randint(0, len(child)-1) #choose a random index in child

        if child[i] == 1: #if value at that index is a 1, change to 0
            child[i] = 0
        else:
            child[i] = 1 #if index at that value is a 0, change to 1
        return child

    def gen_algo(self):
        '''
        Purpose: Takes a random population and generates the fittest population over several generations by using a fitness function, selection(culling),
                    reproduction, and fringe operator(mutation).

        Returns:
            self.pop[max_ind]: fittest individual in the fittest population
        '''

        #initialize fit_val which will later be the maximum fitness value in a population
        fit_val = 0

        #lists of probabilities
        probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        r_probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        #main loop that keeps culling, reproducing, mutating till maximum fintess is at 33
        while fit_val < 35: #fitness cutoff value chosen based on mean max fitness value over 500 runs of the algorithm

            #initialize new_pop and fit_check lists
            new_pop = []
            fit_check = []

            #get random index for the probability lists above. new index for each population
            probs_i = random.randint(0, len(probs)-1)
            r_p_i = random.randint(0, len(r_probs)-1)


            for i in range(len(pop)): #culling, reproducing and mutating population size times (to get to original population size)

                #culling the population and getting inidividuals from culled population
                x = self.culling()
                y = self.culling()

                #culled inidividuals reproduce to create a new individual
                child = self.reproduce(x, y)

                #pick a random prob value that decides whether or not mutation should occur
                p = probs[probs_i]
                rp = r_probs[r_p_i]

                if p < rp: #based on this condition, child undergoes mutation or not
                    child = self.mutate(child)
                    new_pop.append(child) #mutuated child added to new population
                else:
                    new_pop.append(child) #add child to new population

            self.pop = new_pop #new population assigned to original/initial population

            #get fitness of each individual in new population
            for p in range(len(self.pop)):
                fit_check.append(self.fit_func(self.pop[p]))

            #get max fitness of new population
            fit_val = max(fit_check) #if this value is < 33, a new generation will be geenrated using new population
                                    # if = or > 33, gets out of while loop

        #get index of max fitness individual
        max_ind = fit_check.index(fit_val)

        #return fittest individual in population
        return self.pop[max_ind]



#####################################################################Test#######################
pop = [[0,1,0,0,0,0,0,0,1,1,0,0], [0,0,0,1,0,0,0,0,1,1,0,0], [1,0,0,1,0,0,0,0,1,0,0,0], [1,0,0,0,0,0,0,0,1,1,0,1],[1,1,0,0,1,0,0,0,0,1,0,1], [0,0,1,1,1,1,0,0,0,0,0,0], [0,0,0,0,0,1,0,0,1,0,0,1], [0,0,0,0,0,0,0,0,0,1,1,1], [1,1,0,0,1,0,0,0,0,0,0,0]]
gene_weight = {1: 20, 2: 30, 3: 60, 4: 90, 5: 50, 6: 70, 7: 30, 8: 30, 9: 70, 10: 20, 11: 20, 12: 60}
gene_imp = {1: 6, 2: 5, 3: 8, 4: 7, 5: 6, 6: 9, 7: 4, 8: 5, 9: 4, 10: 9, 11: 2, 12: 1}

#####################one run
ga = GA(pop, gene_weight, gene_imp)
ind = ga.gen_algo()
ga.fit_func(ind)

####################500 times
fit_tracker = []
ga = GA(pop, gene_weight, gene_imp)

for i in range(500):
    fip = ga.gen_algo()
    fit_tracker.append(ga.fit_func(fip)) #tracks maximum fitness of individual from fittest population for each run of the algorithm

df_fit = pd.DataFrame(list(zip(range(0,500), fit_tracker)), #dataframe saves the number of runs and the fittest individual resulting from each run
                 columns=['Iterations', 'Fitness of fittest'])

####visualize 500 runs

ax = plt.gca()

df_fit.plot(kind ='line', x='Iterations', y='Fitness of fittest', ax=ax)

plt.xlabel('No. of iterations');
plt.ylabel('Fitness of fittest');
plt.title('Fitness of fittest vs No. of iterations')

plt.show()
