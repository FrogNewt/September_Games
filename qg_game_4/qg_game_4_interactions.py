#!/usr/bin/env python3

import random
import numpy






# Tries to have the 
def reproduce(org1, new_org_list, species_class):
	for i in range(int(org1.fecundity)):
		new_baby = species_class()
		new_org_list.append(new_baby)

def meet_predator(organism, predator):
	if predator.attack > organism.defense:
		organism.dead = True