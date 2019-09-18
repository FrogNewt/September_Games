 if self.organism_low_var_sprite.deaths < 1:
                self.hist_list[0].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT].scale
                self.hist_list[0].center_x = low_var_base_x + 200
                self.hist_list[0].draw()
                self.hist_list[0].drawn = True
            
            # Draws the next 
            if self.organism_low_var_sprite.deaths < 3:
                if ((self.hist_time + 0.5) < current_time) and self.hist_list[1]:
                    self.hist_list[1].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT_SECOND_DEATH].scale
                    self.hist_list[1].center_x = low_var_base_x + 285
                    self.hist_list[1].draw()
            
            # Draws the next-from-leftmost tail (bottom) of the histogram only if it didn't die!
            if self.organism_low_var_sprite.deaths < 2:
                if ((self.hist_time + 1) < current_time) and self.hist_list[2]:
                    #self.hist_list[2].center_y = self.hist_floor + 50
                    self.hist_list[2].center_x = low_var_base_x + 285
                    self.hist_list[2].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT_FIRST_DEATH].scale
                    self.hist_list[2].draw()

            mean_base_x = low_var_base_x + 285

            if self.organism_mean_sprite.deaths < 4:
                if self.hist_time + 1.5 < current_time and self.hist_list[3]:
                    self.hist_list[3].center_y = self.hist_floor
                    self.hist_list[3].center_x = mean_base_x + 85
                    self.hist_list[3].draw()

            if self.organism_mean_sprite.deaths < 3:
                if self.hist_time + 2 < current_time and self.hist_list[4]:
                    self.hist_list[4].center_y = self.hist_floor + 50
                    self.hist_list[4].center_x = mean_base_x + 85
                    self.hist_list[4].draw()

            if self.organism_mean_sprite.deaths < 2:
                if self.hist_time + 2.5 < current_time and self.hist_list[5]:
                    self.hist_list[5].center_y = self.hist_floor + 100
                    self.hist_list[5].center_x = mean_base_x + 85
                    self.hist_list[5].draw()

            if self.organism_mean_sprite.deaths < 1:            
                if self.hist_time + 3 < current_time and self.hist_list[6]:
                    self.hist_list[6].center_y = self.hist_floor + 150
                    self.hist_list[6].center_x = mean_base_x + 85
                    self.hist_list[6].draw()

            high_var_base_x = mean_base_x + 170

            if self.organism_high_var_sprite.deaths < 3:
                if self.hist_time + 3.5 < current_time and self.hist_list[7]: 
                    self.hist_list[7].center_y = self.hist_floor + 5
                    self.hist_list[7].center_x = high_var_base_x
                    self.hist_list[7].scale = self.organism_high_var_sprite.textures[TEXTURE_LEFT_SECOND_DEATH].scale
                    self.hist_list[7].draw()

            if self.organism_high_var_sprite.deaths < 2:
                if self.hist_time + 4 < current_time and self.hist_list[8]:
                    self.hist_list[8].center_y = self.hist_floor + 70
                    self.hist_list[8].center_x = high_var_base_x
                    self.hist_list[8].scale = self.organism_high_var_sprite.textures[TEXTURE_LEFT_FIRST_DEATH].scale
                    self.hist_list[8].draw()

            if self.organism_high_var_sprite.deaths < 1:
                if ((self.hist_time + 4.5) < current_time) and self.hist_list[9]:
                    self.hist_list[9].center_y = self.hist_floor + 15
                    self.hist_list[9].center_x = high_var_base_x + 100
                    self.hist_list[9].draw()








    def give_hist_coordinates(self, current_viewport):
        low_var_base_x = current_viewport[0] + 200

        self.hist_sprite_1.center_y = self.hist_floor - 5
        self.hist_sprite_1.center_x = low_var_base_x

        self.hist_sprite_2.center_y = self.hist_floor - 5
        self.hist_sprite_2.center_x = self.hist_sprite_1.center_x + 85

        self.hist_sprite_3.center_y = self.hist_sprite_2.center_y + 50
        self.hist_sprite_3.center_x = self.hist_sprite_2.center_x

        self.hist_sprite_4.center_y = self.hist_floor
        self.hist_sprite_4.center_x = self.hist_sprite_3.center_x + 85

        self.hist_sprite_5.center_y = self.hist_sprite_4.center_y + 60
        self.hist_sprite_5.center_x = self.hist_sprite_4.center_x

        self.hist_sprite_6.center_y = self.hist_sprite_5.center_y + 60
        self.hist_sprite_6.center_x = self.hist_sprite_5.center_x

        self.hist_sprite_7.center_y = self.hist_sprite_6.center_y + 60
        self.hist_sprite_7.center_x = self.hist_sprite_6.center_x

        self.hist_sprite_8.center_y = self.hist_floor + 5
        self.hist_sprite_8.center_x = self.hist_sprite_7.center_x + 85

        self.hist_sprite_9.center_y = self.hist_sprite_8.center_y + 70
        self.hist_sprite_9.center_x = self.hist_sprite_8.center_x

        self.hist_sprite_10.center_y = self.hist_floor + 5
        self.hist_sprite_10.center_x = self.hist_sprite_9.center_x + 85





self.breeding_coordinates = [
                # First pair
                
                # Left
                [50, 100],
                #Right
                [100, 100],

                # Second pair

                # Left
                [150, 200],
                #Right
                [200, 200],

                # Third pair

                # Left
                [250, 250],
                #Right
                [200, 250],

                # Fourth pair

                # Left
                [260, 300],
                #Right
                [310, 300],

                # Fifth pair

                # Left
                [270, 100],
                #Right
                [320, 100]

        ]