def testSortingGenome(sorting_genome, list_length):
	test_list = [0 for x in range(list_length)]
	for i in range(2**list_length):
		test_list = map(int,list(bin((1<<list_length)+i))[-list_length:])
		correct_solution = sorted(test_list)
		gene_length = 2
		output = list(test_list)
		for gene_num in range((len(sorting_genome)/2)):
			position1 = sorting_genome[gene_num*gene_length]
			position2 = sorting_genome[gene_num*gene_length + 1]
			if output[position1] > output[position2]:
				output[position1], output[position2] = output[position2], output[position1] 
		break_flag = False
		for i in range(len(output)):
			if output[i] is not correct_solution[i]:
				break_flag = True
				
		if break_flag:
			print 'output is ' 
			print output
			print 'test list is '
			print correct_solution
			return False



	print 'Correct Solution!'
	return True

def testAllGenomes(driver_output, list_length):
	for gen in driver_output:
		if(testSortingGenome(gen[1], list_length)):
			print 'Correct genome!'
			print gen[0]
			print gen[1]
			print 'Genome length is '
			print len(gen[1])
