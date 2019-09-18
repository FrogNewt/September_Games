#!/usr/bin/env python3

import random
import qg_game_5_classes as game_classes
import qg_game_5_funcs as game_funcs
from astropy.table import Table, Column
import os




### UNCOMMENT ALL OF THE BELOW TO HAVE USER-GENERATED VALUES FOR ORGANISMS/PREDATORS, ETC ###
### BE SURE TO COMMENT-OUT EITHER USER-GENERATED VALUES *OR* STATIC VALUES--CHOOSE ONE OR THE OTHER ###

###### USER-GENERATED VALUES ######

"""
print("What do you want this species to be?")
species_choice = input("")
print(species_choice)

print("What trait do you want to look at?")
trait_choice = input("")
print(trait_choice)

print("Who do you want their predators to be?")
predator_name = input("")
print(predator_name)

print("What do you want the minimum trait value to be in the ancestors?")
trait_minimum = int(input(""))
print(trait_minimum)

print("...and the maximum (still in the ancestors?)")
trait_maximum = int(input(""))
print(trait_maximum)

print("Finally--how many individuals do you want to start with? (give a population size!)")
population_size = int(input(""))
print(population_size)
"""

##### STATIC ANCESTRAL VALUES (these don't take user-input) #####

species_choice = "Newts"
trait_choice = "tails"
predator_name = "Frogs"
trait_mean = 5
population_size = 10000


# Creates an empty list to hold the dynamically generated ancestors
ancestors = []

# Creates an empty list to hold the GP generation (as produced by the function below)
GP_gen = []

# Creates an empty list to hold the P generation
P_gen = []

# Creates an empty list to hold the F1 generation
F1_gen = []

# Creates an empty list to hold predators
predators = []

# Generates an instance of the "Population" class to hold stats
pop_holder = game_classes.Population()





# Generates ancestors
game_funcs.create_ancestors(ancestors, population_size, species_choice, trait_choice, trait_mean, game_classes.AncestorMom)

# Gets the "stats" for the ancestors
game_funcs.evaluate_ancestors(ancestors, pop_holder, species_choice, trait_choice)

# Gets the ancestral breeding values
game_funcs.calculate_breeding_values(ancestors, pop_holder)


game_funcs.create_predators(pop_holder, predators, predator_name, game_classes.Organism)

game_funcs.encounter_predator(ancestors, pop_holder, predators)

print("")
print("############## ANCESTORS DONE ###############")
print("")

generation_list = []

prev_gen = ancestors
new_gen = []

g = 0

for i in range(20):
	if pop_holder.viable == True:
		print("")
		print("######### GENERATION {0} BEFORE SELECTION (BELOW) #########".format(g+1))
		print("")
		game_funcs.produce_new_gen(prev_gen, new_gen, game_classes.Organism, pop_holder)
		game_funcs.calculate_breeding_values(new_gen, pop_holder)
		game_funcs.calculate_maternal_effects(new_gen, pop_holder)
		game_funcs.calculate_environmental_effects(new_gen, pop_holder)
		game_funcs.evaluate_population(new_gen, pop_holder, species_choice, trait_choice)
		game_funcs.create_predators(pop_holder, predators, predator_name, game_classes.Organism)
		game_funcs.encounter_predator(new_gen, pop_holder, predators)
		print("")
		print("############## RESPONSE TO SELECTION IN GENERATION {0} #############".format(g+1))
		print("")
		print(game_funcs.run_breeders_equation(prev_gen, pop_holder))
		if len(new_gen) == 0:
			print("You've gone extinct!")
		prev_gen = new_gen
		generation_list.append(prev_gen)

		new_gen = []

		g += 1



"""
# Produces a GP generation given the breeding values of the ancestral generation
game_funcs.produce_new_gen(ancestors, GP_gen, game_classes.Organism, pop_holder)

# Gets the breeding values of the GP generation
game_funcs.calculate_breeding_values(GP_gen, pop_holder)

# Calculates the maternal effects on all organisms in the population
game_funcs.calculate_maternal_effects(GP_gen, pop_holder)

# Calculates the environmental effects on all organisms in the population
game_funcs.calculate_environmental_effects(GP_gen, pop_holder)

# Evalutes the GP population
game_funcs.evaluate_population(GP_gen, pop_holder, species_choice, trait_choice)

# Creates a population of predators equal to those in the population
game_funcs.create_predators(pop_holder, predators, predator_name, game_classes.Organism)

# Determines who survives predator encounters to reproduce this next generation
game_funcs.encounter_predator(GP_gen, pop_holder, predators)
print("Predators had a trait value of {0} and prey had an average value of {1} this time!".format(pop_holder.predator_strength, pop_holder.mean_phenotypic_trait_value))

"""

