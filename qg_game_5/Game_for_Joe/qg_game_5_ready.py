#!/usr/bin/env python3

import random
import numpy
import copy
from astropy.table import Table, Column

import qg_game_5_cleaned_funcs as funcs
import qg_game_5_classes as classes


# Checks whether or not the heritable component of the trait values is behaving as expected
# by the breeder's equation
def selection_debugger(pop_object):
	breeding_values = []

	for org in pop_object.current_gen:
		breeding_values.append(org.breeding_value)

	heritability = pop_object.heritability_list[len(pop_object.heritability_list)-1]
	selection_differential = pop_object.selection_differential_list[(len(pop_object.selection_differential_list)-1)]
	response_to_selection = pop_object.response_to_selection_list[(len(pop_object.response_to_selection_list)-1)]

	current_mean_breeding_value = numpy.mean(breeding_values)
	previous_mean_breeding_value = pop_object.mean_breeding_value_list[len(pop_object.mean_breeding_value_list)-2]
	actual_change = current_mean_breeding_value - previous_mean_breeding_value

	print("")
	print("########## DEBUGGER ##########")
	print("")
	print("Mean breeding value for the current generation: ", numpy.mean(breeding_values))
	print("Mean breeding value for the *previous* generation: ", pop_object.mean_breeding_value_list[len(pop_object.mean_breeding_value_list)-2])
	print("")
	print("Heritability: ", heritability)
	print("Selection Differential: ", selection_differential)
	print("")
	print("Response to Selection (predicted change): ", response_to_selection)
	print("Actual change: ", current_mean_breeding_value - previous_mean_breeding_value)
	print("")
	print("Difference between prediction and reality: ", response_to_selection - actual_change)
	print("")
	print("########## END DEBUGGER #########")
	print("")




# A "population" object that'll hold stats for every generation like means, variances, etc
pop_holder = classes.Population()

# The actual first population (a list of "organism"-class objects)
ancestral_population_list = []

# The starting population size--can be adjusted to suit your needs
ancestral_population_size = 10000

# The name of the species you're working with--this only matters for the simulation since the 
# graphical component will have its own...well...everything!
ancestral_species = "Gorilla"

# Choose a trait of interest--again, only valuable for the simulation since the graphical component has its
# own interface
ancestral_trait = "color"

# Choose the species of predator for the simulation
predator_species = "Gyarados"

# Create first ancestral population (slightly different because they have no existing parents to draw from)
funcs.create_ancestors(ancestral_population_list, ancestral_population_size, ancestral_species, ancestral_trait, classes.Organism)

# Evaluate population (again, slightly different since they don't have the same "previous generation" to evaluate)
funcs.evaluate_population(ancestral_population_list, pop_holder, ancestral_species, ancestral_trait)

# Generates the first load of predators
funcs.create_predators(pop_holder, pop_holder.predator_list, predator_species, classes.Organism)

# Has the ancestors encounter their first predators
funcs.encounter_predator(ancestral_population_list, pop_holder, pop_holder.predator_list)

# Produce offspring/a new generation
funcs.reproduce(pop_holder, classes.Organism)

# Check to see that the breeder's equation is predicting response to selection accurately
funcs.breeders_equation(pop_holder)


############ SECOND GENERATION (first gen after ancestors) ###############

for i in range(10):

	# Evaluate population (again, slightly different since they don't have the same "previous generation" to evaluate)
	funcs.evaluate_population(pop_holder.current_gen, pop_holder, ancestral_species, ancestral_trait)

	# Generates the first load of predators
	funcs.create_predators(pop_holder, pop_holder.predator_list, predator_species, classes.Organism)

	# Has the ancestors encounter their first predators
	funcs.encounter_predator(pop_holder.current_gen, pop_holder, pop_holder.predator_list)

	##### EVERYTHING'S FUNCTINOING PROPERLY UP TO THIS POINT #####

	# Produce offspring/a new generation
	funcs.reproduce(pop_holder, classes.Organism)

	#### THINGS ARE NO LONGER WORKING AS OF BREEDER'S EQUATION, SO SOMETHING'S WRONG WITH REPRODUCE ####
	#### THE ISSUE APPEARS TO BE WITH THE GENERATED BREEDING VALUES IN THE OFFSPRING GENERATION ####

	# Check to see that the breeder's equation is predicting response to selection accurately
	funcs.breeders_equation(pop_holder)


