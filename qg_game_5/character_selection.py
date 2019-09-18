#!/usr/bin/env python3

bulbasaur_scaling = 0.1
charmander_scaling = 0.07
squirtle_scaling = 0.25


def draw_selection_text(self, module):
	new_viewport = self.get_viewport()
	output = "CHOOSE YOUR CHARACTER"
	module.draw_text(output, new_viewport[0]+50, new_viewport[2]+350, module.color.WHITE, 40)

def draw_characters(self, module):
	current_viewport = self.get_viewport()

	bulbasaur = module.Sprite("images/bulbasaur_left.png", bulbasaur_scaling)
	charmander = module.Sprite("images/charmander_left.png", charmander_scaling)
	squirtle = module.Sprite("images/squirtle_left.png", squirtle_scaling)

	self.starters_list = module.SpriteList()
	self.starters_list.append(bulbasaur)
	self.starters_list.append(charmander)
	self.starters_list.append(squirtle)

	
	bulbasaur.center_x = current_viewport[0] + 120
	bulbasaur.center_y = current_viewport[2] + 200

	charmander.center_x = current_viewport[0] + 370
	charmander.center_y = current_viewport[2] + 200

	squirtle.center_x = current_viewport[0] + 620
	squirtle.center_y = current_viewport[2] + 200

	#for i in range(len(starters_list)):
	#	starters_list[i].center_x = current_viewport[0] + (i)*50
	#	starters_list[i].center_y = current_viewport[2] + 250

	self.starters_list.draw()