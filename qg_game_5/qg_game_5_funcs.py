#!/usr/bin/env python3

import random
import numpy
import copy

# Creates the ancestral generation
def create_ancestors(ancestor_list, population_size, given_species, given_trait, trait_mean, ancestor_class):
	for i in range(population_size):
		ancestor_list.append(ancestor_class())
	
	# Debugging
	mean_genotype = []
	mean_phenotype = []
	
	for ancestor in ancestor_list:
		ancestor.trait = given_trait
		ancestor.genetic_trait_value = numpy.random.normal(0, numpy.sqrt(5))
		# Ancestors don't need a phenotype if you're not doing anything with them
		ancestor.phenotypic_trait_value = ancestor.genetic_trait_value + trait_mean
		# Add environmental/maternal effects to these as well
		ancestor.species = given_species
		mean_genotype.append(ancestor.genetic_trait_value)
		mean_phenotype.append(ancestor.phenotypic_trait_value)



	print("Mean genotype: ", numpy.mean(mean_genotype))
	print("Mean phenotype: ", numpy.mean(mean_phenotype))

	# This is working properly
	print("")
	print("################### BEGIN ANCESTORS ###################")
	print("")
	print("There are {0} ancestral {1}!".format(len(ancestor_list), given_species))

# Gets the stats of the ancestral generation
def evaluate_ancestors(ancestor_list, population_stats_holder, species, trait):
	temp_genetic_trait_values = []
	temp_phenotypic_trait_values = []



	for ancestor in ancestor_list:
		temp_genetic_trait_values.append(ancestor.genetic_trait_value)
		temp_phenotypic_trait_values.append(ancestor.phenotypic_trait_value)
	
	new_genetic_mean = numpy.mean(temp_genetic_trait_values)
	new_additive_genetic_variance = numpy.var(temp_genetic_trait_values)

	new_phenotypic_mean = numpy.mean(temp_phenotypic_trait_values)
	new_phenotypic_variance = numpy.var(temp_phenotypic_trait_values)

	population_stats_holder.mean_genetic_trait_value = new_genetic_mean
	population_stats_holder.additive_genetic_variance = new_additive_genetic_variance

	population_stats_holder.mean_phenotypic_trait_value = new_phenotypic_mean
	population_stats_holder.phenotypic_variance = new_phenotypic_variance

	population_stats_holder.mean_genetic_trait_value_list.append(new_genetic_mean)
	population_stats_holder.mean_phenotypic_trait_value_list.append(new_phenotypic_mean)
	population_stats_holder.additive_genetic_variance_list.append(new_additive_genetic_variance)
	population_stats_holder.phenotypic_variance_list.append(new_phenotypic_variance)

	population_stats_holder.trait = trait
	population_stats_holder.species = species

	population_stats_holder.population_size = len(ancestor_list)
	population_stats_holder.population_size_list.append(len(ancestor_list))


	print("The ancestral genetic mean in {0} for {1} is {2} and the additive genetic variance is {3}!".format(population_stats_holder.species, population_stats_holder.trait, population_stats_holder.mean_genetic_trait_value, population_stats_holder.additive_genetic_variance))
	print("")
	print("The ancestral phenotypic mean in {0} for {1} is {2} and the phenotypic variance is {3}!".format(population_stats_holder.species, population_stats_holder.trait, population_stats_holder.mean_phenotypic_trait_value, population_stats_holder.phenotypic_variance))

