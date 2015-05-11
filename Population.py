import random as r

class Population:
	"""Class for maintaining a population of test and evaluator 'organisms' """
	def __init__(self, entities, tests, create_entity_f, create_test_f):
		print 'HERE!!!!! IN CONSTRUCTOR OF POPULATION'
		self.entities = entities
		self.tests = tests
		self.entity_fitness = [0.0 for x in range(len(entities))]
		self.test_fitness = [0.0 for x in range(len(tests))]
		self.create_entity_f = create_entity_f
		self.create_test_f = create_test_f


	def next_generation(self):
		total_num_entities = len(self.entities)
		total_num_tests = len(self.tests)
		
		for entity_num in range(total_num_entities):
			self.entity_fitness[entity_num] = self.entities[entity_num].evaluateFitness(self.tests)
		
		for test_num in range(total_num_tests):
			self.test_fitness[test_num] = self.tests[test_num].evaluateFitness()

		#create an array in which jump from element i to i+1 is equal to element i's fitness 
		total_entity_fitness = sum(self.entity_fitness)	
		entity_fitness_interpolate = [self.entity_fitness[0]/total_entity_fitness]
		for entity_num in range(1, total_num_entities):
			entity_fitness_interpolate.append( (self.entity_fitness[entity_num]/total_entity_fitness) \
				+ entity_fitness_interpolate[entity_num-1] )

		total_test_fitness = sum(self.test_fitness)
		test_fitness_interpolate = [self.test_fitness[0]/total_test_fitness]
		for test_num in range(1, total_num_tests):
			test_fitness_interpolate.append( (self.test_fitness[test_num]/total_test_fitness) \
				+ test_fitness_interpolate[test_num-1] )

		next_generation_entities = []
		for i in range(total_num_entities):
			parent1_index = self.selectParent(entity_fitness_interpolate)
			#print 'p1e'
			#print parent1_index
			parent1 = self.entities[parent1_index]
			parent2_index = self.selectParent(entity_fitness_interpolate)
			#print 'p2e'
			#print parent2_index
			parent2 = self.entities[parent2_index]
			new_entity = self.create_entity_f(parent1 = parent1, parent2 = parent2)
			next_generation_entities.append(new_entity)
		self.entities = next_generation_entities


		next_generation_tests = []
		for i in range(total_num_tests):
			parent1_index = self.selectParent(test_fitness_interpolate)
			#print 'p1t '
			#print parent1_index
			parent1 = self.tests[parent1_index]
			parent2_index = self.selectParent(test_fitness_interpolate)
			#print 'p2t '
			#print parent2_index
			parent2 = self.tests[parent2_index]
			new_test = self.create_test_f(parent1 = parent1, parent2 = parent2)
			next_generation_tests.append(new_test)
		self.tests = next_generation_tests
		


	def selectParent(self, fitness_interpolate):
		interpolate_value = r.random() * fitness_interpolate[-1]
		for i in range(len(fitness_interpolate)):
			if interpolate_value<fitness_interpolate[i]:
				return i
		#print 'here????'
		return len(fitness_interpolate)-1

		#standard binary search to select parent... Is log(n) the most optimal algorithm to sample population by fitness? 
		'''min_i = 0
		max_i = len(fitness_interpolate)
		mid_i = (max_i + min_i)/2
		while(max_i>=min_i):
			if (interpolate_value>fitness_interpolate[mid_i]):
				min_i = mid_i+1
				mid_i = (min_i + max_i)/2
			else: 
				max_i = mid_i-1
				mid_i = (min_i + max_i)/2
		##print 'selected parent ' + str(mid_i)
	#	#print 'parent fitness is ' + str(self.entity_fitness[mid_i]/sum(self.entity_fitness))
		return mid_i'''




