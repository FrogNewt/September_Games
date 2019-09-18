#!/usr/bin/env python3

import qg_game_5_cleaned_funcs as funcs
import qg_game_5_classes as classes
import random

starter_list = []
population_size = 1000
starter_species = "charizard"
starter_trait = "size"
starter_class = classes.Organism

pop_holder = classes.Population()


starter_population = funcs.create_ancestors(starter_list, population_size, starter_species, starter_trait, starter_class)

evaluated_starter_population = funcs.evaluate_population(starter_list, pop_holder, starter_species, starter_trait)


pop_holder.current_gen = pop_holder.before_selection_population

demo_death_array = [False, True, True, False, False, False, True, False, False, False]

# Breaks the population into ten tenths so that they're easily extended back into a list
def select_via_player(population, loss_array, pop_object):
	i = 0
	remainder_after_predation = []

	zero_to_ten = []
	ten_to_twenty = []
	twenty_to_thirty = []
	thirty_to_forty = []
	forty_to_fifty = []
	fifty_to_sixty = []
	sixty_to_seventy = []
	seventy_to_eighty = []
	eighty_to_ninety = []
	ninety_to_one_hundred = []

	pop_dict = {

	0 : zero_to_ten,
	1 : ten_to_twenty,
	2 : twenty_to_thirty,
	3 : thirty_to_forty,
	4 : forty_to_fifty,
	5 : fifty_to_sixty,
	6 : sixty_to_seventy,
	7 : seventy_to_eighty,
	8 : eighty_to_ninety,
	9 : ninety_to_one_hundred,
	}

	master_dummy = [
	zero_to_ten,
	ten_to_twenty,
	twenty_to_thirty,
	thirty_to_forty,
	forty_to_fifty,
	fifty_to_sixty,
	sixty_to_seventy,
	seventy_to_eighty,
	eighty_to_ninety,
	ninety_to_one_hundred
	]

	population.sort(key=lambda x: x.phenotypic_trait_value)

	dummy = []

	for i in range(len(master_dummy)):
		print(i)
		print(loss_array[i])
		if loss_array[i-1] == True:
			lower_bound = int(len(population)*((i)/10))
			print(lower_bound)
			upper_bound = int(len(population)*((i+1)/10))
			print(upper_bound)
			for g in range(lower_bound, upper_bound):
				master_dummy[i-1].append(population[g])

			remainder_after_predation.extend(master_dummy[i-1])

	
	

	#for individual in population:
	#	print("Sorted by trait value: ", individual.phenotypic_trait_value)


	"""for x in range(int(len(population)*0.1)):
		zero_to_ten.append(population[x])
		dummy.append(population[x])

	
	for x in range(int(len(population)*0.2)):
		if population[x] not in dummy:
			ten_to_twenty.append(population[x])
			dummy.append(population[x])

	for x in range(int(len(population)*0.3)):
		if population[x] not in dummy:
			twenty_to_thirty.append(population[x])
			dummy.append(population[x])


	for x in range(int(len(population)*0.4)):
		if population[x] not in dummy:
			thirty_to_forty.append(population[x])
			dummy.append(population[x])

	for x in range(int(len(population)*0.5)):
		if population[x] not in dummy:
			forty_to_fifty.append(population[x])
			dummy.append(population[x])
	
	for x in range(int(len(population)*0.6)):
		if population[x] not in dummy:
			fifty_to_sixty.append(population[x])
			dummy.append(population[x])


	for x in range(int(len(population)*0.7)):
		if population[x] not in dummy:
			sixty_to_seventy.append(population[x])
			dummy.append(population[x])


	for x in range(int(len(population)*0.8)):
		if population[x] not in dummy:
			seventy_to_eighty.append(population[x])
			dummy.append(population[x])

	for x in range(int(len(population)*0.9)):
		if population[x] not in dummy:
			eighty_to_ninety.append(population[x])
			dummy.append(population[x])

	for x in range(int(len(population))):
		if population[x] not in dummy:
			ninety_to_one_hundred.append(population[x])
			dummy.append(population[x])

	"""


	for i in range(len(loss_array)):
		if loss_array[i] == True:
			for each_list in master_dummy:
				for g in range(0, (len(each_list)-1), int(len(population)*0.01)):
					remainder_after_predation.append(each_list[g])

	print("Length of total population", len(population), "Length of 10% population", len(zero_to_ten))
	print("Length of 10-20:", len(ten_to_twenty))
	print("Length of 20-30:", len(twenty_to_thirty))
	print("Length of 30-40:", len(thirty_to_forty))
	print("Length of 40-50:", len(forty_to_fifty))
	print("Length of 50-60:", len(fifty_to_sixty))
	print("Length of 60-70:", len(sixty_to_seventy))
	print("Length of 70-80:", len(seventy_to_eighty))
	print("Length of 80-90:", len(eighty_to_ninety))
	print("Length of 90-100:", len(ninety_to_one_hundred))

	while len(remainder_after_predation) > 1000:
		for i in range(0, (len(remainder_after_predation))-1, 10):
			random_choice = random.randint(0, (len(remainder_after_predation)-1))
			remainder_after_predation.pop(random_choice)

	#for this_list in master_dummy:
	#	for individual in this_list:
	#		print(individual.phenotypic_trait_value)

	#for individual in remainder_after_predation:
	#	print(individual.phenotypic_trait_value)

	pop_holder.current_gen = remainder_after_predation
	print("Size of population ready to go: ", len(pop_holder.current_gen))





#select_via_player(starter_list, demo_death_array, pop_holder)

#print(len(remainder_list))

#funcs.reproduce(pop_holder, classes.Organism)

#print(len(pop_holder.current_gen))
#funcs.evaluate_population(pop_holder.current_gen, pop_holder, starter_species, starter_trait)

#for i in range(2):
#	print(pop_holder.mean_phenotypic_trait_value_list[i])

#### DEBUGGING ####
#genetic_differential = pop_holder.mean_breeding_value_list[1] - pop_holder.mean_breeding_value_list[0]
#selection_differential = pop_holder.mean_phenotypic_trait_value_list[1] - pop_holder.mean_phenotypic_trait_value_list[0]


#print(selection_differential*pop_holder.heritability_list[0])
#print(genetic_differential)