# Gets the stats of the ancestral generation
def evaluate_population(pop_list, population_stats_holder, species, trait):
	temp_genetic_trait_values = []
	temp_phenotypic_trait_values = []

	if len(pop_list) > 1:
		# Iterates through all organisms and creates a list of values to be used in calculating variances
		for organism in pop_list:
			temp_genetic_trait_values.append(organism.genetic_trait_value)
			temp_phenotypic_trait_values.append(organism.phenotypic_trait_value)
			

		# Calculates the genetic mean and additive genetic variance
		new_genetic_mean = numpy.mean(temp_genetic_trait_values)
		new_additive_genetic_variance = numpy.var(temp_genetic_trait_values)

		print("Genetic mean: ", new_genetic_mean)
		print("VA:", new_additive_genetic_variance)
		print("")
		# Calculates the phenotypic mean and phenotypic variance (includes maternal and environmental effects)
		new_phenotypic_mean = numpy.mean(temp_phenotypic_trait_values)
		print("Phenotypic mean: ", new_phenotypic_mean)
		new_phenotypic_variance = numpy.var(temp_phenotypic_trait_values)
		print("VP:", new_phenotypic_variance)

		# Calculate the heritability of the trait
		if not (new_additive_genetic_variance or new_phenotypic_variance) == 0:
			heritability = new_additive_genetic_variance / new_phenotypic_variance
		else:
			return

		#### NOTE:  YOU'VE GOT THE HERITABILITY BEING CALCULATED IN THE WRONG PLACE--THIS NEEDS TO BE
		#### DONE *AFTER* PREDATORS ENCOUNTER THE POPULATION SO THAT THE POPULATION YOU'RE BREEDING
		#### IS THE POPULATION YOU'RE EVALUATING FOR HERITABILITY; PERHAPS CREATE CATEGORIES
		#### FOR BEFORE SELECTION/AFTER SELECTION

		population_stats_holder.heritability = heritability
		population_stats_holder.mean_genetic_trait_value = new_genetic_mean
		population_stats_holder.additive_genetic_variance = new_additive_genetic_variance
		population_stats_holder.mean_phenotypic_trait_value = new_phenotypic_mean
		population_stats_holder.phenotypic_variance = new_phenotypic_variance
		population_stats_holder.trait = trait
		population_stats_holder.species = species

		population_stats_holder.heritability_list.append(heritability)
		population_stats_holder.mean_genetic_trait_value_list.append(new_genetic_mean)
		population_stats_holder.additive_genetic_variance_list.append(new_additive_genetic_variance)
		population_stats_holder.mean_phenotypic_trait_value_list.append(new_phenotypic_mean)
		population_stats_holder.phenotypic_variance_list.append(new_phenotypic_variance)

		print("The population genetic mean in {0} for {1} is {2} and the additive genetic variance is {3}!".format(population_stats_holder.species, population_stats_holder.trait, population_stats_holder.mean_genetic_trait_value, population_stats_holder.additive_genetic_variance))
		print("")
		print("The population phenotypic mean in {0} for {1} is {2} and the phenotypic variance is {3}!".format(population_stats_holder.species, population_stats_holder.trait, population_stats_holder.mean_phenotypic_trait_value, population_stats_holder.phenotypic_variance))

		print("The heritability of this trait is {0}.".format(population_stats_holder.heritability))
		print("")



	print("Phenotypic trait value at the point of evaluation: ", pop_list[5].phenotypic_trait_value)

### BREEDING VALUES ARE ALL MESSED-UP RIGHT NOW ###

# Gets the breeding values for the individuals in the population
def calculate_breeding_values(population, population_stats_holder):
	for organism in population:
		organism.breeding_value = organism.genetic_trait_value
		# Erased the subtraction of the genetic mean from the genetic trait value here because
		# the breeding value is just the genetic value and doesn't need to be modified further
		
		

# Adds maternal effects to the phenotype of the organism		
def calculate_maternal_effects(population, population_stats_holder):
	for organism in population:
		organism.phenotypic_trait_value = organism.phenotypic_trait_value + (organism.phenotypic_trait_value * organism.dam.maternal_effect)
		organism.genetic_and_maternal_trait_value = organism.phenotypic_trait_value
	print("Trait value after maternal effects: ", population[5].phenotypic_trait_value)

