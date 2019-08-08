#!/usr/bin/env python3

import random

# Game 1: Designated to produce breeding values and use the breeder's equation to control what happens next.

# Defines the player class (a placeholder for various values to be used)
class Player(object):
	def __init__(self):
		self.mean = 0
		self.new_mean = 0
		self.desired_response = 0
		self.heritability = 0

# Creates an object of the class "Player"
player = Player()


print("A wild population of Charmanders appears!")
input("")
print("Oooo!  Look at their tail-flames!")


# Get the population mean for a given trait value (in this example, tail-flame height represents the trait)
while True:
	player.mean = input("What would you like the population mean for tail-flame height to be? (type a number!) \n")

	if not player.mean.isdigit():
		print("Ooops!  That's not a number!  Try again.")
	else:
		player.mean = int(player.mean)
		break

#input("So, we've got our mean tail-flame height ({0}), but what's the range like?")

print("Ok--the population mean for tail flames is {0}!".format(str(player.mean)))


while True:
	player.response = input("So, what do you WANT the tail-flames to be? (enter a number!)\n")

	if not player.response.isdigit():
		print("Ooops!  That's not a number!  Try again.")
	else:
		player.response = int(player.response)
		print("Ok, you want it to be {0}".format(player.response))
		break


player.heritability = random.random()


print(player.heritability)

print("Ok...a little quantitative genetic magic, and...")

def breeders_equation(mean, desired_response, heritability):
	player.new_mean = 6 + (desired_response + (heritability*mean)) / heritability
	print("Looks like the population mean required to produce a tail-flame of {0} is {1}!".format(player.desired_response, player.new_mean))
	return player.new_mean

breeders_equation(player.mean, player.desired_response, player.heritability)


# The breeder's equation is defined as:
# R (new breeding value, sometimes also written as delta "Z", the change in the trait value) = h^2 (the heritability of the trait) * S (the selection differential, or the difference between the new trait mean and the parent trait mean)
# In short: R = h^2(new - old)



