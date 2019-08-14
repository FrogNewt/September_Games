#!/usr/bin/env python3

import sys
import random
import numpy

from functions_for_qg_game_4 import *
#from qg_game_4_lists_and_dicts import *
from qg_game_4_classes import *
from qg_game_4_interactions import *

#import qg_game_4_lists_and_dicts as l_and_d

# 


"""Pokemon Preserve

Years ago, when big corporations began construction on natural Charizard habitats, you and many other conservationists
set out to rescue the Charizards and recolonized them in the Pokemon Preserve, a vast, multi-environment safe-haven for pokemon!

Now, those Charizards have given rise to the next generation, but the offspring they've produced are VERY different from what we'd expect!
The Preserve has tasked you with uncovering the mystery--how did we get so many crazy Charizards?!
"""




pop_holder_object = popHolder()





pop_holder_object.generations = []
pop_holder_object.readability_dict = {}


i = len(pop_holder_object.generations)

print(i)

def produce_population(pop_holder):

	i = len(pop_holder.generations)

	### BEGIN ONE-TIME PROCESSES ###


	if i==0:

		### IMPORTANT LISTS ###

		# A master list to hold all pokemon generated initially (unseparated into parents/offspring)
		pop_list = []



		# A list to contain all moms
		moms = []

		# A mechanism to link moms in the master list to their names
		mom_dict = {}


		# A list of all environment instances derived from the "Environment" class
		environments = []

		# A mechanism to link environments in the master list to their names
		env_dict = {}

		# A list to contain all offspring
		offspring = []

		# A master list of all available names
		name_list = [
		"barry",
		"henry",
		"tyrone",
		"jenny",
		"shamia",
		"sasquatch",
		"hyerin",
		"oboku",
		"jiwon",
		"hanzhou",
		"matt",
		"veronica",
		"delaware",
		"lloyd",
		"buster",
		"gob",
		"stefanos",
		"daenerys",
		"draco",
		"lucius",
		"heimer",
		"drax",
		"thor",
		"zealand",
		"flamington",
		"lord flamesworth",
		"shannon",
		"duke",
		"robin",
		"max power",
		"homer",
		"hercules",
		"stan",
		"lewis",
		"emerson",
		"brady",
		"shaniqua",
		"amanda",
		"bronson",
		"harrington",
		"bro",
		"d'fwan",
		"matt",
		"iwo",
		"phyllis",
		"gorgon",
		"munchy",
		"nemo",
		"wakanda",
		"panther",
		"charles"
		]

		# A list to hold names that have been 'popped' out of the master name list
		used_names = []


		# Different environment names
		env_names = [
		"desert",
		"forest",
		"prairie",
		"wetland",
		"mountains"
		]


		# Creates a list that includes genetic and maternal effects
		offspring_with_maternal_effects = []

		offspring_with_maternal_and_env_effects = []







		### END IMPORTANT LISTS ###


		# Reset all relevant lists and dicts
		offspring = []
		offspring_with_maternal_effects = []
		used_names = []
		moms = []
		mom_dict = {}
		


		# Creates 25 unique Charizards--not yet assigned parent of offspring status
		for i in range(len(name_list)-1):
			pop_list.append(Charizard())




		# Assign new 'mom' classes to moms
		give_mom_class(pop_list, Momizard)


		# Assign traits to individuals
		assign_traits(pop_list, name_list, used_names, offspring, moms)



		# Generate a mother's contribution (based on a random distribution)
		for mom in moms:
			for trait in mom.__dict__:
				if trait in mom.traits_of_impact:
					trait_range = str(trait+"_range")
					trait = random.uniform(mom.__dict__[trait_range][0], mom.__dict__[trait_range][1])



		# Assign moms to offspring
		assign_moms(offspring, moms)


		# Prints pokemon's stats--mostly for debugging right now.
		"""for pokemon in pop_list:
			print("Name: " + pokemon.name.title())
			if pokemon.is_mom == False:
				for trait in pokemon.__dict__:
					if "range" not in trait and (trait in pokemon.continuous_traits):
						if isinstance(pokemon.__dict__[trait], float):
							print(trait.title() + ":", str(pokemon.__dict__[trait])[:4])
						#elif str(trait) == "is_mom":
						#	pass
						else:	
							print(trait.title() + ":", str(pokemon.__dict__[trait]).title())
			print("")
			"""

		# Creates a list to hold the unaltered genetic-only trait-values of organisms
		offspring_without_maternal_effects = offspring

		# Counts the number of moms and offspring (for debugging)
		#print("There are " + str(len(moms)) + " mothers and " + str(len(offspring)) + " offspring!")
		#print("")

		# Generate lists that represent a single trait value for each individual in the population
		color_intensity_list_for_VA = get_color_intensity_list(offspring)
		adult_weight_list_for_VA = get_adult_weight_list(offspring)
		tail_flame_height_list_for_VA = get_tail_flame_height_list(offspring)
		moves_known_list_for_VA = get_moves_known_list(offspring)
		fecundity_list_for_VA = get_fecundity_list(offspring)


		# Since 'moves known' has to round to a whole number, all its elements get converted to integers
		moves_known_list_for_VA = list(map(int, moves_known_list_for_VA))


		# Calculates the average values (strictly genetic) for traits among offspring
		avg_genetic_color_intensity = calculate_average_color_intensity(offspring)
		avg_genetic_adult_weight = calculate_average_adult_weight(offspring)
		avg_genetic_tail_flame_height = calculate_average_tail_flame_height(offspring)
		avg_genetic_fecundity = calculate_average_fecundity(offspring)	
		avg_genetic_moves_known = calculate_average_moves_known(offspring)
		avg_genetic_moves_known = int(avg_genetic_moves_known)

		# Calculates the additive genetic variance with respect to a given trait within a population of offspring
		color_intensity_VA = numpy.var(color_intensity_list_for_VA)
		adult_weight_VA = numpy.var(adult_weight_list_for_VA)
		tail_flame_height_VA = numpy.var(tail_flame_height_list_for_VA)
		fecundity_VA = numpy.var(fecundity_list_for_VA)
		moves_known_VA = numpy.var(moves_known_list_for_VA)


		# Adds all moms to the mom-dictionary as key-value pairs where the 'key' is the mom's name and the value is the Momizard instance
		for mom in moms:
			mom_dict[mom.name] = mom


		# Creates an empty list (note: this SHOULD be available from "lists-and-dicts" but a bug has rendered that list null in the context of the 'main' function)
		offspring_with_maternal_effects = []


		generate_environments(Environment, environments)

		add_maternal_effects(offspring, mom_dict, offspring_with_maternal_effects)

		offspring_with_maternal_effects = list(set(offspring_with_maternal_effects))

		assign_environments_to_moms(moms, Environment, environments)


		assign_birth_environments(offspring_with_maternal_effects, mom_dict)

		add_environmental_effects(offspring_with_maternal_effects, mom_dict, offspring_with_maternal_and_env_effects)





			# Adds the pokemon to a new, updated list of offspring
			#offspring_with_maternal_effects.append(pokemon)

		# Get lists of individual trait values with just genetic and maternal effects

		color_intensity_list_for_VA_and_ma = get_color_intensity_list(offspring_with_maternal_effects)
		adult_weight_list_for_VA_and_ma = get_adult_weight_list(offspring_with_maternal_effects)
		tail_flame_height_list_for_VA_and_ma = get_tail_flame_height_list(offspring_with_maternal_effects)
		fecundity_list_for_VA_and_ma = get_fecundity_list(offspring_with_maternal_effects)
		moves_known_list_for_VA_and_ma = get_moves_known_list(offspring_with_maternal_effects)

		# Since 'moves known' has to round to a whole number, all its elements get converted to integers
		moves_known_list_for_VA_and_ma = list(map(int, moves_known_list_for_VA_and_ma))


		# Get averages that include genetic and maternal effects
		avg_gen_and_ma_color_intensity = calculate_average_color_intensity(offspring_with_maternal_effects)
		avg_gen_and_ma_adult_weight = calculate_average_adult_weight(offspring_with_maternal_effects)
		avg_gen_and_ma_tail_flame_height = calculate_average_tail_flame_height(offspring_with_maternal_effects)
		avg_gen_and_ma_fecundity = calculate_average_fecundity(offspring_with_maternal_effects)
		avg_gen_and_ma_moves_known = calculate_average_moves_known(offspring_with_maternal_effects)

		# Since 'moves known' has to round to a whole number, all its elements get converted to integers
		avg_gen_and_ma_moves_known = int(avg_gen_and_ma_moves_known)


		color_intensity_list_for_VA_and_ma_and_env = get_color_intensity_list(offspring_with_maternal_and_env_effects)
		adult_weight_list_for_VA_and_ma_and_env = get_adult_weight_list(offspring_with_maternal_and_env_effects)
		tail_flame_height_list_for_VA_and_ma_and_env = get_tail_flame_height_list(offspring_with_maternal_and_env_effects)
		fecundity_list_for_VA_and_ma_and_env = get_fecundity_list(offspring_with_maternal_and_env_effects)
		moves_known_list_for_VA_and_ma_and_env = get_moves_known_list(offspring_with_maternal_and_env_effects)

		# Since 'moves known' has to round to a whole number, all its elements get converted to integers
		moves_known_list_for_VA_and_ma_and_env = list(map(int, moves_known_list_for_VA_and_ma_and_env))


		# Get averages that include genetic and maternal effects
		avg_gen_and_ma_and_env_color_intensity = calculate_average_color_intensity(offspring_with_maternal_and_env_effects)
		avg_gen_and_ma_and_env_adult_weight = calculate_average_adult_weight(offspring_with_maternal_and_env_effects)
		avg_gen_and_ma_and_env_tail_flame_height = calculate_average_tail_flame_height(offspring_with_maternal_and_env_effects)
		avg_gen_and_ma_and_env_fecundity = calculate_average_fecundity(offspring_with_maternal_and_env_effects)
		avg_gen_and_ma_and_env_moves_known = calculate_average_moves_known(offspring_with_maternal_and_env_effects)

		# Since 'moves known' has to round to a whole number, all its elements get converted to integers
		avg_gen_and_ma_moves_known = int(avg_gen_and_ma_and_env_moves_known)





		print("There are currently {0} Charizards in this population!".format(len(offspring)))

		#print(len(offspring), "offspring")
		#print(len(name_list), "name list")
		#print(len(offspring_with_maternal_effects), "offspring_with_maternal_effects")
		#print(len(used_names), "used_names")
		#print(len(pop_list), "pop_list")
		#print(len(moms), "moms")
		males = []
		females = []
		for pokemon in offspring_with_maternal_effects:
			if pokemon.sex == 0:
				females.append(pokemon)
			if pokemon.sex == 1:
				males.append(pokemon)
		print("There are {0} males and {1} females in this population!".format(len(males), len(females)))

		ready_population = offspring_with_maternal_and_env_effects
		pop_holder.next_up_population = ready_population

		generation_data = {
			"pop_list": pop_list,
			"moms": moms,
			"mom_dict": mom_dict,
			"offspring": offspring,
			"name_list" : name_list,
			"used_names" : used_names,
			"env_names" : env_names,
			"offspring_with_maternal_effects" : offspring_with_maternal_effects,
			"offspring_with_maternal_and_env_effects" : offspring_with_maternal_and_env_effects,
			"color_intensity_list_for_VA" : color_intensity_list_for_VA,
			"adult_weight_list_for_VA" : tail_flame_height_list_for_VA,
			"moves_known_list_for_VA" : moves_known_list_for_VA,
			"fecundity_list_for_VA" : fecundity_list_for_VA,
			"ready_population" : ready_population,

			"avg_genetic_color_intensity" : avg_genetic_color_intensity,
			"avg_genetic_adult_weight" : avg_genetic_adult_weight,
			"avg_genetic_tail_flame_height" : avg_genetic_tail_flame_height,
			"avg_genetic_fecundity" : avg_genetic_fecundity,
			"avg_genetic_moves_known" : avg_genetic_moves_known,
			"avg_genetic_moves_known" : avg_genetic_moves_known,

			"color_intensity_VA" : color_intensity_VA,
			"adult_weight_VA" : adult_weight_VA,
			"tail_flame_height_VA" : tail_flame_height_VA,
			"fecundity_VA" : fecundity_VA,
			"moves_known_VA" : moves_known_VA,

			"color_intensity_list_for_VA_and_ma" : color_intensity_list_for_VA_and_ma,
			"adult_weight_list_for_VA_and_ma" : adult_weight_list_for_VA_and_ma,
			"tail_flame_height_list_for_VA_and_ma" : tail_flame_height_list_for_VA_and_ma,
			"fecundity_list_for_VA_and_ma" : fecundity_list_for_VA_and_ma,
			"moves_known_list_for_VA_and_ma" : moves_known_list_for_VA_and_ma,

			"color_intensity_list_for_VA_and_ma_and_env" : color_intensity_list_for_VA_and_ma_and_env,
			"adult_weight_list_for_VA_and_ma_and_env" : adult_weight_list_for_VA_and_ma_and_env,
			"tail_flame_height_list_for_VA_and_ma_and_env" : tail_flame_height_list_for_VA_and_ma_and_env,
			"fecundity_list_for_VA_and_ma_and_env" : fecundity_list_for_VA_and_ma_and_env,
			"moves_known_list_for_VA_and_ma_and_env" : moves_known_list_for_VA_and_ma_and_env,

			"avg_gen_and_ma_color_intensity" : avg_gen_and_ma_color_intensity,
			"avg_gen_and_ma_adult_weight" : avg_gen_and_ma_adult_weight,
			"avg_gen_and_ma_tail_flame_height" : avg_gen_and_ma_tail_flame_height,
			"avg_gen_and_ma_fecundity" : avg_gen_and_ma_fecundity,
			"avg_gen_and_ma_moves_known" : avg_gen_and_ma_moves_known,

			"avg_gen_and_ma_and_env_color_intensity" : avg_gen_and_ma_and_env_color_intensity,
			"avg_gen_and_ma_and_env_adult_weight" : avg_gen_and_ma_and_env_adult_weight,
			"avg_gen_and_ma_and_env_tail_flame_height" : avg_gen_and_ma_and_env_tail_flame_height,
			"avg_gen_and_and_env_ma_fecundity" : avg_gen_and_ma_and_env_fecundity,
			"avg_gen_and_and_env_ma_moves_known" : avg_gen_and_ma_and_env_moves_known

			}


		readability_dict = {

			"avg_genetic_color_intensity": "average color intensity due to genes",
			"avg_genetic_adult_weight": "average adult weight due to genes",
			"avg_genetic_tail_flame_height": "average tail flame height due to genes",
			"avg_genetic_fecundity": "average fecundity due to genes",
			"avg_genetic_moves_known": "average number of moves known due to genes",

			"color_intensity_VA" : "additive genetic variance in color intensity",
			"adult_weight_VA" : "additive genetic variance in adult weight",
			"tail_flame_height_VA" : "additive genetic variance in tail flame height",
			"fecundity_VA" : "additive genetic variance in fecundity",
			"moves_known_VA" : "additive genetic variance in moves known",

			"avg_gen_and_ma_color_intensity" : "The average combined genetic and maternal effects on color intensity",
			"avg_gen_and_ma_adult_weight" : "The average combined genetic and maternal effects on color adult weight",
			"avg_gen_and_ma_tail_flame_height" : "The average combined genetic and maternal effects on color tail flame height",
			"avg_gen_and_ma_fecundity" : "The average combined genetic and maternal effects on fecundity",
			"avg_gen_and_ma_moves_known" : "The average combined genetic and maternal effects on moves known",

			"avg_gen_and_ma_and_env_color_intensity" : "Color intensity including genetic, maternal, and environmental effects",
			"avg_gen_and_ma_and_env_adult_weight" : "Adult Weight including genetic, maternal, and environmental effects",
			"avg_gen_and_ma_and_env_tail_flame_height" : "Tail flame height including genetic, maternal, and environmental effects",
			"avg_gen_and_and_env_ma_fecundity" : "Total fecundity including genetic, maternal, and environmental effects",
			"avg_gen_and_and_env_ma_moves_known" : "The number of moves known including genetic, maternal, and environmental effects"
		}

			
			


		pop_holder.generations.append(generation_data)
		pop_holder.readability_key = readability_dict

	
	
	elif i > 0:
	
		predator_list = []
		master_list = []
		this_gen = pop_holder.next_up_population
		new_gen = []



		for i in range(len(this_gen)-1):
			predator = Predator()
			predator_list.append(predator)

		

		dead_charizards = 0

		for org in this_gen:
			roll = random.randint(0,1)
			if roll == 0:
				random_predator = predator_list[random.randint(0,len(predator_list)-1)]
				meet_predator(org, random_predator)
			elif roll ==1:
				reproduce(org, new_gen, Charizard)
			if org.dead == True:
				dead_charizards += 1
				this_gen.pop(this_gen.index(org))
		
		print("This time, {0} charizards died!".format(dead_charizards))
		print("Your population was able to produce {0} new babies!".format(len(new_gen)))

		print("There are {0} charizards left in your population!".format(len(this_gen)))
		for org in this_gen:
			print(org.defense)
		






while True:
	print("Do you want to produce a population?")
	user_input = input("")
	if 'y' in user_input:
		produce_population(pop_holder_object)
		print("Do you want to set them free and see how they do?")
		user_input = input("")
		if 'y' in user_input:
			print("Ok!  Let's do it!")
			produce_population(pop_holder_object)
	else:
		break



print("Do you want to look at the generations you've produced?")
user_input = input("")
if 'y' in user_input and pop_holder_object.generations:
	while True:
		print("Which generation do you want to look at? (Choose a number 1-{0} or 'quit'!)".format(len(pop_holder_object.generations)))
		user_input = input("")
		if 'quit' in user_input:
			break
		elif not user_input.isdigit():
			print("Whoops--that's not a number!")
		elif int(user_input) in range(0, len(pop_holder_object.generations) + 1):
			gen_number = int(user_input)-1
			print(len(pop_holder_object.generations))
			generation_choice = pop_holder_object.generations[gen_number]
			get_generation_stats(generation_choice, pop_holder_object.readability_key)
			#get_generation_stats(gen_number)
		else:
			print("You don't have that many generations--try again!")
elif not pop_holder_object.generations:
	print("You haven't made any generations yet!")
else:
	pass