import random as r 
import math as m 
import SortTestGenome

class SortingGenome:
	"""Class for containing all the genomes"""
	meta_mutation_rate = .01
	meta_mutation_amount = .01
	fitness_epsilon = 0.0000001
	def __init__(self, list_length=None, parent1=None, parent2=None):
		if parent1 is not None and parent2 is not None:
			self.mutation_rate = (parent1.mutation_rate+parent2.mutation_rate)/2.0
			self.list_length = parent1.list_length
			if r.random()<self.meta_mutation_amount: #allow the mutation rate to change according to the meta values
				self.mutation_rate += (r.random()-0.5)*self.meta_mutation_amount
			if r.random() < .5:
				parent1, parent2 = parent2, parent1 
			genome_length = len(parent1.genome)
			crossover_point = int(r.random() * genome_length)
			self.genome = [parent1.genome[x] if x < crossover_point+1 else parent2.genome[x] for x in range(genome_length)]
	 		map(lambda nucleotide: nucleotide if r.random() < self.mutation_rate else \
	 			int(r.random() * (self.list_length + 1)), self.genome)
		elif list_length is not None:
			#max number of comparisons to sort list = (n-1) + (n-2) + (n-3) + ... + 3 + 2 + 1 = 1/2 (n-1)n 
			max_comparisons = int((1.0/2.0) * ( float(list_length-1)*float(list_length) ))
			self.genome = [int(m.floor((r.random()*list_length)%list_length)) for x in range(2 * max_comparisons)]
			self.mutation_rate = r.random()
			self.list_length = list_length
		else: 
			raise Exception("Must pass in either parents to breed or a list length")

		print 'mutation rate is ' + str(self.mutation_rate)

	def canSort(self, test_sorting_genome):
		output = test_sorting_genome.genome;
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
		return swaps_from_correct


	def evaluateFitness(self, list_test_sorting_genome):
		num_correct_trials = 0
		num_trials = len(list_test_sorting_genome)
		total_swaps = 0
		for test_sorting_genome in list_test_sorting_genome:
			total_swaps+=self.canSort(test_sorting_genome)
		return m.exp(-total_swaps/len(list_test_sorting_genome))


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
