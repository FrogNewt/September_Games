#!/usr/bin/env python3

# Game 1: Designated to produce breeding values and use the breeder's equation to control what happens next.

print("A wild population of Charmanders appears!")
input("")
print("Oooo!  Look at their tail-flames!")


# Get the population mean for a given trait value (in this example, tail-flame height represents the trait)
while True:
	mean = input("What would you like the population mean for tail-flame height to be? (type a number!) \n")

	if not mean.isdigit():
		print("Ooops!  That's not a number!  Try again.")
	else:
		mean = int(mean)
		break

print("Ok--the population mean for tail flames is {0}!".format(str(mean)))

# The breeder's equation is defined as:
# R (new breeding value, sometimes also written as delta "Z", the change in the trait value) = h^2 (the heritability of the trait) * S (the selection differential, or the difference between the new trait mean and the existing trait mean)
# In short: R = h^2(S)