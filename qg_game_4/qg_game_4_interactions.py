#!/usr/bin/env python3

import random
import numpy





def encounter(org1, org2):
	if org1.species == org2.species:
		reproduce(org1, org2)

# Tries to have the 
def reproduce(male):
	pass

def meet_predator(organism, predator):
	if predator.attack > organism.defense:
		organism.dead = True