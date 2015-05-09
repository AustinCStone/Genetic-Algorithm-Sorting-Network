import SortingGenome as sg
import SortTestGenome as stg
import Population as p

def driver(num_sorting_genomes, num_test_genomes, num_generations, list_length):
	sorting_genomes = [sg.SortingGenome(list_length=list_length) for x in range(num_sorting_genomes)]
	sort_test_genomes = [stg.SortTestGenome(list_length=list_length) for x in range(num_test_genomes)]
	population = p.Population(sorting_genomes, sort_test_genomes, sg.SortingGenome, stg.SortTestGenome)
	for gen_num in range(num_generations):
		population.next_generation()
		print gen_num
		
	for sorting_genome in population.entities:
		print sorting_genome.genome

