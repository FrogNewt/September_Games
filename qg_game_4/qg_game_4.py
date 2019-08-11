#!/usr/bin/env python3

import random
import numpy

# Pokemon Preserve

# Years ago, when big corporations began construction on natural Charizard habitats, you and many other conservationists
# set out to rescue the Charizards and recolonized them in the Pokemon Preserve!

# Now, those Charizards have given rise to the next generation, but the offspring they've produced are VERY different from what we'd expect!
# The Preserve has tasked you with uncovering the mystery--how did we get so many crazy Charizards?!



### IMPORTANT LISTS ###

# A master list to hold all pokemon generated initially (unseparated into parents/offspring)
pop_list = []



# A list to contain all moms
moms = []

# A mechanism to link moms in the master list to their names
mom_dict = {}

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

### END IMPORTANT LISTS ###




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

### END FUNCTIONS ###
 

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

### END FUNCTIONS ###
 


### CLASSES ###

class Environment(object):
	def __init__(self, name = "default environment", adult_weight_impact = 1, color_intensity_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1):
		self.name = name
		self.adult_weight_impact = weight_impact
		self.color_intensity_impact = color_impact
		self.tail_flame_height_impact = tail_flame_height_impact
		self.moves_known_impact = moves_known_impact


# Creates a Charizard object--mothers and offspring both begin as an instance of this class, but mothers will adopt a second class
class Charizard(object):
	def __init__(self, name = "default", color_intensity = 5, adult_weight = 10, tail_flame_height = 30, moves_known = 4):
		self.name = name

		# Gives the color of the Charizard on a spectrum of hues
		self.color_intensity = color_intensity
		self.color_intensity_range = [0,10]
		
		# Gives the adult weight of the charizard in kg
		self.adult_weight = adult_weight
		self.adult_weight_range = [1,50]
		
		# Gives the tail-flame height of the charizard in cm
		self.tail_flame_height = tail_flame_height
		self.tail_flame_height_range = [10,50]

		# Gives the quantity of abilities this Charizard is born able to perform (measured in its own units)
		self.moves_known = moves_known
		self.moves_known_range = [1,10]

		# Tells us who this charizard's mother is
		self.mom_identity = ""

		# Describes the environment in which this Charizard was raised
		self.raised_environment = ""

		# Determines whether or not this Charizard is a mom--note: all "moms" will be reassigned to "Momizard" class
		self.is_mom = False

		# Keeps track of which Charizard is which numerically (simpler than names for use in organizing them later)
		self.index = ""

		self.continuous_traits = [
		"color_intensity",
		"adult_weight",
		"tail_flame_height",
		"moves_known"
		]


class Momizard(object):
	def __init__(self, offspring = "default offspring", name = "default name", adult_weight_impact = 1, color_intensity_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1):
		super().__init__()
		self.name = name
		self.adult_weight_impact = adult_weight_impact
		self.adult_weight_impact_range = [-1,1]
		
		self.color_intensity_impact = color_intensity_impact
		self.color_intensity_impact_range = [-0.2,0.2]
		
		self.tail_flame_height_impact = tail_flame_height_impact
		self.tail_flame_height_impact_range = [-1,1]
		
		self.moves_known_impact = moves_known_impact
		self.moves_known_impact_range = [-1,1]

		self.index = "has a 'mom' index"
		self.traits_of_impact = [
		"weight_impact",
		"adult_weight_impact",
		"tail_flame_height_impact",
		"moves_known_impact"
		]


### END CLASSES ###


### BEGIN ONE-TIME PROCESSES ###



# Creates 25 unique Charizards--not yet assigned parent of offspring status
for i in range(len(name_list)-1):
	pop_list.append(Charizard())


# Assigns motherhood randomly; for any pokemon assigned motherhood, changes class to "Momizard"
for pokemon in pop_list:
	mom_roll = random.randint(0,5)
	if mom_roll == 1:
		pokemon.is_mom = True
	if pokemon.is_mom == True:
		saved = pokemon.name
		saved_mom = pokemon.is_mom
		pop_list.pop(pop_list.index(pokemon))
		new_mom = Momizard()
		new_mom.name = saved
		new_mom.is_mom = saved_mom
		pop_list.append(new_mom)


