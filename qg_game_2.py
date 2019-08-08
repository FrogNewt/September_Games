#!/usr/bin/env python3

import random

# Game 2: Designed to determine the heritability of a trait!

class Player(object):
	def __init__(self):
		self.animal = ""
		self.animals = {
			"pigeon" : ["long", "centimeters"],
			"charmander" : ["tall","inches"],
			"blue whale" : ["long","meters"],
			}
		self.first_animal = 0
		self.second_animal = 0
		self.third_animal = 0
		self.fourth_animal = 0
		self.fifth_animal = 0
		self.sixth_animal = 0
		self.seventh_animal = 0
		self.eighth_animal = 0
		self.ninth_animal = 0
		self.tenth_animal = 0

player = Player()

total_phenotypic_variance = random.randint(1,1000)

total_genotypic_variance = random.randint(1,total_phenotypic_variance)


heritability = total_genotypic_variance / total_phenotypic_variance


print("The heritability of the trait is: " + str(heritability)[:4])






while True:
	print("What kind of animal do you want to look at?  You can choose from these: \n")

	for animal in player.animals.keys():
		print(animal.title())
	print("")

	player.animal = input("").lower()

	print("\n")

	if player.animal.lower() in player.animals.keys():
		print("Gotcha--we're working with {0}s!".format(player.animal))
		break
	else:
		print("Ooops--that one's not on the list!  Here are your choices:")



while True:
	print("Now, let's make some!")  
	player.first_animal = input("How {0} do you want your first {1} to be? (Give your answer in {2}!)".format(player.animals[player.animal][0],player.animal, player.animals[player.animal][1]))
	if player.first_animal.isdigit():
		print("Ok!  Your first {0} is {1} {2} {3}!".format(player.animal, player.first_animal, player.animals[player.animal][1], player.animals[player.animal][0]))
		break
	else:
		print("Whoops--enter a number!")


while True:
	player.second_animal = input("And the second? (Give your answer in {2}!)".format(player.animals[player.animal][0],player.animal, player.animals[player.animal][1]))
	if player.second_animal.isdigit():
		break
	else:
		print("Whoops--enter a number!")



