#!/usr/bin/env python3

import random
import numpy

### FUNCTIONS FOR USE IN GENERATING NUMBERS ###




# These functions produce a list that contains all instances of the trait described (i.e. every measurement from within the population)

def get_color_intensity_list(population_list):
	stored = []
	for pokemon in population_list:
		stored.append(pokemon.color_intensity)
	return stored

def get_adult_weight_list(population_list):
	stored = []
	for pokemon in population_list:
		stored.append(pokemon.adult_weight)
	return stored

def get_tail_flame_height_list(population_list):
	stored = []
	for pokemon in population_list:
		stored.append(pokemon.tail_flame_height)
	return stored

def get_moves_known_list(population_list):
	stored = []
	for pokemon in population_list:
		stored.append(pokemon.moves_known)
	return stored

def get_fecundity_list(population_list):
	stored = []
	for pokemon in population_list:
		stored.append(pokemon.fecundity)
	return stored


# These functions calculate the within-population averages of trait values

def calculate_average_color_intensity(population_list):
	storage = 0
	for pokemon in population_list:
		storage += pokemon.color_intensity
	avg_trait = storage / len(population_list)
	return avg_trait

def calculate_average_adult_weight(population_list):
	storage = 0
	for pokemon in population_list:
		storage += pokemon.adult_weight
	avg_trait = storage / len(population_list)
	return avg_trait

def calculate_average_tail_flame_height(population_list):
	storage = 0
	for pokemon in population_list:
		storage += pokemon.tail_flame_height
	avg_trait = storage / len(population_list)
	return avg_trait

def calculate_average_moves_known(population_list):
	storage = 0
	for pokemon in population_list:
		storage += pokemon.moves_known
	avg_trait = storage / len(population_list)
	return avg_trait

def calculate_average_fecundity(population_list):
	storage = 0
	for pokemon in population_list:
		storage += pokemon.fecundity
	avg_trait = storage / len(population_list)
	return avg_trait


### FUNCTIONS FOR USE IN GENERATING TRAITS ###

### Assigns Charizards their traits

def assign_traits(population_list, list_of_names, used_up_names, offspring_list, moms_list):
	i = 0
	for pokemon in population_list:
		pokemon.sex = random.randint(0,1)

		# Checks all traits that each Charizard instance possesses and assigns it a value
		for trait in pokemon.__dict__:
			trait_range = str(trait+"_range")
			if "moves_known" == trait:
				pokemon.__dict__[trait] = random.randint(pokemon.__dict__[trait_range][0], pokemon.__dict__[trait_range][1])
			elif hasattr(pokemon, trait_range):
				pokemon.__dict__[trait] = random.uniform(pokemon.__dict__[trait_range][0], pokemon.__dict__[trait_range][1])
			else:
				pass

		# Gives the pokemon a name from the master list
		pokemon.name = list_of_names[random.randint(0,len(list_of_names)-1)]
		
		# Checks to see if the pokemon's name ends in a vowel (or 'y') and if it does, ends the name in "zard"
		if pokemon.name[-1].lower() in ["a", "e", "i", "o", "u", "y"]:
			pokemon.name = pokemon.name + "zard"
			used_up_names.append(pokemon.name)
			#list_of_names.pop(list_of_names.index(pokemon.name[:-4]))
		
		# If the pokemon's name doesn't end in a vowel or 'y', it's given 'izard' for a cleaner-sounding name.
		else:
			pokemon.name = pokemon.name + "izard"
			used_up_names.append(pokemon.name)
			#list_of_names.pop(list_of_names.index(pokemon.name[:-5]))

		# Assign the non-continuous/non-float traits binary or integer values
		#pokemon.moves_known = random.randint(0,20)

		# Assigns an index based on whether or not the pokemon is a mother
		if not pokemon.is_mom:
			pokemon.index = i
		elif pokemon.is_mom:
			pokemon.mom_index = i

		# Checks to see who the moms_list and offspring_list are and assigns them to their respective lists
		if pokemon.is_mom:
			moms_list.append(pokemon)
		else:
			offspring_list.append(pokemon)
		
		# Increments forward
		i += 1

