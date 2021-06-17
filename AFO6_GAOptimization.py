import math, random
class Population:
    # The design and definition of population
    def __init__(self, size, chrom_size_amplification, chrom_size_shift, interval_amplification, interval_shift, cp, mp, gen_max, simulation_results_File):
        # The initialization of the population
        # size: the size of the individuals in the population
        # chrom_size_amplification: the size of the chromosome / individual for the amplification of AFO material
        # chrom_size_shift: the size of the chromosom / individual for the shift of AFO material
        # cp: the predefined probability of the crossover
        # mp: the predefined probability of the mutation
        # gen_max: the maximum ages for the mutation / maximum numbers of the loop
        self.individuals = []                                     # The individual sets for the population
        self.fitness = []                                            # The fitness function for the optimization
        self.selector_probability = []                      # The probability of selection
        self.new_individuals = []                           # The new individual sets for the offersprins
        self.elitist = {'chromosome':[0,0,0,0], 'fitness':0, 'position':0, 'age':0} # The optimum results

        self.size = size                                             # The size of the individuals
        self.chromosome_size_amplification = chrom_size_amplification         # The size of the chromosome/individual for the amplification of AFO material
        self.chromosome_size_shift = chrom_size_shift                                     # The size of the chromosome/individual for the shift of AFO material
        self.interval_amplification=interval_amplification
        self.interval_shift=interval_shift
        self.crossover_probability = cp                  # The predefined probability of the crossover
        self.mutation_probability = mp                  # The predefined probability of the mutation
        self.generation_max = gen_max                # The maximum ages for the mutation / maxmum numbers of the loop
        self. simulation_results_file = simulation_results_File      # The folder path and file of the excel file including the simulation results, default = 'AFO simulation results\AFO simulation results.xls'
        self.age = 0                                                 # The current age of the mutation / current number of loop

        #-----------------------------------------------------------------------------------------------------------------
        # Randomly generate the initial individulas for the population, and initialize the other population parameters to zeros
        v_amplification = 2 ** self.chromosome_size_amplification - 1
        v_shift=2 ** self.chromosome_size_shift - 1
        for i in range(self.size):
            self.individuals.append([random.randint(0, v_amplification), random.randint(0, v_shift), random.randint(0, v_amplification), random.randint(0, v_shift)])
            self.new_individuals.append([0, 0, 0, 0])
            self.fitness.append(0)
            self.selector_probability.append(0)
    def decode(self, interval, chromosome, type):
        if type=='integer':
            # Decode for the interval_amplification, which is a integer
            chrom=chromosome
        elif type=='float':
            # Decode for the interval_shift, which is a float
            d = interval[1] - interval[0]
            n = float (2 ** self.chromosome_size_shift -1)
            chrom=interval[0] + chromosome*d/n
            chrom=float("%.2f" %chrom)
        return chrom
    def GetSimulationResultsfromExcel(self, simulation_results_file, X):
        #--------------------------------------------------------------------------------------------------------------------------
        # Put the simulation results to a matrix from the excel file
        # Input: File_folder: The folder path for the simulation results excel
        #           File_excel: The excel file of the simulation results
        #           X: A tuple that includes the variables exported from the excel file
        # Output: Sim_output1: the subtalar angle during drop landing: S_drop
        #               Sim_output2: the subtalar angle for model without AFO during gait: S_gait
        #               Sim_output3: the subtalar angle for model with AFO during gait: S_gait_AFO
        import pandas as pd
        import os
        import numpy as np
        import xlrd
        # The folder path of pthon script
        path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
        Sim_results_file=os.path.join(path_simulation, simulation_results_file)
        if not os.path.exists(Sim_results_file):
            print('No specific file found, plrease check!')
            exit()
        table=xlrd.open_workbook(Sim_results_file).sheets()[0]
        nrows=table.nrows
        ncols=table.ncols
        # Put the simulation results exported from the excel file to the mtrix Sim_matrix, initialed by zeros
        Sim_matrix=np.zeros((nrows-1, ncols))
        for row in range (1,nrows):
            row_Values=np.array(table.row_values(row))
            Sim_matrix[row-1,:]=row_Values
        Variable0=set(np.where(Sim_matrix==X[0])[0])
        Variable1=set(np.where(Sim_matrix==X[1])[0])
        Variable2=set(np.where(Sim_matrix==X[2])[0])
        Variable3=set(np.where(Sim_matrix==X[3])[0])
        Variable_pos=list(Variable0&Variable1&Variable2&Variable3)[0]
        Sim_output1=Sim_matrix[Variable_pos][4]
        Sim_output2=Sim_matrix[Variable_pos][5]
        Sim_output3=Sim_matrix[Variable_pos][6]
        return Sim_output1, Sim_output2, Sim_output3
    def fitness_func(self, chrom1, chrom2, chrom3, chrom4, interval1, interval2, simulation_results_file):
        import math
        X= (x1, x2, x3, x4) = (self.decode(interval1, chrom1, 'integer'), self.decode(interval2, chrom2, 'float'),
                                            self.decode(interval1, chrom3, 'integer'), self.decode(interval2, chrom4, 'float'))
        # y1: Sim_output1: S_drop           y2: Sim_output2: S_gait        y3: Sim_output3: S_gait_AFO
        (y1, y2, y3)=self.GetSimulationResultsfromExcel(simulation_results_file, X)
        f_drop=lambda y1: math.exp(y1-30)
        f_gait=lambda y2, y3: abs(y2-y3)
        f_fitness=lambda y1, y2, y3: 1/(f_drop(y1) + f_gait(y2, y3))
        return f_fitness(y1, y2, y3)
    def evaluate(self):
        #--------------------------------------------------------------------------------------------------------------------
        # To calculate the fitniess of the individuals in the set self.individuals in the population
        sp = self.selector_probability
        for i in range (self.size):
            self.fitness[i] = self.fitness_func (self.individuals[i][0],   #  Put the calculated fitness of the individuals in the list self.fitness
                                                 self.individuals[i][1], self.individuals[i][2], self.individuals[i][3], self.interval_amplification, self.interval_shift, self.simulation_results_file)
        ft_sum = sum (self.fitness)
        for i in range (self.size):
            sp[i] = self.fitness[i] / float (ft_sum)   # Calculate the individual probability
        for i in range (1, self.size):
            sp[i] = sp[i] + sp[i-1]   #  Calculate the cumulated probability for each individual
    def select(self):
        # Selection, roulette gambling machine
        (t, i) = (random.random(), 0)
        for p in self.selector_probability:
            if p > t:
                break
            i = i + 1
        return i
    def cross(self, chrom1, chrom2, chromotype):
        # crossover
        if chromotype=='amplification':
            chromosome_size=self.chromosome_size_amplification
        elif chromotype=='shift':
            chromosome_size=self.chromosome_size_shift
        p = random.random()    #  generate random probability
        n = 2 ** chromosome_size -1
        if chrom1 != chrom2 and p < self.crossover_probability:
            t = random.randint(1, chromosome_size - 1)     # randomly select one point for crossover (one point crossover)
            mask = n << t    # <<    左移运算符
            (r1, r2) = (chrom1 & mask, chrom2 & mask)   # &
            mask = n >> (chromosome_size - t)
            (l1, l2) = (chrom1 & mask, chrom2 & mask)
            (chrom1, chrom2) = (r1 + l2, r2 + l1)
        return (chrom1, chrom2)
    def mutate(self, chrom, chromotype):
    # Mutation
        if chromotype=='amplification':
            chromosome_size=self.chromosome_size_amplification
        elif chromotype=='shift':
            chromosome_size=self.chromosome_size_shift
        p = random.random ()
        if p < self.mutation_probability:
            t = random.randint (1, chromosome_size)
            mask1 = 1 << (t - 1)
            mask2 = chrom & mask1
            if mask2 > 0:
                chrom = chrom & (~mask2)  # ~ Bitwise negation operation: negate each binary data, that is to change 1 to 0 and change 0 to 1
            else:
                chrom = chrom ^ mask1   # ^  Bitwise XOR operation, when two corresponding binary data are different, then the result is 1
        return chrom
    def reproduct_elitist (self):
    # Keep the best individual
        # Compare the fitness with the current population, update the best individual
        j = -1
        for i in range (self.size):
            if self.elitist['fitness'] < self.fitness[i]:
                j = i
                self.elitist['fitness'] = self.fitness[i]
        if (j >= 0):
            self.elitist['chromosome'][0] = self.individuals[j][0]
            self.elitist['chromosome'][1] = self.individuals[j][1]
            self.elitist['chromosome'][2] = self.individuals[j][2]
            self.elitist['chromosome'][3] = self.individuals[j][3]
            self.elitist['position'] = j
    def evolve(self):
    # Evolutionary process
        indvs = self.individuals
        new_indvs = self.new_individuals
        # Calculate the fitness and selection probability
        self.evaluate()
        # evolutionary process
        i = 0
        while True:
            # Select two individuals to do crossover and mutation, generate new population
            idv1 = self.select()
            idv2 = self.select()
            # Crossover operation
            (idv1_x1, idv1_x2, idv1_x3, idv1_x4) = (indvs[idv1][0], indvs[idv1][1], indvs[idv1][2], indvs[idv1][3])
            (idv2_x1, idv2_x2, idv2_x3, idv2_x4) = (indvs[idv2][0], indvs[idv2][1], indvs[idv2][2], indvs[idv2][3])
            (idv1_x1, idv2_x1) = self.cross(idv1_x1, idv2_x1, 'amplification')
            (idv1_x2, idv2_x2) = self.cross(idv1_x2, idv2_x2, 'shift')
            (idv1_x3, idv2_x3) = self.cross(idv1_x3, idv2_x3, 'amplification')
            (idv1_x4, idv2_x4) = self.cross(idv1_x4, idv2_x4, 'shift')
            # Mutation operation
            (idv1_x1, idv1_x2, idv1_x3, idv1_x4)=(self.mutate(idv1_x1, 'amplification'), self.mutate(idv1_x2, 'shift'), self.mutate(idv1_x3, 'amplification'), self.mutate(idv1_x4, 'shift'))
            (idv2_x1, idv2_x2, idv2_x3, idv2_x4)=(self.mutate(idv2_x1, 'amplification'), self.mutate(idv2_x2, 'shift'), self.mutate(idv2_x3, 'amplification'), self.mutate(idv2_x4, 'shift'))
            (new_indvs[i][0], new_indvs[i][1], new_indvs[i][2], new_indvs[i][3]) = (idv1_x1, idv1_x2, idv1_x3, idv1_x4)                                      # Save the results in the new population self.new_individuals
            (new_indvs[i+1][0], new_indvs[i+1][1], new_indvs[i+1][2], new_indvs[i+1][3]) = (idv2_x1, idv2_x2, idv2_x3, idv2_x4)
            # Termination of the evolutionary loop
            i = i + 2                            #  Choose 2 individuals from the population every time
            if i >= self.size:
                break                           # Terminate the loop
        # Save the best individual, before the selection
        self.reproduct_elitist()
        # Update the population: use the new population after the evolution to replace the old population
        print(self.individuals)
        for i in range (self.size):
            self.individuals[i][0] = self.new_individuals[i][0]
            self.individuals[i][1] = self.new_individuals[i][1]
            self.individuals[i][2] = self.new_individuals[i][2]
            self.individuals[i][3] = self.new_individuals[i][3]
        print(self.individuals)
        print(self.selector_probability)
    def run(self):
    # Run the maximum numbers of the loop
    # In the loop, run the evolve module and output the ages, the maximum fitness and the best individual
        for i in range (self.generation_max):
            self.evolve ()
            print (i, max (self.fitness), self.elitist)
#-------------------------------------------------------------------------------------------------------------------------------------------
# The main function of the code, define the initial parameters of the algorithom
# def __init__(self, size, chrom_size_amplification, chromo_size_shift, interval_amplification, interval_shift, cp, mp, gen_max, simulation_results_File):
        # size: the size of the individuals in the population, default = 20
        # chrom_size_amplification: the size / length of the chromosome / individual for the amplification of AFO material, e.g. size(11111)=5
        # chrom_size_shift: the size /length of the chromosom / individual for the shift of AFO material, e.g. size(11111)=5
        # interval_amplification: the range / interval of the variables amplification
        # interval_shift: the range / inerval of the variables shift, default = [0,1]
        # cp: the predefined probability of the crossover, default = 0.8
        # mp: the predefined probability of the mutation, default = 0.1
        # gen_max: the maximum ages for the mutation / maximum numbers of the loop
        # simulation_results_File: the excel file that includes the simulation results, including it's folder paths
if __name__ == '__main__':
                pop = Population (20, 3, 3, [0, 127], [0, 1.0], 1, 1, 10, 'AFO simulation results\AFO simulation results.xls')
                pop.run()
