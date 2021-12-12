Maha Mapara
CS 131: Assignment A3

Assumptions and rules:
1. A backpack is an individual containing a set of boxes. The set of boxes is the solution.
2. An empty backpack is represented as [0,0,0,0,0,0,0,0,0,0,0,0].
3. A backpack with weight 50 can be represented as [1,1,0,0,0,0,0,0,0,0,0,0]. Other representations are possible.
4. A population contains n individuals.
5. An individual is always of length 12 and can only have 1s or 0s.
6. The only fringe operation applied here is a single point mutation.
7. Two dictionaries contain the information about the weight and importance of each box/gene:
   gene_weight = {1: 20, 2: 30, 3: 60, 4: 90, 5: 50, 6: 70, 7: 30, 8: 30, 9: 70, 10: 20, 11: 20, 12: 60}
   gene_imp = {1: 6, 2: 5, 3: 8, 4: 7, 5: 6, 6: 9, 7: 4, 8: 5, 9: 4, 10: 9, 11: 2, 12: 1}
8. Fitness function will assign a value of 0 to backpack/inidividual with weight > 250. Otherwise, it returns the sum of the importance of all boxes/genes in the individual.
9. The culling method rounds up the culled population size if it is not a whole number (when size of population is divided by 2).
10. Point of mutation in child is chosen randomly using random.randint.
11. The gen_algo in GA class contains two lists of probabilities from 0.1 to 0.9, both of length 9 and values being 0.1 apart.
    Randomly chosen values from these lists are used to determine whether a child should be mutated or not. 
12. For the algorithm to decide if the generated population is fit enough or not, a fitness cutoff value of 35 was chosen based on the average maximum fitness
    value over 500 runs of the algorithm (when this value was 33).

Instructions and additional info:

1. Libraries needed for the code and test: random, math, pandas as pd, pyplot as plt from matplotlib
2. Line 218 onwards is the test for GA. A population is given as a list of lists, and the gene_weight and gene_imp dictionaries are provided.
3. The test is in two parts: one run of the algo and the resulting fittest individual from some fitter population and 500 runs of the algo. 
The fitness of the 500 fittest inviduals gets saved to the df_fit dataframe.
4. Line 239 onwards visualizes the fitness of the 500 individuals.