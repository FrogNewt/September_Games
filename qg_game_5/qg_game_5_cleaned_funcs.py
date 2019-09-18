#!/usr/bin/env python3

import random
import numpy
import copy


# Creates the ancestral generation
							#### CLEAR AND WORKING CORRECTLY ####
def create_ancestors(ancestor_list, population_size, given_species, given_trait, ancestor_class):
	for i in range(population_size):
		ancestor_list.append(ancestor_class())
	
	# Give each ancestor a trait and a value
	for ancestor in ancestor_list:
		ancestor.trait = given_trait
		ancestor.breeding_value = numpy.random.normal(0, numpy.sqrt(5))
		
		# Gives each ancestor a phenotype
		ancestor.phenotypic_trait_value = ancestor.breeding_value + numpy.random.normal(5, numpy.sqrt(1))
		if ancestor.phenotypic_trait_value < 0:
			ancestor.phenotypic_trait_value = 0.01

	test_genetic_mean = []
	test_phenotypic_mean = []

	for i in ancestor_list:
		test_genetic_mean.append(i.breeding_value)
		test_phenotypic_mean.append(i.phenotypic_trait_value)

	# Checking for consistency with below (consistent with evaluate population)
	print("")
	print("Genetic mean (in create ancestors): ", numpy.mean(test_genetic_mean))
	print("Additive genetic variance (in create ancestors): ", numpy.var(test_genetic_mean))
	print("Phenotypic mean (in create ancestors): ", numpy.mean(test_phenotypic_mean))
	print("Phenotypic variance (in create ancestors): ", numpy.var(test_phenotypic_mean))
	print("")

# Get data on the population generated and add values to the population-class object					
					#### CLEAR AND WORKING CORRECTLY IN ANCESTORS ####
def evaluate_population(current_pop_list, pop_object, species, trait):
	# Lists to store the breeding values and phenotypic values for use in generating means, variances
	# and other metrics
	print("")
	print("########## NEW GENERATION #############")
	print("")

	temp_breeding_values = []
	temp_phenotypic_trait_values = []

	# Aggregates all genetic and phenotypic values into lists to be used in calulating means and variances
	for organism in current_pop_list:
		temp_breeding_values.append(organism.breeding_value)
		temp_phenotypic_trait_values.append(organism.phenotypic_trait_value)

	# Temporary variables used to hold means and variances strictly within this function
	### ALL CONSISTENT WITH CREATE ANCESTORS ###
	temp_genetic_mean = numpy.mean(temp_breeding_values)
	print("")
	print("This generation's genetic mean (in evaluate population): ", temp_genetic_mean)
	temp_phenotypic_mean = numpy.mean(temp_phenotypic_trait_values)
	print("This generation's phenotypic mean (in evaluate population): ", temp_phenotypic_mean)
	temp_additive_genetic_variance = numpy.var(temp_breeding_values)
	temp_phenotypic_variance = numpy.var(temp_phenotypic_trait_values)

							##### CALCULATE HERITABILITY #####
	# Note: Heritability should be generated BEFORE predation (because selection will be accounted
	# for by the breeder's equation

	temp_heritability = temp_additive_genetic_variance / temp_phenotypic_variance
	print("Heritability: VA ({0}) / VP ({1}) = {2}!".format(temp_additive_genetic_variance, temp_phenotypic_variance, temp_heritability))
	print("")

			### BEGIN ACCRUING POPULATION STATS FOR THIS GENERATION ###

	# Adds the entire generation to the population object for later use
	pop_object.before_selection_population = current_pop_list

	# Add the mean breeding value for generation x to position x-1 in the list
	# (e.g. Generation "2" will be in position "1" in the list, etc)
	
	#### IMPORTANT NOTE: THE MEAN BREEDING VALUE IS APPENDED TO THIS LIST BACK IN THE 'REPRODUCE' FUNC
	#### THIS ALLOWS FOR THE PROPER EVALUATION OF RESPONSE TO SELECTION

	pop_object.mean_breeding_value_list.append(temp_genetic_mean)

	# Add the additive genetic variance
	pop_object.additive_genetic_variance_list.append(temp_additive_genetic_variance)

	# Add the phenotypic mean
	pop_object.mean_phenotypic_trait_value_list.append(temp_phenotypic_mean)

	# Add the phenotypic variance
	pop_object.phenotypic_variance_list.append(temp_phenotypic_variance)

	# Add the heritability
	pop_object.heritability_list.append(temp_heritability)

	### ALL POP_OBJECT ADDITIONS ARE CURRENTLY EQUIVALENT TO THOSE OF CREATE ANCESTORS ###

					
# Generate predators to encounter this generation/population of organisms
# Note: Predators are the chief selection agent acting on each population
						#### CLEAR AND WORKING CORRECTLY IN ANCESTORS ####
