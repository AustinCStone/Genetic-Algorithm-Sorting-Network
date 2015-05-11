import SortingGenome as sg
import SortTestGenome as stg
import Population as p

def driver(num_sorting_genomes, num_test_genomes, num_generations, list_length):
	max_fitness_per_generation = []
	sorting_genomes = [sg.SortingGenome(list_length=list_length) for x in range(num_sorting_genomes)]
	sort_test_genomes = [stg.SortTestGenome(list_length=list_length) for x in range(num_test_genomes)]
	population = p.Population(sorting_genomes, sort_test_genomes, sg.SortingGenome, stg.SortTestGenome)
	for gen_num in range(num_generations):
		population.next_generation()
		max_fit = -1.0
		max_fit_index = 0
		print 'entity fitness length is '
		print len(population.entities)
		for i in range(len(population.entity_fitness)):
			if(population.entity_fitness[i]>max_fit):
				max_fit = population.entity_fitness[i]
				max_fit_index = i

		max_fitness_per_generation.append([max_fit, population.entities[max_fit_index].genome])
		print 'Max fit genome is ' 
		print population.entities[max_fit_index].genome
		print 'Fitness is ' + str(max_fit)
		print 'Max fit genome length is '
		print str(len(population.entities[max_fit_index].genome))
		print 'max fit genome delete mutation rate is ' 
		print str(population.entities[max_fit_index].delete_mutation_rate)
		print 'max fit genome mutation rate is ' 
		print str(population.entities[max_fit_index].mutation_rate)
		print 'max fit genome add mutation rate is ' 
		print str(population.entities[max_fit_index].copy_mutation_rate)

		print gen_num
		print 'Test cases are: '
		for i in range(len(population.tests)):
			print population.tests[i].genome

	#for sorting_genome in population.entities:
		#print sorting_genome.genome
	max_fit = -1.0
	max_fit_index = 0.0
	for i in range(len(population.entity_fitness)):
		if(population.entity_fitness[i]>max_fit):
			max_fit = population.entity_fitness[i]
			max_fit_index = i
	print 'Max fit genome is ' 
	print population.entities[i].genome
	print 'Max fit genome length is '
	print len(population.entities[i].genome)

	return max_fitness_per_generation



