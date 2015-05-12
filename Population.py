import random as r
import numpy as np

class Population:
	"""General class for maintaining a population of test and evaluator 'organisms' """
	def __init__(self, entities, tests, create_entity_f, create_test_f):
		self.entities = entities
		self.tests = tests
		self.entity_fitness = [0.0 for x in range(len(entities))]
		self.test_fitness = [0.0 for x in range(len(tests))]
		self.create_entity_f = create_entity_f
		self.create_test_f = create_test_f


	def next_generation(self):
		"""Breed, mutate, and repopulate tests and entities"""
		total_num_entities = len(self.entities)
		total_num_tests = len(self.tests)
		
		for entity_num in range(total_num_entities):
			self.entity_fitness[entity_num] = self.entities[entity_num].evaluateFitness(self.tests)
		
		for test_num in range(total_num_tests):
			self.test_fitness[test_num] = self.tests[test_num].evaluateFitness()

		next_generation_entities = [None for x in range(total_num_entities)]
		for i in range(total_num_entities):
			parent1_index = self.selectParent(self.entity_fitness)
			#print 'p1e ' + str(parent1_index)
			parent1 = self.entities[parent1_index]
			parent2_index = self.selectParent(self.entity_fitness, previous_parent_index = parent1_index )
			#print 'p2e ' + str(parent2_index)
			parent2 = self.entities[parent2_index]
			child_entity = self.create_entity_f(parent1 = parent1, parent2 = parent2)
			child_location = self.placeChild(parent1_index, parent2_index, next_generation_entities)
			#print 'child_location is ' + str(child_location)
			next_generation_entities[child_location] = child_entity
		self.entities = next_generation_entities


		next_generation_tests = []
		for i in range(total_num_tests):
			parent1_index = self.selectParent(self.test_fitness)
			#print 'p1t ' + str(parent1_index)
			parent1 = self.tests[parent1_index]
			parent2_index = self.selectParent(self.test_fitness)
			#print 'p2t ' + str(parent2_index)
			parent2 = self.tests[parent2_index]
			child_test = self.create_test_f(parent1 = parent1, parent2 = parent2)
			next_generation_tests.append(child_test)
		self.tests = next_generation_tests
		


	def selectParent(self, fitness_values, previous_parent_index=None):
		'''If previous_parent_index is passed in, it selects a mate within a standard deviation of 5 away in either direction from the 
		previous parent, else it selects anywhere from the population'''
		if previous_parent_index is None:
			rand_i = r.uniform(0, sum(fitness_values))
			current_sum = 0.0
			i = 0
			for fitness_val in fitness_values:
				current_sum += fitness_val
				if rand_i < current_sum: 
					return i
				i += 1
			return i
		else:
			num_fitness_values = len(fitness_values)
			mu, sigma = float(previous_parent_index), 10.0 # mean and standard deviation
			distance_away_can_mate = abs(int(np.random.normal(mu, sigma, 1))-int(mu)) #draw a random sample
			lower_index = (previous_parent_index-distance_away_can_mate)%num_fitness_values
			upper_index = (previous_parent_index+distance_away_can_mate)%num_fitness_values
			lower_half = []
			upper_half = []
			if(lower_index>previous_parent_index): #wrap around
				lower_half = fitness_values[lower_index:] + fitness_values[0:previous_parent_index]
			else: 
				lower_half = fitness_values[lower_index:previous_parent_index]
			
			if(upper_half<previous_parent_index): #wrap around
				upper_half =  fitness_values[previous_parent_index:] + fitness_values[0:upper_index]
			else:
				upper_half = fitness_values[previous_parent_index:upper_index]

			fitness_values_available_to_mate = list(lower_half+upper_half)
			rand_i = r.uniform(0, sum(fitness_values_available_to_mate))
			current_sum = 0.0
			i = 0
			for fitness_val in fitness_values_available_to_mate:
				current_sum += fitness_val
				if rand_i < current_sum: 
					return (lower_index+i)%num_fitness_values
				i += 1
			return (lower_index+i)%num_fitness_values

	def placeChild(self, parent1_index, parent2_index, next_generation_children):
		"""Place the child as close to the parents as possible. Assumes next_generation_children is populated 
		with None at locations that have not been taken yet"""
		average = (parent1_index + parent2_index)/2
		size_next_gen = len(next_generation_children)
		dist_away = 0
		while(dist_away<size_next_gen): 
			if(next_generation_children[(average+dist_away)%size_next_gen]==None):
				return (average+dist_away)%size_next_gen
			if(next_generation_children[(average-dist_away)%size_next_gen]==None):
				return (average-dist_away)%size_next_gen
			dist_away+=1
		raise Exception("Attempted to place child when the next generation population is already full")



