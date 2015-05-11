import matplotlib.pyplot as plt


def plotFitness(driver_output):
	generations = [x for x in range(len(driver_output))]
	fitness = [x[0] for x in driver_output]
	lineGraph(generations, fitness, xlabel='Generation Number', ylabel='Max Fit Genome Fitness', title='Fitness Over Time')


def plotGenomeLength(driver_output):
	generations = [x for x in range(len(driver_output))]
	genome_length = [len(x[1]) for x in driver_output]
	lineGraph(generations, genome_length, xlabel='Generation Number', ylabel='Max Fit Genome Length', title='Genome Length Over Time')


def lineGraph(x, y, xlabel=None, ylabel=None, title=None):
	plt.plot(x, y)
	if title is not None:
		plt.title(title) 
	if xlabel is not None:
		plt.xlabel(xlabel)	
	if ylabel is not None:
		plt.ylabel(ylabel) 
	plt.show()