### Assigns Charizards their traits
i = 0
for pokemon in pop_list:

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
	pokemon.name = name_list[random.randint(0,len(name_list)-1)]
	
	# Checks to see if the pokemon's name ends in a vowel (or 'y') and if it does, ends the name in "zard"
	if pokemon.name[-1].lower() in ["a", "e", "i", "o", "u", "y"]:
		pokemon.name = pokemon.name + "zard"
		used_names.append(pokemon.name)
		name_list.pop(name_list.index(pokemon.name[:-4]))
	
	# If the pokemon's name doesn't end in a vowel or 'y', it's given 'izard' for a cleaner-sounding name.
	else:
		pokemon.name = pokemon.name + "izard"
		used_names.append(pokemon.name)
		name_list.pop(name_list.index(pokemon.name[:-5]))

	# Assign the non-continuous/non-float traits binary or integer values
	#pokemon.moves_known = random.randint(0,20)

	# Assigns an index based on whether or not the pokemon is a mother
	if not pokemon.is_mom:
		pokemon.index = i
	elif pokemon.is_mom:
		pokemon.mom_index = i

	# Checks to see who the moms and offspring are and assigns them to their respective lists
	if pokemon.is_mom:
		moms.append(pokemon)
	else:
		offspring.append(pokemon)
	
	# Increments forward
	i += 1




# Generate a mother's contribution (based on a random distribution)
for mom in moms:
	for trait in mom.__dict__:
		if trait in mom.traits_of_impact:
			trait_range = str(trait+"_range")
			trait = random.uniform(mom.__dict__[trait_range][0], mom.__dict__[trait_range][1])



# Assign moms to offspring
for baby in offspring:
	baby.mom_identity = random.randint(0, len(moms)-1)
	baby.mom_identity = moms[baby.mom_identity].name
	# Print statement used for debugging commented-out below
	#print("{0}'s mom is {1}!".format(baby.name, baby.mom_identity))





# Prints pokemon's stats--mostly for debugging right now.
for pokemon in pop_list:
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


offspring_without_maternal_effects = offspring

# Counts the number of moms and offspring (for debugging)
print("There are " + str(len(moms)) + " mothers and " + str(len(offspring)) + " offspring!")
print("")

# Generate lists that represent a single trait value for each individual in the population
color_intensity_list_for_VA = get_color_intensity_list(offspring)
adult_weight_list_for_VA = get_adult_weight_list(offspring)
tail_flame_height_list_for_VA = get_tail_flame_height_list(offspring)


moves_known_list_for_VA = get_moves_known_list(offspring)

# Since 'moves known' has to round to a whole number, all its elements get converted to integers
moves_known_list_for_VA = list(map(int, moves_known_list_for_VA))


# Calculates the average values (strictly genetic) for traits among offspring
avg_genetic_color_intensity = calculate_average_color_intensity(offspring)
avg_genetic_adult_weight = calculate_average_adult_weight(offspring)
avg_genetic_tail_flame_height = calculate_average_tail_flame_height(offspring)
avg_genetic_moves_known = calculate_average_moves_known(offspring)
avg_genetic_moves_known = int(avg_genetic_moves_known)

# Calculates the additive genetic variance with respect to a given trait within a population of offspring
color_intensity_VA = numpy.var(color_intensity_list_for_VA)
adult_weight_VA = numpy.var(adult_weight_list_for_VA)
tail_flame_height_VA = numpy.var(tail_flame_height_list_for_VA)
moves_known_VA = numpy.var(moves_known_list_for_VA)


# Adds all moms to the mom-dictionary as key-value pairs where the 'key' is the mom's name and the value is the Momizard instance
for mom in moms:
	mom_dict[mom.name] = mom

#print(mom_dict)

# Creates a list that includes genetic and maternal effects
offspring_with_maternal_effects = []



# Changes each trait in each individual Charizard based on its maternal effects; this is confusing, so I'll break it down comment-by-comment
for pokemon in offspring:

	# Looks at each trait in a single pokemon
	for trait in pokemon.__dict__:

		# Checks to see if the trait is in the "continuous traits" list
		if trait in pokemon.continuous_traits:

			# Sets the genetic trait value equal to the ORIGINAL trait value (what it was BEFORE mom or other influences)
			genetic_trait_value = pokemon.__dict__[trait]
			print(trait, genetic_trait_value)

			# Checks to see that mom's identity is present in the mom_dict dictionary (it should be--all the  moms ought to be there)
			if pokemon.mom_identity in mom_dict.keys():

				# Creates a short-hand for ease of use--just reducing characters
				my_mom = pokemon.mom_identity
				print(pokemon.mom_identity)

				# Looks at each character that mom possesses to check and see whether it's equal to the trait (+ "impact"--the attribute mom possesses will be "trait_impact") in question
				for attribute in mom_dict[my_mom].__dict__:
					if attribute == (trait + "_impact"):

						#print("The original trait value is: " + str(pokemon.__dict__[trait]))
						# If the offspring trait is equal to the mom's attribute, it assigns the value of the attribute to "mom's influence"
						moms_influence = mom_dict[my_mom].__dict__[attribute]
						print("Mom's influence: ", moms_influence)
						#print("Mom's influence (proportion): " + str(moms_influence))
						
						# Multiplies mom's influence by the genetic trait value to get a fraction of the original value
						mom_effect = moms_influence*genetic_trait_value
						print("Mom's effect: ", mom_effect)
						#print("Mom's actual effect: " + str(mom_effect))
						
						# Gives the total after mom's addition
						new_total = mom_effect + genetic_trait_value
						print("New total value: ", new_total)
						#print("The new trait value: " + str(new_total))
						
						# Replaces the old trait value with the new total for the pokemon (offspring)
						pokemon.__dict__[trait] = new_total
						#print("All this pokemon's traits: ")
						#for trait in pokemon.__dict__:
						#	print(trait, pokemon.__dict__[trait])
						offspring_with_maternal_effects.append(pokemon)


