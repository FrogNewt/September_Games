def breed(self):
		current_viewport = arcade.get_viewport()
		if self.current_music != self.love_music:
		    self.current_music = self.love_music
		    mixer.init()
		    mixer.music.load(self.love_music)
		    mixer.music.play()
		    mixer.music.fadeout(6000)
		    print("Should've played!")

		#self.honeymoon_ready = True
		self.set_breeding_coordinates(current_viewport)

		for i in range(len(self.histogram_list)):
		    g = i - 1

		    breeding_coordinates = self.breeding_coordinates

		    if self.histogram_list[g].mating_point == False:
		        # Establish semi-permanent mating coordinates for each organism
		        self.histogram_list[g].point = numpy.random.randint(0, len(breeding_coordinates))
		    
		    # Shorthand
		    point = self.histogram_list[g].point

		    print("This guy's point: ", point)
		    # Flip a switch so that all organisms don't continue to get new points
		    if breeding_coordinates[point] not in self.used_coords:
		        self.histogram_list[g].mating_point = True


		    # If you reach the coordinate, stop moving left and right
		    if self.histogram_list[g].center_x == breeding_coordinates[point][0]:
		        self.histogram_list[g].change_x = 0
		        self.histogram_list[g].paired_x = True

		    # If the coordinate is to your left, move left
		    elif self.histogram_list[g].center_x > (breeding_coordinates[point][0]):
		        self.histogram_list[g].change_x = -5

		    # If the coordinate is to your right, move right
		    elif self.histogram_list[g].center_x < (breeding_coordinates[point][0]):
		        self.histogram_list[g].change_x = 5

		    # If the coordinate is below you, move south
		    if self.histogram_list[g].center_y > (breeding_coordinates[point][1]):
		        self.histogram_list[g].change_y = -5

		    # If the coordinate is above you, move up
		    elif self.histogram_list[g].center_y < (breeding_coordinates[point][1]):
		        self.histogram_list[g].change_y = 5
		    else:
		    	# If you've reached the coordinate, stay there
		        self.histogram_list[g].change_y = 0
		        self.histogram_list[g].paired_y = True

		    

		    self.used_coords.append(breeding_coordinates[point])
		if not self.paired_count >= len(self.histogram_list):
		    self.paired_count = 0

		    for i in self.histogram_list:
		        if (i.paired_y and i.paired_x) == True:
		            self.paired_count += 1
		    print("Pre-honeymoon but really close!")

		if self.paired_count >= len(self.histogram_list):
		    print("At the honeymoon!")
		    self.honeymoon()