def generate_environments(environment_class, environment_list):
	temp_names = []
	for env in environment_class.env_names:
		temp_names.append(env)

	for environment in environment_class.env_names:
		new_env = environment_class()
		new_env.name = temp_names[random.randint(0, len(temp_names)-1)]
		temp_names.pop(temp_names.index(new_env.name))
		print(new_env.name)
		environment_list.append(new_env)
		for trait in new_env.__dict__.keys():
			if "_impact" in str(trait) and ("_range" not in str(trait)):
				trait_range = str(trait)+"_range"
				trait_range = new_env.__dict__[trait_range]
				print(trait_range)
				trait = random.uniform(trait_range[0], trait_range[1])
				print(trait)

		#print(environment_class.env_names)
	print(environment_list)


def assign_environments_to_moms(mothers, environment_class, environments_list):
	local_env_dict = {}
	i = 0
	env_names = []
	for environment in environments_list:
		env_names.append(environment.name)

	#print(env_names)

	for env in environments_list:
		local_env_dict[i] = env
		i += 1

	for mother in mothers:
		mother.env = random.randint(0, len(env_names)-1)
		mother.env = local_env_dict[mother.env]


def assign_birth_environments(offspring_list, mom_dictionary):
	for org in offspring_list:
		org.env_born = mom_dictionary[org.mom_identity].env



def assign_moms(offspring_list, moms_list):
	for baby in offspring_list:
		baby.mom_identity = random.randint(0, len(moms_list)-1)
		baby.mom_identity = moms_list[baby.mom_identity].name
		# Print statement used for debugging commented-out below
		#print("{0}'s mom is {1}!".format(baby.name, baby.mom_identity))



def add_maternal_effects(offspring_list, moms_dictionary, offspring_with_mom_effects_list):
# Changes each trait in each individual Charizard based on its maternal effects; this is confusing, so I'll break it down comment-by-comment
	for pokemon in offspring_list:

		# Looks at each trait in a single pokemon
		for trait in pokemon.__dict__:

			# Checks to see if the trait is in the "continuous traits" list
			if trait in pokemon.continuous_traits:

				# Sets the genetic trait value equal to the ORIGINAL trait value (what it was BEFORE mom or other influences)
				genetic_trait_value = pokemon.__dict__[trait]
				#print(trait,"base value: ", genetic_trait_value)

				# Checks to see that mom's identity is present in the mom_dict dictionary (it should be--all the  moms ought to be there)
				if pokemon.mom_identity in moms_dictionary.keys():

					# Creates a short-hand for ease of use--just reducing characters
					my_mom = pokemon.mom_identity
					#print(pokemon.mom_identity)

					# Looks at each character that mom possesses to check and see whether it's equal to the trait (+ "impact"--the attribute mom possesses will be "trait_impact") in question
					for attribute in moms_dictionary[my_mom].__dict__:
						if attribute == (trait + "_impact"):

							#print("The original trait value is: " + str(pokemon.__dict__[trait]))
							# If the offspring trait is equal to the mom's attribute, it assigns the value of the attribute to "mom's influence"
							moms_influence = moms_dictionary[my_mom].__dict__[attribute]
							#print("Mom's influence on ", trait, moms_influence)
							#print("Mom's influence (proportion): " + str(moms_influence))
							
							# Multiplies mom's influence by the genetic trait value to get a fraction of the original value
							mom_effect = moms_influence*genetic_trait_value
							#print("Mom's effect: ", mom_effect)
							#print("Mom's actual effect: " + str(mom_effect))
							
							# Gives the total after mom's addition
							new_total = mom_effect + genetic_trait_value
							#print("New total value: ", new_total)
							#print("The new trait value: " + str(new_total))
							
							# Replaces the old trait value with the new total for the pokemon (offspring)
							pokemon.__dict__[trait] = new_total
							#print("All this pokemon's traits: ")
							#for trait in pokemon.__dict__:
							#	print(trait, pokemon.__dict__[trait])
							offspring_with_mom_effects_list.append(pokemon)


def add_environmental_effects(offspring_list, moms_dictionary, offspring_with_env_effects_list):
# Changes each trait in each individual Charizard based on the environment in which it was reared; this is confusing, so I'll break it down comment-by-comment
# IMPORTANT NOTE: With respect to this game, maternal effects are added first, so this function should accept POST-maternal-effect offspring trait values (and not strictly genetic-effect trait values)
	for pokemon in offspring_list:

		# Looks at each trait in a single pokemon
		for trait in pokemon.__dict__:

			# Checks to see if the trait is in the "continuous traits" list
			if trait in pokemon.continuous_traits:

				# Sets the genetic trait value equal to the ORIGINAL trait value (what it was BEFORE environmental influences)
				gen_and_mom_trait_value = pokemon.__dict__[trait]
				print("")
				print("Starting at", trait, gen_and_mom_trait_value)


