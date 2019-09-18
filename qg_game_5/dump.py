#!/usr/bin/env python3



		self.hist_list = None
		self.hist_wall_list = None


        # Sprites to be generated for use in the histogram
        self.hist_sprite_1 = None
        self.hist_sprite_2 = None
        self.hist_sprite_3 = None
        self.hist_sprite_4 = None
        self.hist_sprite_5 = None
        self.hist_sprite_6 = None
        self.hist_sprite_7 = None
        self.hist_sprite_8 = None
        self.hist_sprite_9 = None
        self.hist_sprite_10 = None


if self.level_complete == True:
            self.hist_list.draw()
            self.hist_wall_list.draw()
            #self.enemy_wall_list.draw()



        self.hist_list = arcade.SpriteList()
        self.hist_wall_list = arcade.SpriteList()





        # Groups the histogram sprites by default in a particular arrangement
        self.hist_sprite_1 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_1.center_y = 200
        self.hist_sprite_1.center_x = 150


        self.hist_sprite_2 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_2.center_y = 300
        self.hist_sprite_2.center_x = 150

        self.hist_sprite_3 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_4 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING)
        self.hist_sprite_5 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING)
        self.hist_sprite_6 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING)
        self.hist_sprite_7 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING)
        self.hist_sprite_8 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_HIGH_VAR)
        self.hist_sprite_9 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_HIGH_VAR)
        self.hist_sprite_10 = arcade.Sprite('images/player_1/clean_charizard.png', CHARACTER_SCALING_HIGH_VAR)

        self.hist_list.append(self.hist_sprite_1)
        self.hist_list.append(self.hist_sprite_2)
        self.hist_list.append(self.hist_sprite_3)
        self.hist_list.append(self.hist_sprite_4)
        self.hist_list.append(self.hist_sprite_5)
        self.hist_list.append(self.hist_sprite_6)
        self.hist_list.append(self.hist_sprite_7)
        self.hist_list.append(self.hist_sprite_8)
        self.hist_list.append(self.hist_sprite_9)
        self.hist_list.append(self.hist_sprite_10)

        # Makes every histogram sprite into a wall object that others must remain atop
        self.hist_wall_list.append(self.hist_sprite_1)
        self.hist_wall_list.append(self.hist_sprite_2)
        self.hist_wall_list.append(self.hist_sprite_3)
        self.hist_wall_list.append(self.hist_sprite_4)
        self.hist_wall_list.append(self.hist_sprite_5)
        self.hist_wall_list.append(self.hist_sprite_6)
        self.hist_wall_list.append(self.hist_sprite_7)
        self.hist_wall_list.append(self.hist_sprite_8)
        self.hist_wall_list.append(self.hist_sprite_9)
        self.hist_wall_list.append(self.hist_sprite_10)


self.wall_list.append(wall)
            self.hist_wall_list.append(wall)



        self.physics_engine_hist_1 = arcade.PhysicsEnginePlatformer(self.hist_sprite_1, self.hist_wall_list, GRAVITY)
        self.physics_engine_hist_2 = arcade.PhysicsEnginePlatformer(self.hist_sprite_2, self.hist_wall_list, GRAVITY)
        self.physics_engine_hist_3 = arcade.PhysicsEnginePlatformer(self.hist_sprite_3, self.hist_wall_list, GRAVITY)
        self.physics_engine_hist_4 = arcade.PhysicsEnginePlatformer(self.hist_sprite_4, self.hist_wall_list, GRAVITY)
        self.physics_engine_hist_5 = arcade.PhysicsEnginePlatformer(self.hist_sprite_5, self.hist_wall_list, GRAVITY)
        self.physics_engine_hist_6 = arcade.PhysicsEnginePlatformer(self.hist_sprite_6, self.hist_wall_list, GRAVITY)





        self.physics_engine_hist_1.update()
        self.physics_engine_hist_2.update()


        self.make_histogram()


            

        self.hist_list.draw()



