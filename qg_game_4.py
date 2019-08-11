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
 


### CLASSES ###

class Environment(object):
	def __init__(self, name = "default environment", weight_impact = 1, color_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1):
		self.name = name
		self.weight_impact = weight_impact
		self.color_impact = color_impact
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
	def __init__(self, offspring = "default offspring", name = "default name", weight_impact = 1, color_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1):
		super().__init__()
		self.name = name
		self.weight_impact = weight_impact
		self.color_impact = color_impact
		self.tail_flame_height_impact = tail_flame_height_impact
		self.moves_known_impact = moves_known_impact
		self.index = "has a 'mom' index"


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
		pokemon = Momizard()




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

	# Checks to see who the moms and offspring are and assigns them to their respective lists
	if pokemon.is_mom:
		moms.append(pokemon)
	else:
		offspring.append(pokemon)

	# Assigns an index based on whether or not the pokemon is a mother
	if not pokemon.is_mom:
		pokemon.index = i
	elif pokemon.is_mom:
		pokemon.mom_index = i
	
	# Increments forward
	i += 1





for baby in offspring:
	baby.mom_identity = random.randint(0, len(moms)-1)
	baby.mom_identity = moms[baby.mom_identity].name
	print("{0}'s mom is {1}!".format(pokemon.name, pokemon.mom_identity))





# Prints pokemon's stats--mostly for debugging right now.
for pokemon in pop_list:
	print("Name: " + pokemon.name.title())
	for trait in pokemon.__dict__:
		if "range" not in trait and (trait in pokemon.continuous_traits):
			if isinstance(pokemon.__dict__[trait], float):
				print(trait.title() + ":", str(pokemon.__dict__[trait])[:4])
			#elif str(trait) == "is_mom":
			#	pass
			else:	
				print(trait.title() + ":", str(pokemon.__dict__[trait]).title())
	print("")





print("There are " + str(len(moms)) + " mothers and " + str(len(offspring)) + " offspring!")
print("")

color_intensity_list = get_color_intensity_list(offspring)
adult_weight_list = get_adult_weight_list(offspring)
tail_flame_height_list = get_tail_flame_height_list(offspring)


moves_known_list = get_moves_known_list(offspring)

# Since 'moves known' has to round to a whole number, all its elements get converted to integers
moves_known_list = list(map(int, moves_known_list))

# Calculates the average values for traits among offspring
avg_color_intensity = calculate_average_color_intensity(offspring)
avg_adult_weight = calculate_average_adult_weight(offspring)
avg_tail_flame_height = calculate_average_tail_flame_height(offspring)
avg_moves_known = calculate_average_moves_known(offspring)

# Calculates the variances with respect to a given trait within a population of offspring
color_intensity_var = numpy.var(color_intensity_list)
adult_weight_var = numpy.var(adult_weight_list)
tail_flame_height_var = numpy.var(tail_flame_height_list)
moves_known_var = numpy.var(moves_known_list)





print("The average color intensity is {0}.".format(str(avg_color_intensity)[:4]))
print("The variance in color intensity is {0}.".format(str(color_intensity_var)[:4]))
print("The minimum color intensity in this population is {0}.".format(str(min(color_intensity_list))[:4]))
print("The maximum color intensity in this population is {0}.".format(str(max(color_intensity_list))[:4]))
print("")

print("The average adult weight is {0}.".format(str(avg_adult_weight)[:4]))
print("The variance in adult weight is {0}".format(str(adult_weight_var)[:4]))
print("The minimum adult weight in this population is {0}.".format(str(min(adult_weight_list))[:4]))
print("The maximum adult weight in this population is {0}.".format(str(max(adult_weight_list))[:4]))
print("")



print("The average tail flame height is {0}.".format(str(avg_tail_flame_height)[:4]))
print("The variance in tail flame height is {0}".format(str(tail_flame_height_var)[:4]))
print("The minimum tail-flame height in this population is {0}.".format(str(min(tail_flame_height_list))[:4]))
print("The maximum tail-flame height in this population is {0}.".format(str(max(tail_flame_height_list))[:4]))
print("")


print("The average moves known is {0}.".format(str(avg_moves_known)[:4]))
print("The variance in moves is {0}.".format(str(moves_known_var)[:4]))
print("The minimum moves known in this population is {0}.".format(str(min(moves_known_list))[:4]))
print("The maximum moves known in this population is {0}.".format(str(max(moves_known_list))[:4]))
print("")


templist = []

print("Moms:")
[templist.append(baby.mom_identity.title()) for baby in offspring]

print(set(templist))


print("")
print("Offspring:")
[print(baby.name.title()) for baby in offspring]



