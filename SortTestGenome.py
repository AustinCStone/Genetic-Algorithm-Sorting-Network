import random as r
import math as m

class SortTestGenome:
	"""Class for evaluating the fitness of sorting genomes"""
	meta_mutation_amount = .01 
	meta_mutation_amount = .01
	fitness_epsilon = 0.0000001
	def __init__(self, list_length=None, parent1=None, parent2=None):
		if parent1 is not None and parent2 is not None:
			self.mutation_rate = (parent1.mutation_rate+parent2.mutation_rate)/2.0
			if r.random()<self.meta_mutation_amount:
				self.mutation_rate += (r.random()-0.5)*self.meta_mutation_amount
			if r.random() < .5:
				parent1, parent2 = parent2, parent1 
			genome_length = len(parent1.genome)
			crossover_point = int(r.random() * genome_length)
			self.genome = [parent1.genome[x] if x < crossover_point+1 else parent2.genome[x] for x in range(genome_length)]
	 		map(lambda nucleotide: nucleotide if r.random() < self.mutation_rate else \
	 			int(r.random() * (genome_length + 1)), self.genome)
		elif list_length is not None:
			self.genome = [int(m.floor((r.random()*list_length)%list_length)) for x in range(list_length)]
			self.mutation_rate = r.random()
		else: 
			raise Exception("Must pass in list length or parents")
		self.num_attempted = 0 #number of SortingGenomes that attempted to sort, updated per generation
		self.num_solved = 0 #number of SortingGenomes that correctly sorted, updated per generation
		self.num_swaps = 0#cumulative number of swaps away from the correct solution that the population was
		self.solution = sorted(self.genome)
		self.max_swaps = 2.0**(len(self.genome)/2.0) 

	def evaluateFitness(self):
		if (self.num_solved/self.num_attempted) > 0.6:
			return self.fitness_epsilon
		else:
			return self.num_swaps/(self.max_swaps*self.num_attempted)