### NOTE: ALL CODE ABOVE APPLIES TO BOTH MATERNAL AND ENVIRONMENTAL EFFECTS, BUT THE CODE BELOW IS SPECIFIC TO ENVIRONMENTAL EFFECTS--BE SURE TO CHANGE IT ###

				# Checks to see that mom's identity is present in the mom_dict dictionary (it should be--all the  moms ought to be there)
				if pokemon.mom_identity in moms_dictionary.keys():

					# Creates a short-hand for ease of use--just reducing characters
					my_mom = moms_dictionary[pokemon.mom_identity]
					print(my_mom.env.name)

					# Looks at each character that mom possesses to check and see whether it's equal to the trait (+ "impact"--the attribute mom possesses will be "trait_impact") in question
					for attribute in my_mom.env.__dict__:
						#print(attribute)
						if attribute == (trait + "_impact"):
							#print(attribute)
							#print("The original trait value is: " + str(pokemon.__dict__[trait]))
							# If the offspring trait is equal to the mom's attribute, it assigns the value of the attribute to "mom's influence"
							attribute_range = str(attribute) + "_range"
							attribute_range = my_mom.env.__dict__[attribute_range]
							attribute = random.uniform(attribute_range[0], attribute_range[1])

							env_influence = attribute
							
							print("Env's influence (proportion): " + str(env_influence))
							
							# Multiplies mom's influence by the genetic trait value to get a fraction of the original value
							env_effect = env_influence*gen_and_mom_trait_value
							#print("Mom's effect: ", mom_effect)
							print("Env's actual effect: " + str(env_effect))
							
							# Gives the total after mom's addition
							new_total = env_effect + gen_and_mom_trait_value
							#print("New total value: ", new_total)
							print("The new trait value: " + str(new_total))
							
							# Replaces the old trait value with the new total for the pokemon (offspring)
							pokemon.__dict__[trait] = new_total
							#print("All this pokemon's traits: ")
							#for trait in pokemon.__dict__:
							#	print(trait, pokemon.__dict__[trait])
							offspring_with_env_effects_list.append(pokemon)



# Assigns motherhood randomly; for any pokemon assigned motherhood, changes class to "Momizard"

def give_mom_class(population_list, used_class):
	while True:
		temp_moms = []
		for pokemon in population_list:
			if pokemon.sex == 0:
				mom_roll = random.randint(0,5)
				if mom_roll == 1:
					pokemon.is_mom = True
				if pokemon.is_mom == True:
					saved = pokemon.name
					saved_mom = pokemon.is_mom
					population_list.pop(population_list.index(pokemon))
					new_mom = used_class()
					new_mom.name = saved
					new_mom.is_mom = saved_mom
					population_list.append(new_mom)
					temp_moms.append(new_mom)

		# Guarantees that there are at least five moms in the starting population (i.e. five families)
		i = 0
		for pokemon in population_list:
			if pokemon.is_mom == True:
				i += 1
		if i >= 5:
			break


def get_generation_stats(single_generation, readability_dictionary):
	i = 0
	choice_dict = {}
	for trait_string in single_generation.keys():
		for trait_link_string in readability_dictionary.keys():
			if trait_string==trait_link_string:
				choice_dict[i] = trait_string
				print(readability_dictionary[trait_link_string].title(), "(Index: " + str(i)+ ")")
				i += 1
	while True:
		print("Which trait are you interested in?  (Choose the index from the choices listed above or type 'done'!)")
		user_input = input("")
		if 'done' in user_input:
			break
		for choice in choice_dict:
			if user_input == str(choice):
				number = single_generation[choice_dict[int(user_input)]]
				if isinstance(number, int):
					single_generation[choice_dict[int(user_input)]] = str(single_generation[choice_dict[int(user_input)]])[:4]
				elif isinstance(number, float):
					single_generation[choice_dict[int(user_input)]] = str(single_generation[choice_dict[int(user_input)]])[:4]
				print("The {0} in this population: {1}!".format(readability_dictionary[trait_link_string].title(), single_generation[choice_dict[int(user_input)]]))

			#print("The ", generation[measurement], "is ", choice_dict[user_input])
		

### END FUNCTIONS ###


### END FUNCTIONS ###