#### ADDITIONAL GENERATIONS--SHOULD NOT BE NECESSARY; CODE SOMETHING THAT INCREMENTS INFINITE GENERATIONS AT REQUEST ####

"""
# Produces a P generation given the breeding values of the GP generation
game_funcs.produce_new_gen(GP_gen, P_gen, game_classes.Organism, pop_holder)

# Gets the breeding values of the P generation
game_funcs.calculate_breeding_values(P_gen, pop_holder)

# Evalutes the P population
game_funcs.evaluate_population(P_gen, pop_holder, species_choice, trait_choice)

# Creates a population of predators equal to those in the population
game_funcs.create_predators(pop_holder, predators, predator_name, game_classes.Organism)

# Determines who survives predator encounters to reproduce this next generation
game_funcs.encounter_predator(P_gen, pop_holder, predators)
print("Predators had a trait value of {0} this time!".format(pop_holder.predator_strength))


# Produces a F1 generation given the breeding values of the ancestral generation
game_funcs.produce_new_gen(P_gen, F1_gen, game_classes.Organism, pop_holder)

# Gets the breeding values of the F1 generation
game_funcs.calculate_breeding_values(F1_gen, pop_holder)

# Evalutes the F1 population
game_funcs.evaluate_population(F1_gen, pop_holder, species_choice, trait_choice)

# Creates a population of predators equal to those in the population
game_funcs.create_predators(pop_holder, predators, predator_name, game_classes.Organism)

# Determines who survives predator encounters to reproduce this next generation
game_funcs.encounter_predator(F1_gen, pop_holder, predators)
print("Predators had a mean trait value of {0} this time!".format(pop_holder.predator_strength))
"""

### DEBUGGER; JUST CHECKS THE GENETIC AND PHENOTYPIC VALUES ###
#for organism in GP_gen:
#	print("This is a {0}.  It has a genetic trait value of {1} and a phenotypic value of {2} with maternal effects contributing {3}.".format(
#																	organism.species, organism.genetic_trait_value, organism.phenotypic_trait_value, (organism.genetic_trait_value*organism.dam.maternal_effect)))

#print(pop_holder.heritability_list)



#print(len(new_gen))
predator_strengths = []
generations = []
g = 1
for i in range(len(pop_holder.mean_phenotypic_trait_value_list)):
	generations.append(g)
	g+=1
	predator_strengths.append(pop_holder.predator_strength)

pop_holder.response_to_selection_list.insert(0, "NA")

pop_holder.heritability_list.insert(0, "NA")
new_h = []
new_va = []
new_vp = []
new_gen_mean = []
new_r = []
new_phen_mean = []

for va in pop_holder.additive_genetic_variance_list:
	va = str(va)[:6]
	new_va.append(va)

for vp in pop_holder.additive_genetic_variance_list:
	vp = str(vp)[:6]
	new_vp.append(vp)

for mean in pop_holder.mean_genetic_trait_value_list:
	mean = str(mean)[:6]
	new_gen_mean.append(mean)

for mean in pop_holder.mean_phenotypic_trait_value_list:
	mean = str(mean)[:6]
	new_phen_mean.append(mean)

for r in pop_holder.response_to_selection_list:
	r = str(r)[:5]
	new_r.append(r)


for h in pop_holder.heritability_list:
	h = str(h)[:5]
	new_h.append(h)

print("")



t = Table([generations, pop_holder.population_size_list, new_phen_mean, new_gen_mean, predator_strengths, new_va, new_vp, new_h, new_r],
	names=('Gen', 'Pop Size', 'Phen Means', "Gen Means", 'Pred Value', 'VA', 'VP', 'H^2', "R"))
t.pprint(max_lines = 100, max_width = 100)