# Adds environmental effects to phenotype.  NOTE:  Maternal effects function should be run first in order to apply both effects properly
def calculate_environmental_effects(population, population_stats_holder):
	for organism in population:
		environmental_effects = numpy.random.uniform(-0.5, 0.5)
		organism.phenotypic_trait_value = organism.phenotypic_trait_value + (organism.phenotypic_trait_value*environmental_effects)
		organism.genetic_and_environmental_trait_value = organism.phenotypic_trait_value + (organism.phenotypic_trait_value+environmental_effects)
	
	print("Trait value after environmental effects: ", population[5].phenotypic_trait_value)

def run_breeders_equation(population, population_stats_holder):

	current_gen_genetic_mean = population_stats_holder.mean_genetic_trait_value_list[len(population_stats_holder.mean_genetic_trait_value_list)-1]	
	previous_gen_genetic_mean = population_stats_holder.mean_genetic_trait_value_list[len(population_stats_holder.mean_genetic_trait_value_list)-2]

	current_gen_phenotypic_mean = population_stats_holder.mean_phenotypic_trait_value_list[len(population_stats_holder.mean_phenotypic_trait_value_list)-1]
	previous_gen_phenotypic_mean = population_stats_holder.mean_phenotypic_trait_value_list[len(population_stats_holder.mean_phenotypic_trait_value_list)-2]

	print(current_gen_phenotypic_mean)
	print(previous_gen_phenotypic_mean)
	

	# SELECTION DIFFERENTIAL IS CURRENTLY WRONG #

	selection_differential = current_gen_phenotypic_mean - previous_gen_phenotypic_mean
	heritability = population_stats_holder.heritability_list[len(population_stats_holder.heritability_list)-1]

	response_to_selection = selection_differential*heritability

	population_stats_holder.response_to_selection_list.append(response_to_selection)

	print("Previous trait mean (G): ", previous_gen_genetic_mean)
	print("Current trait mean (G): ", current_gen_genetic_mean)

	print("Previous trait mean (P): ", previous_gen_phenotypic_mean)
	print("Current trait mean (P): ", current_gen_phenotypic_mean)
	print("")
	print("Response to selection: ", response_to_selection)



# Produces the GP gen based on the breeding values of the ancestral generation
def produce_new_gen(ancestor_list, new_gen_list, organism_class, population_stats_holder):
	# Empty lists to sort out males and females
	dams = []
	sires = []



	# This is working properly
	#print("Starting out, there are {0} in the ancestor list!".format(len(ancestor_list)))

	for ancestor in ancestor_list:
		ancestor.sex = random.randint(0,1)
		if ancestor.sex == 1:
			sires.append(ancestor)
		elif ancestor.sex == 0:
			dams.append(ancestor)
	
	ancestor_list = []

	if (len(dams) or len(sires)) == 0:
		population_stats_holder.viable = False
		return

	for dam in dams:
		if dam.dead == False:
			if len(sires) > 0:
				dam.mate = sires[random.randint(0, len(sires)-1)]
				# An arbitrary quantity of offspring that replaces both mother and father; can be amended
				offspring = 2
				for i in range(offspring):
					new_baby = organism_class()
					new_baby.dam = dam
					new_baby.species = dam.species
					# Establishes the mid-parent value: the population mean plus the sum of the deviations of the parents divided by two (quantity of parents)
					mid_parent_value = (dam.breeding_value + dam.mate.breeding_value) / 2
					
					# Establishes the baby's trait value by drawing from a normal distribution with a mean centered at the mid-parent value and a standard deviation of half the additive genetic variance
					new_baby.genetic_trait_value = numpy.random.normal(mid_parent_value, numpy.sqrt((population_stats_holder.additive_genetic_variance/2)))
					new_baby.phenotypic_trait_value = new_baby.genetic_trait_value + population_stats_holder.mean_phenotypic_trait_value
					if new_baby.phenotypic_trait_value <= 0:
						new_baby.phenotypic_trait_value = 0
					
					# Prevents the trait value from falling below zero (absent trait)
					#if new_baby.genetic_trait_value < 0:
					#	new_baby.genetic_trait_value = 0

					# Adds new baby to the list
					new_gen_list.append(new_baby)

	# Resets the dam and sire lists for future use
	dams = []
	sires = []
	# Gives population holder object the population size
	population_stats_holder.population_size = len(new_gen_list)
	population_stats_holder.population_size_list.append(len(new_gen_list))
			

