#!/usr/bin/env python3

import random
import numpy



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


# Different environment names
env_names = [
"desert",
"forest",
"prairie",
"wetland",
"mountains"
]


# Creates a list that includes genetic and maternal effects
offspring_with_maternal_effects = []

offspring_with_maternal_and_env_effects = []


def reset_lists(*each_list):
	each_list = []






### END IMPORTANT LISTS ###

 