#offspring_with_maternal_effects = list(set(offspring_with_maternal_effects))


	# Adds the pokemon to a new, updated list of offspring
	#offspring_with_maternal_effects.append(pokemon)

# Get lists of individual trait values with just genetic and maternal effects

color_intensity_list_for_VA_and_ma = get_color_intensity_list(offspring_with_maternal_effects)
adult_weight_list_for_VA_and_ma = get_adult_weight_list(offspring_with_maternal_effects)
tail_flame_height_list_for_VA_and_ma = get_tail_flame_height_list(offspring_with_maternal_effects)
moves_known_list_for_VA_and_ma = get_moves_known_list(offspring_with_maternal_effects)

# Since 'moves known' has to round to a whole number, all its elements get converted to integers
moves_known_list_for_VA_and_ma = list(map(int, moves_known_list_for_VA_and_ma))


# Get averages that include genetic and maternal effects
avg_gen_and_ma_color_intensity = calculate_average_color_intensity(offspring_with_maternal_effects)
avg_gen_and_ma_adult_weight = calculate_average_adult_weight(offspring_with_maternal_effects)
avg_gen_and_ma_tail_flame_height = calculate_average_tail_flame_height(offspring_with_maternal_effects)
avg_gen_and_ma_moves_known = calculate_average_moves_known(offspring_with_maternal_effects)

avg_gen_and_ma_moves_known = int(avg_gen_and_ma_moves_known)






print("The average genetic color intensity is {0}.".format(str(avg_genetic_color_intensity)[:4]))
print("The average genetic+maternal color intensity is {0}.".format(str(avg_gen_and_ma_color_intensity)[:4]))
print("The additive genetic variance in color intensity is {0}.".format(str(color_intensity_VA)[:4]))
print("The minimum color intensity in this population is {0}.".format(str(min(color_intensity_list_for_VA))[:4]))
print("The maximum color intensity in this population is {0}.".format(str(max(color_intensity_list_for_VA))[:4]))
print("")

print("The average genetic adult weight is {0}.".format(str(avg_genetic_adult_weight)[:4]))
print("The average genetic+maternal adult weight is {0}.".format(str(avg_gen_and_ma_adult_weight)[:4]))
print("The additive genetic variance in adult weight is {0}".format(str(adult_weight_VA)[:4]))
print("The minimum adult weight in this population is {0}.".format(str(min(adult_weight_list_for_VA))[:4]))
print("The maximum adult weight in this population is {0}.".format(str(max(adult_weight_list_for_VA))[:4]))
print("")



print("The average genetic tail flame height is {0}.".format(str(avg_genetic_tail_flame_height)[:4]))
print("The average genetic+maternal tail flame height is {0}.".format(str(avg_gen_and_ma_tail_flame_height)[:4]))
print("The additive genetic variance in tail flame height is {0}".format(str(tail_flame_height_VA)[:4]))
print("The minimum tail-flame height in this population is {0}.".format(str(min(tail_flame_height_list_for_VA))[:4]))
print("The maximum tail-flame height in this population is {0}.".format(str(max(tail_flame_height_list_for_VA))[:4]))
print("")


print("The average genetic moves known is {0}.".format(str(avg_genetic_moves_known)[:4]))
print("The average genetic+maternal moves known is {0}.".format(str(avg_gen_and_ma_moves_known)[:4]))
print("The additive genetic variance in moves is {0}.".format(str(moves_known_VA)[:4]))
print("The minimum moves known in this population is {0}.".format(str(min(moves_known_list_for_VA))[:4]))
print("The maximum moves known in this population is {0}.".format(str(max(moves_known_list_for_VA))[:4]))
print("")


