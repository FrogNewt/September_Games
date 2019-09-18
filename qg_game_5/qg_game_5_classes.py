#!/usr/bin/env python3

import random


# A class to hold population-wide data (means, variances, etc)
class Population(object):
	def __init__(self):
		self.mean_genetic_trait_value = "undefined_mean_genetic_trait_value"
		self.additive_genetic_variance = "undefined_additive_genetic_variance"
		self.mean_phenotypic_trait_value = "undefined_mean_phenotypic_trait_value"
		self.phenotypic_variance = "undefined_phenotypic_variance"
		self.trait = "undefined_trait_(population)"
		self.species = "undefined_population_species"
		self.predator_type = "undefined_predator_type"
		self.predator_strength = "undefined_predator_strength"
		self.population_size = "undefined_population_size"
		self.heritability = "undefined heritability"
		self.viable = True

		self.mean_breeding_value_list = []

		self.BREEDERS_EQUATION_BEFORE = ""
		self.BREEDERS_EQUATION_AFTER = ""

		# Used to hold a single static predator that each organism will encounter
		self.predator = ""
		self.mean_phenotypic_trait_value_list = []
		self.additive_genetic_variance_list = []
		self.phenotypic_variance_list = []
		self.population_size_list = []
		self.predator_strength_list = []
		self.predator_list = []
		self.heritability_list = []
		self.selection_differential_list = []
		self.response_to_selection_list = []
		self.dead_this_gen_list = []

		self.parent_gen = []
		self.current_gen = []

		self.before_selection_population = []
		self.before_selection_trait_mean_list = []
		self.after_selection_population = []
		self.after_selection_trait_mean_list = []

# Defines all attributes of the Organism class (to be instantiated to produce each organism)
class Organism(object):
	def __init__(self):
		self.species = "undefined_species"
		self.trait = "undefined_trait"

		# The trait below combines genetic and maternal effects (no environmental); just for back-end use
		self.genetic_and_maternal_trait_value = "undefined genetic + maternal effects"

		# The trait below combines genetic and environmental effects (no maternal; just for back-end use)
		self.genetic_and_environmental_trait_value = "undefined genetic + environmental effects"
		self.breeding_value = "undefined_breeding_value"
		self.mendelian_sampling_deviation = ""
		self.sex = "undefined_sex"
		self.mate = "undefined_mate"
		self.dam = "undefined_dam"
		self.sire = "undefined sire"
		self.dead = False

		# This is a proportion; we multiply it by the breeding value to add or subtract
		# A certain proportion of the breeding value again as a maternal effect.
		# This is to be used to calculate this organism's OFFSPRING's phenotype, not its
		# own phenotype
		self.maternal_effect = random.uniform(-0.5, 0.5)
		self.environmental_effect = random.uniform(-0.5, 0.5)

		# This will be the organism's phenotype AFTER maternal and environmental effects
		self.phenotypic_trait_value = 0

# To be used only in generating the original ancestors; new trait values will come from pairing parents
class AncestorMom(Organism):
	def __init__(self):
		super().__init__()
		self.parenting_style = "Helicopter"