def create_predators(population_stats_holder, predator_list, predator_type, organism_class):
	# Multiplies the random float generated by the predator value by a random integer (arbitrary; can be modified)
	predator_multiplier = random.randint(1,3)

	# Currently gives the predator a pseudo-random strength (this can be modified)
	predator_value = random.uniform(population_stats_holder.mean_genetic_trait_value, population_stats_holder.mean_genetic_trait_value*predator_multiplier)
	predator_value = 6
	# Produces predators with trait values and species
	for i in range(population_stats_holder.population_size):
		# Makes the predator an organism
		new_predator = organism_class()

		# Assigns the predator a species
		new_predator.species = predator_type

		# Sets the predator's trait value--this value will compete with the focal organism's trait value to determine if the focal organism is eaten
		# Predators currently have a trait value sampled from a normal distribution centered around the randomly-drawn trait value above with a standard deviation of 1
		
		### USE THE LINE BELOW TO GET VARIABLE PREDATORS TAKEN FROM A NORMAL DISTRIBUTION AROUND A MEAN
		#new_predator.genetic_trait_value = numpy.random.normal(predator_value)
		new_predator.phenotypic_trait_value = predator_value

		if new_predator.phenotypic_trait_value >= 0:
			pass

		# Adds the predator to a master list of predators
		predator_list.append(new_predator)

	# Affixes population data into a population holder object
	population_stats_holder.predator_strength = predator_value
	population_stats_holder.predator_type = predator_type

### NOTE: PREDATORS ARE CURRENTLY ONLY WORKING PROPERLY IN THE FIRST GENERATION ###

# Determines whether or not the organism survives an encounter with a predator; the "predator value" describes the value that the organism must exceed to survive its encounter with the predator
def encounter_predator(population, population_stats_holder, predator_list):
	length_before = len(population)


	temp_dead = []
	i = 0


	prey_genetic_list = []
	prey_phenotypic_list = []

	population_stats_holder.after_selection_trait_mean = numpy.mean(prey_phenotypic_list)
	
	for organism in population:
		i += 1
		predator_choice = random.randint(0, len(predator_list)-1)
		predator = predator_list[predator_choice]

#### WHAT IS THE DEAL WITH THIS WEIRDNESS?!  I NEED TO GET THE PRE-PREDATION POPULATION FOR USE IN THE SELECTION DIFFERENTIAL! ####		


		if organism.phenotypic_trait_value > predator.phenotypic_trait_value:
			organism.dead = True
			temp_dead.append(organism)
		else:
			prey_genetic_list.append(organism.genetic_trait_value)
			prey_phenotypic_list.append(organism.phenotypic_trait_value)
	for organism in temp_dead:
		if organism in population:
			population.pop(population.index(organism))
			#print(len(population))

	print("Length before predation: ", length_before)
	print("Length after predation: ", len(population))
	print("")
	print("These guys are going on to reproduce:")
	print("Test genetic mean (after murders): ",numpy.mean(prey_genetic_list))
	print("Test phenotypic mean (after murders): ", numpy.mean(prey_phenotypic_list))



	
	
	print("Predator value was {0} this generation!".format(population_stats_holder.predator_strength))


	print("It looks like {0} of the {1} {2} were killed by the {3} this time!".format(len(temp_dead), len(population_stats_holder.before_selection_population)+len(temp_dead), population_stats_holder.species, population_stats_holder.predator_type))