def create_predators(population_stats_holder, list_of_predators, predator_type, organism_class):

	# Currently gives the predator a trait value
	predator_value = population_stats_holder.mean_phenotypic_trait_value_list[len(population_stats_holder.mean_phenotypic_trait_value_list)-1]-1

	### DEBUGGING ###
	predator_value =8

	# Generates a predator (every organism will encounter this single predator)
	predator = organism_class()

	# Assigns the predator its phenotypic trait value (i.e. its ability to prey upon organisms)
	predator.phenotypic_trait_value = predator_value

	# Affixes population data into a population holder object
	population_stats_holder.predator_strength = predator_value

	# Adds predator type and the specific predator to the population object
	population_stats_holder.predator_type = predator_type
	population_stats_holder.predator_list.append(predator)



# Determines whether or not the organism survives an encounter with a predator; the "predator value" describes the value that the organism must exceed to survive its encounter with the predator
							 #### CLEAR AND WORKING CORRECTLY ####
def encounter_predator(population, pop_object, predator_list):
	# Will hold all dead individuals for processing (they'll be popped from the population list when killed)
	temp_dead = []

	# Will hold all surviving individuals for processing
	still_alive = []

	# Holds the "before selection" trait mean value to be used in the breeder's equation
	#### ALL CONSISTENT WITH PREVIOUS FUNCTIONS IN ANCESTORS ####
	pop_object.before_selection_trait_mean_list.append(pop_object.mean_phenotypic_trait_value_list[len(pop_object.mean_phenotypic_trait_value_list)-1])
	print("")
	print("Pop object mean phenotypic trait value (should be equivalent to above): ", pop_object.mean_phenotypic_trait_value_list[len(pop_object.mean_phenotypic_trait_value_list)-1])
	print("Before selection (phenotypic mean) list debugged (encounter predator): ", pop_object.before_selection_trait_mean_list[len(pop_object.before_selection_trait_mean_list)-1])
	print("(The above should be equal to the phenotypic mean above)")
	
	# Used to hold the trait values for the population before selection
	everybody_phenotypic_trait_values = []
	everybody_genetic_trait_values = []

	for i in population:
		everybody_phenotypic_trait_values.append(i.phenotypic_trait_value)
		everybody_genetic_trait_values.append(i.breeding_value)

	#### ALL CONSISTENT WITH PREVIOUS FUNCTIONS IN ANCESTORS ####
	print("")
	print("Before selection phenotypic trait mean: ", numpy.mean(everybody_phenotypic_trait_values))
	print("Before selection genetic trait mean: ", numpy.mean(everybody_genetic_trait_values))
	print("Before selection (population size): ", len(population))

	### USE THIS IN THE BREEDER'S EQUATION ###
	#### BREEDER'S EQUATION BEFORE AND EVERYBODY PHENOTYPIC TRAIT VALUES MEAN ARE EQUIVALENT IN ANCESTORS ####
	pop_object.BREEDERS_EQUATION_BEFORE = numpy.mean(everybody_phenotypic_trait_values)
	


	# Sets the predator equal to the length of the list--that means the most recently generated predator
	# Will be used against this population (and not the only that ate its parents or grandparents)
	predator = pop_object.predator_list[len(pop_object.predator_list)-1]
	
	# Has each organism encounter the predator
	for organism in population:
		if organism.phenotypic_trait_value >= predator.phenotypic_trait_value:
			organism.dead = False
		elif organism.phenotypic_trait_value < predator.phenotypic_trait_value:
			# Switches the organism to "dead" so that it won't be processed in breeding,
			# Even accidentally
			organism.dead = True


	# Check to see who's been killed this generation and append them to the appropriate lists
	i = 0
	for organism in population:
		if organism.dead == True:
			temp_dead.append(organism)

		elif organism.dead == False:
			still_alive.append(organism)

	
	
	# Adds the remaining living individuals to the pop_holder object
	pop_object.after_selection_population.append(still_alive)


	# Adds the dead individuals to the pop_holder object
	pop_object.dead_this_gen_list.append(temp_dead)

	# Makes the remaining individuals into a simple "parent_gen" variable usable by the "reproduce" function
	pop_object.current_gen = still_alive

	# Used to calculate the "after selection" trait mean value to be used in the breeder's equation
	still_alive_phenotypic_trait_values = []
	still_alive_genetic_trait_values = []

	# Gathers up all the phenotypic values of those who survived to generate the 
	# 'after selection' mean trait value for use in the breeder's equation
	for i in still_alive:
		still_alive_phenotypic_trait_values.append(i.phenotypic_trait_value)
		still_alive_genetic_trait_values.append(i.breeding_value)

	print("")
	print("Genetic mean after selection: ", numpy.mean(still_alive_genetic_trait_values))
	print("Phenotypic mean after selection: ", numpy.mean(still_alive_phenotypic_trait_values))
	print("After selection: ", len(still_alive))
	print("")

	# THE TWO VARIABLES BELOW ARE EQUIVALENT IN THE ANCESTRAL GENERATION
	pop_object.BREEDERS_EQUATION_AFTER = numpy.mean(still_alive_phenotypic_trait_values)

	# Sets the mean trait value after selection
	pop_object.after_selection_trait_mean_list.append(numpy.mean(still_alive_phenotypic_trait_values))
	



