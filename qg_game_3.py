#!/usr/bin/env python3


# Imports the "random" module which allows for random number generation
import random

# Game 3: Designed to test an organism's fitness (environment-by-environment)

# Defines basic stats for all pokemon populations (defaults, to be adjusted on a population-by-population basis)
class Pokemon(object):
	def __init__(self):
		self.name = "Undefined Pokemon Population"
		self.HP = 1
		self.attack = 1
		self.defense = 1
		self.fecundity = 1
		self.size = 1
		self.development_time = 1
		self.longevity = 1
		self.strong_against = "Strong against nothing"
		self.weak_against = "Weak against nothing"
		self.temperature_preferred = "No preferred temperature"
		self.population_size = 1

# Sets stats for Bulbasaur
class Bulbasaur(Pokemon):
	def __init__(self):
		super().__init__()
		self.name = "Bulbasaur"
		self.HP = random.randint(10, 20)
		self.attack = random.randint(5,25)
		self.defense = random.randint(0,5)
		self.population_size = 50
		self.weak_against = "fire"

# Sets stats for Charmander
class Charmander(Pokemon):
	def __init__(self):
		super().__init__()
		self.name = "Charmander"
		self.HP = random.randint(10, 20)
		self.attack = random.randint(5,50)
		self.defense = random.randint(0,5)
		self.population_size = 25
		self.weak_against = "water"

# Sets stats for Squirtles
class Squirtle(Pokemon):
	def __init__(self):
		super().__init__()
		self.name = "Squirtle"
		self.HP = random.randint(10, 100)
		self.attack = random.randint(5,10)
		self.defense = random.randint(10,30)
		self.fecundity = random.randint(0,5)
		self.longevity = 30
		self.population_size = 20
		self.weak_against = "plants"

class MewTwo(Pokemon):
	def __init__(self):
		super().__init__()
		self.name = "MewTwo"
		self.HP = random.randint(10, 20)
		self.attack = random.randint(5,100)
		self.fecundity = random.randint(0,5)
		self.longevity = 10
		self.defense = random.randint(0,5)


input("Congratulations!  You're being awarded your first Pokemon!\n")
input("...hey, wait a minute--it looks like Professor Oak has decided to give you an entire POPULATION of them!\n")
input("HOLY.\n")
input("COW.\n")
input("He says it's your job to select the population with the highest fitness!\n")
input("Well, we'd better have a look at them!  Here are the populations you can choose from!\n")

bulbasaur = Bulbasaur()
charmander = Charmander()
squirtle = Squirtle()
mewtwo = MewTwo()


species_available = [bulbasaur, charmander, squirtle, mewtwo]


for pokemon in species_available:
	for stat in pokemon.__dict__.keys():
		print(stat.title() + " (on average):", pokemon.__dict__[stat])
	print("\n")
