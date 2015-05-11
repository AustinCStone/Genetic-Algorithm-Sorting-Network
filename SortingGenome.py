import random as r 
import math as m 
import SortTestGenome

class SortingGenome:
	"""Class for containing all the genomes"""
	meta_mutation_rate = .5
	meta_mutation_amount = .001
	meta_delete_mutation_rate = .1
	meta_delete_mutation_amount = .01
	meta_copy_mutation_rate = .1
	meta_copy_mutation_amount = .01
	fitness_epsilon = 0.0000001
	def __init__(self, list_length=None, parent1=None, parent2=None):
		if parent1 is not None and parent2 is not None:
			self.mutation_rate = (parent1.mutation_rate+parent2.mutation_rate)/2.0
			self.copy_mutation_rate = (parent1.copy_mutation_rate+parent2.copy_mutation_rate)/2.0
			self.delete_mutation_rate = (parent1.delete_mutation_rate+parent2.delete_mutation_rate)/2.0
			self.list_length = parent1.list_length

			if r.random()<self.meta_mutation_rate: #allow the mutation rate to change according to the meta values
				self.mutation_rate = min(1.0, max(0.0, self.mutation_rate + (r.random()-0.5)* 2.0 * self.meta_mutation_amount))

			if r.random()<self.meta_delete_mutation_rate: #allow the delete mutation rate to change according to the meta values
				self.delete_mutation_rate = min(1.0, max(0.0, self.delete_mutation_rate + (r.random()-0.5)*2.0 * self.meta_delete_mutation_amount))

			if r.random()<self.meta_copy_mutation_rate: #allow the copy mutation rate to change according to the meta values
				self.copy_mutation_rate = min(1.0, max(0.0, self.copy_mutation_rate + (r.random()-0.5)*2.0 * self.meta_copy_mutation_amount))

			if r.random() < .5:
				parent1, parent2 = parent2, parent1 

			p2_genome_length = len(parent2.genome)
			p1_genome_length = len(parent1.genome)

			crossover_point = int(r.random() * p1_genome_length)
			if crossover_point%2 is not 0:
				crossover_point = crossover_point - 1
			#cross over
			self.genome = []
			for base_pair_num in range(crossover_point + max(0, p2_genome_length-crossover_point)):
				if base_pair_num < crossover_point +1:
					self.genome.append(parent1.genome[base_pair_num]) 
				else:
					self.genome.append(parent2.genome[base_pair_num])

			gene_length = 2 #number of base pairs per gene
			for gene_num in range((len(self.genome)/2)): #copy some genes
				if(r.random()<self.copy_mutation_rate):
					insert_location = int(m.floor(r.random()*len(self.genome)))
					self.genome.insert(insert_location, self.genome[2*gene_num])
					self.genome.insert(insert_location+1, self.genome[2*gene_num+1])

			#not clear on what this should be? n * log(n) ? 
			min_genome_size = int(float(self.list_length) * m.log(float(self.list_length)))
			for gene_num in range((len(self.genome)/2)): #delete some genes
				if(r.random()<self.delete_mutation_rate and len(self.genome) > min_genome_size):
					self.genome.pop(gene_num) 
					self.genome.pop(gene_num)

			for gene_num in range((len(self.genome)/2)): #mutate some genes
				if(r.random()<self.mutation_rate):
					self.genome[gene_num] = int(r.random() * self.list_length)


		elif list_length is not None:
			starting_length = list_length*list_length*2 #start out with a genome longer than necessary
			self.genome = [int(m.floor((r.random()*list_length)%list_length)) for x in range(2 * starting_length)]
			self.mutation_rate = r.random()/20.0 #set the starting mutation rate to between 0.0 and 0.05
			self.delete_mutation_rate = r.random()/20.0 #set the starting mutation rate to between 0.0 and 0.05
			self.copy_mutation_rate = r.random()/20.0 #set the starting mutation rate to between 0.0 and 0.05
			self.list_length = list_length
		else: 
			raise Exception("Must pass in either parents to breed or a list length")

	def canSort(self, test_sorting_genome):
		output = list(test_sorting_genome.genome)
		gene_length = 2 #number of base pairs per gene
		for gene_num in range((len(self.genome)/2)):
			position1 = self.genome[gene_num*gene_length]
			position2 = self.genome[gene_num*gene_length + 1]
			if output[position1] > output[position2]:
				output[position1], output[position2] = output[position2], output[position1] 
			#print output
		test_sorting_genome.num_attempted+=1
		swaps_from_correct = sort_and_count(output)[0]
		test_sorting_genome.num_swaps+=swaps_from_correct
		if(output == test_sorting_genome.solution):
			test_sorting_genome.num_solved+=1
		#exponentially weight performance by total swaps, linearly weight by genome length
		return 1.0/max(float(swaps_from_correct), 0.1) + (0.01/len(test_sorting_genome.genome)**2) * len(self.genome)


	def evaluateFitness(self, list_test_sorting_genome):
		num_correct_trials = 0
		num_trials = len(list_test_sorting_genome)
		total_fitness = 0.0
		for test_sorting_genome in list_test_sorting_genome:
			total_fitness+=self.canSort(test_sorting_genome)
		return total_fitness/float(len(list_test_sorting_genome))

def merge_and_count(a, b):
	assert a == sorted(a) and b == sorted(b)
	c = []
	count = 0
	i, j = 0, 0
	while i < len(a) and j < len(b):
		c.append(min(b[j], a[i]))
		if b[j] < a[i]:
			count += len(a) - i # number of elements remaining in `a`
			j+=1
		else:
			i+=1
	# now we reached the end of one the lists
	c += a[i:] + b[j:] # append the remainder of the list to C
	return count, c
   

def sort_and_count(L):
	if len(L) == 1: return 0, L
	n = len(L) // 2 
	a, b = L[:n], L[n:]
	ra, a = sort_and_count(a)
	rb, b = sort_and_count(b)
	r, L = merge_and_count(a, b)
	return ra+rb+r, L