##### EVERYTHING'S WORKING BEAUTIFULLY WITH ANCESTORS THROUGH THIS POINT #####

def reproduce(pop_object, organism_class):
	
	# Makes a list to hold the new babies
	new_baby_list = []

	# Makes the parents easier to manipulate in the function
	parents = pop_object.current_gen

	# Start by checking to see that there are at least two organisms left
	if len(parents) < 2:
		return

	# Creates a shorthand for the additive genetic variance
	adv = pop_object.additive_genetic_variance_list[len(pop_object.additive_genetic_variance_list)-1]

	# Set the number of offspring for each individual to produce
	offspring_number = 2

	
	# Assign a random mate; check to see that no one mates with him/herself
	for parent in parents:
		while True:
			mate_choice = random.randint(0, len(parents)-1)
			mate_choice = parents[mate_choice]
			if mate_choice != parent:
				break

		# Produce a mid-parent value with partner
		mid_parent_value = (mate_choice.breeding_value + parent.breeding_value) / 2

		# Make the babies
		for i in range(offspring_number):
			
			# Give each baby a class equivalent to their parents' class
			new_baby = organism_class()

			### Everything's working up until the above (at least)! ###
			
			# Give the baby a breeding value equal to the mid-parent value plus a mendelian sampling deviation
			new_baby.breeding_value = mid_parent_value + numpy.random.normal(0, numpy.sqrt((adv/2)))

			# Give the baby a phenotypic value equal to the breeding value plus a deviation
			new_baby.phenotypic_trait_value = new_baby.breeding_value + numpy.random.normal(5, numpy.sqrt(1))

			# Adds the baby to the new population list
			new_baby_list.append(new_baby)

	##### DEBUGGING; CHANGE THIS INTO SOMETHING PERMANENT #####

	# Holds the genetic values of all offspring
	temp_offspring_genetic_values = []
	
	# Aggregates all genetic values into the above list
	for i in new_baby_list:
		temp_offspring_genetic_values.append(i.breeding_value)

	# Gets the mean (this is for use in the breeder's equation)
	temp_mean_offspring_genetic_value = numpy.mean(temp_offspring_genetic_values)

	# Adds to variable to be used in breeder's equation
	pop_object.offspring_genetic_mean = temp_mean_offspring_genetic_value

	# Updates this generation to be the "current generation"
	pop_object.current_gen = new_baby_list



#### WORKING PROPERLY WITH ANCESTORS ####
def breeders_equation(pop_obj):
	# Heritability * selection differential = response to selection


	# WORKING AND CONSISTENT WITH THE ABOVE FOR ANCESTORS; CORRECT IN SECOND GEN
	heritability = pop_obj.heritability_list[len(pop_obj.heritability_list)-1]


	# The difference between the mean phenotypic value before selection and the mean phenotypic value after selection
	selection_differential = pop_obj.BREEDERS_EQUATION_AFTER - pop_obj.BREEDERS_EQUATION_BEFORE
	print("AFTER SELECTION (breeder's equation): ", pop_obj.BREEDERS_EQUATION_AFTER)
	print("BEFORE SELECTION (breeder's equation): ", pop_obj.BREEDERS_EQUATION_BEFORE)


	# This is how much the average genetic values should change before and after selection from the ancestors to the offspring
	response_to_selection = heritability * selection_differential

	# A shorthand for the breeding value list
	bv_list = pop_obj.mean_breeding_value_list

######## IF THERE'S A PROBLEM, IT'S LIKELY GOING TO BE HERE WITHIN 'ACTUAL DIFFERENCE' WHERE 'OFFSPRING GENETIC MEAN' MAY NOT REPRESENT THE RIGHT GENERATION! ##########

	# The actual genetic difference
	actual_difference = pop_obj.offspring_genetic_mean - bv_list[len(bv_list)-1]

	# Difference between prediction and reality
	absolute_error = actual_difference - response_to_selection

	# The percent by which the two values differ
	percent_error = str(100 * (absolute_error / actual_difference))[:4]

	print("Response to selection: ", response_to_selection)
	print("Actual genetic difference between generations: ", actual_difference)
	print("Parent generation genetic mean: {0}, Offspring generation genetic mean: {1}.".format(bv_list[len(bv_list)-1], pop_obj.offspring_genetic_mean))
	print("Difference between prediction and actual genetic difference: {0} (or {1} %!)".format(absolute_error, percent_error)) 
	print(pop_obj.mean_breeding_value_list)




