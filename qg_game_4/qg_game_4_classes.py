#!/usr/bin/env python3

import random
import numpy




### CLASSES ###

class popHolder(object):
	def __init__(self):
		pass

class Environment(object):
	env_names = [
		"desert",
		"forest",
		"prairie",
		"wetland",
		"mountains"
		]

	def __init__(self, name = "default environment", defense_impact = 0, fecundity_impact = 0, adult_weight_impact = 1, color_intensity_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1, description = "default description"):
		self.name = name
		self.adult_weight_impact = adult_weight_impact
		self.adult_weight_impact_range = [-1,1]

		self.color_intensity_impact = color_intensity_impact
		self.color_intensity_impact_range = [-1,1]

		self.tail_flame_height_impact = tail_flame_height_impact
		self.tail_flame_height_impact_range = [-1,1]

		self.moves_known_impact = moves_known_impact
		self.moves_known_impact_range = [-1,1]

		self.fecundity_impact = fecundity_impact
		self.fecundity_impact_range = [-1,1]

		self.defense_impact = defense_impact
		self.defense_impact_range = [-1,1]

		self.predator_attack_impact = 0
		self.predator_attack_impact_range = [-1,1]

		self.description = description

		



# Creates a Charizard object--mothers and offspring both begin as an instance of this class, but mothers will adopt a second class
class Charizard(object):
	def __init__(self, name = "default", defense = 1, fecundity = 5, color_intensity = 5, adult_weight = 10, tail_flame_height = 30, moves_known = 4):
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

		# Tells us how capable the charizard is of defending itself or escaping from danger
		self.defense = defense
		self.defense_range = [1,10]

		# Tells us who this charizard's mother is
		self.mom_identity = ""

		# Tells us the environment that this charizard was born in (for determining the effects of environment on your birthplace)
		self.env_born = ""

		# Describes the environment in which this Charizard was raised
		self.raised_environment = ""

		# Describes the charizard's reproductive potential--how many offspring will it produce?
		self.fecundity = fecundity
		self.fecundity_range = [1,5]

		# Determines whether or not this Charizard is a mom--note: all "moms" will be reassigned to "Momizard" class
		self.is_mom = False

		# Keeps track of which Charizard is which numerically (simpler than names for use in organizing them later)
		self.index = ""

		# Gives the species (for later incarnations of the game when other organisms may be available)
		self.species = "Charizard"
		
		# Changes to "True" when the charizard has been eaten by a predator--should add it to a list of the dead from that generation
		self.dead = False

		# Gives the charizard's sex--"0" is female, "1" is male
		self.sex = 0

		self.continuous_traits = [
		"color_intensity",
		"adult_weight",
		"tail_flame_height",
		"moves_known",
		"fecundity",
		"defense"
		]


class Momizard(Charizard):
	def __init__(self, offspring = "default offspring", defense_impact = 0, fecundity_impact = 0, name = "default name", adult_weight_impact = 1, color_intensity_impact = 1, tail_flame_height_impact = 1, moves_known_impact = 1):
		super().__init__()
		self.name = name

		# The environment in which this mother gave birth--all her offspring will share this environment
		self.env = ""

		# Note: You can use the "range"s below to change the proportion of the effect mom has (e.g. an effect of -0.5 would cut the existing trait value in half)
		self.adult_weight_impact = adult_weight_impact
		self.adult_weight_impact_range = [-1,1]
		
		self.color_intensity_impact = color_intensity_impact
		self.color_intensity_impact_range = [-0.2,0.2]
		
		self.tail_flame_height_impact = tail_flame_height_impact
		self.tail_flame_height_impact_range = [-1,1]
		
		self.moves_known_impact = moves_known_impact
		self.moves_known_impact_range = [-1,1]

		self.fecundity_impact = fecundity_impact
		self.fecundity_impact_range = [-1,1]

		self.defense_impact = defense_impact
		self.defense_impact_range = [-1,1]

		self.index = "has a 'mom' index"
		self.traits_of_impact = [
		"weight_impact",
		"adult_weight_impact",
		"tail_flame_height_impact",
		"moves_known_impact",
		"fecundity_impact",
		"defense_impact"
		]


class Predator(object):
	def __init__(self, attack = 2):
		self.attack_range = [1,10]
		self.attack = random.uniform(self.attack_range[0], self.attack_range[1])
		self.species = "predator"


### END CLASSES ###
