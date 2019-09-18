#!/usr/bin/env python3

# Thanks to the arcade tutorial on platformer games for providing a basis for this version!
# Thanks also to the users of stack exchange for constructively answering *so* many questions
# about gaming and offering up snippets of useful code!

# NOTE: use arcade.get_viewport() to get the current viewport dimensions (left, right, bottom, top)

# NOTE: arcade.schedule(function, interval) calls a function every certain number of seconds
# Don't forget on_mouse_press and on_mouse_motion functions!
"""
Platformer Game
"""
import arcade
#import qg_game_5
import numpy
#import qg_game_5
import time
from threading import Timer
from pygame import mixer

import sim_for_game as sim
#import character_selection as cs


pop = sim.starter_list
pop_keeper = sim.pop_holder

starting_mean = pop_keeper.mean_phenotypic_trait_value_list[0]


bulbasaur_scaling = 0.1
charmander_scaling = 0.07
squirtle_scaling = 0.25

# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Jake's Platformer"

# Set default textures
TEXTURE_RIGHT = 1
TEXTURE_LEFT = 0
#TEXTURE_MATED = 2

TEXTURE_LEFT_FIRST_DEATH = 2
TEXTURE_RIGHT_FIRST_DEATH = 3
#TEXTURE_MATED_FIRST_DEATH = 5

TEXTURE_LEFT_SECOND_DEATH = 4
TEXTURE_RIGHT_SECOND_DEATH = 5
#TEXTURE_MATED_SECOND_DEATH = 8

# Constants used to scale our sprites from their original size
DEMO_SCALING = 0.5
CLOUD_SCALING = 0.05
MOUNTAIN_SCALING = 1
BOUNDARY_TREE_SCALING = 0.40

STATIC_CHARACTER_SCALING = 0.1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
ENEMY_SCALING = 0.1

# Set the speed at which the character increments
ORGANISM_MEAN_MOVEMENT_SPEED = 5
ORGANISM_LOW_VAR_MOVEMENT_SPEED = 5
ORGANISM_HIGH_VAR_MOVEMENT_SPEED = 5
ENEMY_MOVEMENT_SPEED = 1

# Note: Changing the gravity not only affects the speed at which your character is pulled back to Earth but also the distance upward it can travel
# Note: If you lower the gravity enough, you can "jump" in mid-air (i.e. fly) if your character has enough jump strength
GRAVITY = 1.0
HIST_GRAVITY = 0.1
ORGANISM_MEAN_JUMP_SPEED = 10
ORGANISM_LOW_VAR_JUMP_SPEED = 6
ORGANISM_HIGH_VAR_JUMP_SPEED = 16


# How many pixels to keep as a minimum margin between the character
# and the edge of the screen
LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH*(6/8)
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH*(6/8)
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 350



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of all sprites--every sprite should have a list, and that listed should probably be based on what the sprite can/can't do
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.darwin_list = None
        self.mate_list = None
        self.enemy_list = None
        self.starters_list = None

        self.CHARACTER_SCALING = 0.02 * starting_mean
        self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING * 0.5
        self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING * 1.5

        # A list to hold all histogram characters
        self.hist_list = None
        self.hist_wall_list = None
        self.sound_opener = None

        self.zelda = None
        self.media_player = mixer.init()
        self.intro_music = 'sounds/fairy_fountain_intro.wav'
        self.game_music = 'sounds/Night_Riding.wav'
        self.current_music = mixer.music.load(self.intro_music)

        

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

        # Here's a separate variable that holds the player sprite
        self.organism_mean_sprite = None
        self.organism_low_var_sprite = None
        self.organism_high_var_sprite = None
        self.enemy = None
        self.darwin_sprite = None

        self.pop_0_alive = True
        self.pop_1_alive = True
        self.pop_2_alive = True
        self.pop_3_alive = True
        self.pop_4_alive = True
        self.pop_5_alive = True
        self.pop_6_alive = True
        self.pop_7_alive = True
        self.pop_8_alive = True
        self.pop_9_alive = True
        self.loss_list = []

        self.current_state = "OPENING"

        self.starter_organism_dict = {
        "bulbasaur" : "images/bulbasaur_left.png",
            "charmander" : "images/charmander_left.png",
            "squirtle" : "images/squirtle_left.png"
        
        }
        self.starter_organism = "images/player_1/clean_charizard.png"


        # Attributes used to keep track of which organism is being followed on the screen
        self.focus_counter = 0
        self.focal_organism = ""
        self.focal_organism_list = []

        # Switches to be flipped in case all of the upper, middle, or bottom sprites are killed.
        self.top_dead = False
        self.mean_dead = False
        self.bottom_dead = False

        self.level = 1

        # Keeps track of how many times the upper, lower, and mean avatars have died
        # (Max 3 for top and bottom and max 4 for mean)
        self.top_deaths = 0
        self.mean_deaths = 0
        self.bottom_deaths = 0

        # Sets the background screen fade
        self.fade_stage_1 = False
        self.fade_stage_2 = False
        self.fade_stage_3 = False
        self.fade_stage_4 = False
        self.fade_stage_5 = False
        self.fade_stage_6 = False
        self.fade_stage_7 = False
        self.fade_stage_8 = False
        self.fade_stage_9 = False
        self.fade_stage_10 = False
        self.fade_stage_11 = False
        self.quick_sunset = False
        
        # Sets the default values of these colors to be changed
        self.fade_blue = 238
        self.fade_green = 149
        self.fade_red = 100

        # Sets up a floor for the histogram characters
        self.hist_floor = ""

        # Checks to see if the level is complete
        self.level_complete = False

        self.go_to_next_level = False

        # Switches on while histogram is being generated
        self.making_histogram = False
        
        # If this is true, begin the debriefing process
        self.debriefing = False

        # Switches extinction on and ends the game
        self.extinction = False

        # Holds the current time
        self.start_time = ""

        # Runs a timer for the histogram process
        self.hist_time = ""

        # Toggles the breeding event on/off
        self.ready_to_breed = False

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Where is the right edge of the map (or any edge, as you like)?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.victory_theme = arcade.load_sound("sounds/victory_theme.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")

         # Sets the background color--there are lots of options available through the arcade site
        arcade.set_background_color((230, 143, 255))

    def setup(self, level=1, CHARACTER_SCALING = starting_mean):
        """ Set up the game here. Call this function to restart the game. """
        
             

        self.CHARACTER_SCALING = 0.02 * CHARACTER_SCALING
        self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING * 0.5
        self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING * 1.5

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Groups the histogram sprites by default in a particular arrangement
        self.hist_list = arcade.SpriteList()
        self.hist_wall_list = arcade.SpriteList()

        # Designate the "floor" for the histogram characters
        self.hist_floor = 70

        # Histogram character 1
        self.hist_sprite_1 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_1.center_y = self.hist_floor - 5
        self.hist_sprite_1.center_x = 800

        # Histogram character 2
        self.hist_sprite_2 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_2.center_y = self.hist_floor - 5
        self.hist_sprite_2.center_x = self.hist_sprite_1.center_x + 85

        # Histogram character 3
        self.hist_sprite_3 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_3.center_y = self.hist_sprite_2.center_y + 50
        self.hist_sprite_3.center_x = self.hist_sprite_2.center_x

        # Histogram character 4
        self.hist_sprite_4 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING)
        self.hist_sprite_4.center_y = self.hist_floor
        self.hist_sprite_4.center_x = self.hist_sprite_3.center_x + 85

        # Histogram character 5
        self.hist_sprite_5 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING)
        self.hist_sprite_5.center_y = self.hist_sprite_4.center_y + 60
        self.hist_sprite_5.center_x = self.hist_sprite_4.center_x

        # Histogram character 6
        self.hist_sprite_6 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING)
        self.hist_sprite_6.center_y = self.hist_sprite_5.center_y + 60
        self.hist_sprite_6.center_x = self.hist_sprite_5.center_x

        # Histogram character 7
        self.hist_sprite_7 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING)
        self.hist_sprite_7.center_y = self.hist_sprite_6.center_y + 60
        self.hist_sprite_7.center_x = self.hist_sprite_6.center_x

        # Histogram character 8
        self.hist_sprite_8 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_HIGH_VAR)
        self.hist_sprite_8.center_y = self.hist_floor + 5
        self.hist_sprite_8.center_x = self.hist_sprite_7.center_x + 85

        # Histogram character 9
        self.hist_sprite_9 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_HIGH_VAR)
        self.hist_sprite_9.center_y = self.hist_sprite_8.center_y + 70
        self.hist_sprite_9.center_x = self.hist_sprite_8.center_x

        # Histogram character 10
        self.hist_sprite_10 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_HIGH_VAR)
        self.hist_sprite_10.center_y = self.hist_floor + 5
        self.hist_sprite_10.center_x = self.hist_sprite_9.center_x + 85

        # Add histogram sprites to a list so that their gravity et al can be manipulated
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


        for i in range(10):
            self.hist_list[i-1].drawn = False

        # Make every histogram sprite into a "wall" object so that they can stand on one another
        #self.hist_wall_list.append(self.hist_sprite_1)
        #self.hist_wall_list.append(self.hist_sprite_2)

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.mate_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.darwin_list = arcade.SpriteList()
        self.focal_organism_list = []
        
        self.enemy_physics_engine_list = []



        # Set up the player, specifically placing it at these coordinates (to begin the game)
        self.organism_mean_sprite = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING)
        self.organism_low_var_sprite = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_LOW_VAR)
        self.organism_high_var_sprite = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_HIGH_VAR)
        

        self.focal_organism_list.append(self.organism_mean_sprite)
        self.focal_organism_list.append(self.organism_low_var_sprite)
        self.focal_organism_list.append(self.organism_high_var_sprite)

        self.focal_organism = self.focal_organism_list[self.focus_counter]

        # Sets up textures for right and left facing sprites that can be modified
        # For mean organism
        self.organism_mean_sprite.current_right = TEXTURE_RIGHT
        self.organism_mean_sprite.current_left = TEXTURE_LEFT

        # For top organism
        self.organism_high_var_sprite.current_right = TEXTURE_RIGHT
        self.organism_high_var_sprite.current_left = TEXTURE_LEFT

        # For bottom organism
        self.organism_low_var_sprite.current_right = TEXTURE_RIGHT
        self.organism_low_var_sprite.current_left = TEXTURE_LEFT

        # Starts the invincibility clock for each organism
        self.organism_low_var_sprite.invincibility_timer = 0
        self.organism_mean_sprite.invincibility_timer = 0
        self.organism_high_var_sprite.invincibility_timer = 0

        self.organism_low_var_sprite.invincible = False
        self.organism_mean_sprite.invincible = False
        self.organism_high_var_sprite.invincible = False


        self.organism_mean_sprite.center_x = 64
        self.organism_mean_sprite.center_y = 220
        self.organism_mean_sprite.textures = []
        self.organism_mean_sprite.alpha = 255
        self.organism_mean_sprite.deaths = 0

        self.organism_low_var_sprite.center_x = 64
        self.organism_low_var_sprite.center_y = 220
        self.organism_low_var_sprite.textures = []
        self.organism_low_var_sprite.alpha = 50
        self.organism_low_var_sprite.deaths = 0

        self.organism_high_var_sprite.center_x = 64
        self.organism_high_var_sprite.center_y = 220
        self.organism_high_var_sprite.textures = []
        self.organism_high_var_sprite.alpha = 50
        self.organism_high_var_sprite.deaths = 0

        self.player_list.append(self.organism_mean_sprite)
        self.player_list.append(self.organism_low_var_sprite)
        self.player_list.append(self.organism_high_var_sprite)


        



        ### ADJUSTS CHARACTER ###
        # Load a left-facing texture and a right facing texture.
        # The 'mirrored' argument will mirror whichever image we load.

        # Mean organism
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        
        self.organism_mean_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)

        # First Death
        texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", mirrored=True, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        # Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)

        # Second Death
        texture = arcade.load_texture("images/player_1/clean_charizard_ice.png", scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        texture = arcade.load_texture("images/player_1/clean_charizard_ice.png", mirrored=True, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)


        # Textures for the smallest variant of the organism
        # No deaths
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_LOW_VAR)
        #self.organism_low_var_sprite.textures.append(texture)
        

        # First death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        #self.organism_low_var_sprite.textures.append(texture)

        # Second death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        #self.organism_low_var_sprite.textures.append(texture)


        # Textures for the largest variant of the organism
        # No deaths
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_HIGH_VAR)
        #self.organism_high_var_sprite.textures.append(texture)

        # First death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        #self.organism_high_var_sprite.textures.append(texture)

        # Second death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture("images/player_1/clean_charizard_purple.png", scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
        #self.organism_high_var_sprite.textures.append(texture)

        # By default, face right.
        self.organism_mean_sprite.set_texture(TEXTURE_RIGHT)
        self.organism_low_var_sprite.set_texture(TEXTURE_RIGHT)
        self.organism_high_var_sprite.set_texture(TEXTURE_RIGHT)

        self.organism_high_var_sprite.pop_position = 10

       
        # Creates the ground
        for x in range(-500, 10000, 64):
            wall = arcade.Sprite("images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 10
            self.wall_list.append(wall)
            self.hist_wall_list.append(wall)
            self.enemy_wall_list.append(wall)

        tree = arcade.Sprite("images/tiles/boundary_tree.png", BOUNDARY_TREE_SCALING)
        tree.center_x = -350
        tree.center_y = 265
        self.wall_list.append(tree)
        

        

        # Set up the predator
        self.enemy = arcade.Sprite("images/red_gyarados_right.png", ENEMY_SCALING)
        self.enemy.center_x = -150
        self.enemy.center_y = 90
        arcade.schedule(self.make_enemy, 5)
        
        self.enemy_list.append(self.enemy)

        # Set up Darwin (end of level)
        self.darwin_sprite = arcade.Sprite("images/darwin.png")

        # Darwin Textures
        self.darwin_sprite.textures = []
        texture = arcade.load_texture("images/darwin.png", scale = 1)
        self.darwin_sprite.textures.append(texture)
        texture = arcade.load_texture("images/darwin.png", mirrored = True, scale = 1)
        self.darwin_sprite.textures.append(texture)
        self.darwin_sprite.set_texture(1)

        self.darwin_sprite.center_x = 1200
        self.darwin_sprite.center_y = 64

        self.darwin_list.append(self.darwin_sprite)

        level_y_boundary = self.organism_high_var_sprite.textures[0].height * self.organism_high_var_sprite.textures[TEXTURE_RIGHT].scale
        print("Min Boundary for y on boxes: ", level_y_boundary)
        level_y_boundary = level_y_boundary + self.hist_floor

        print("Texture height: ", self.organism_high_var_sprite.textures[0].height)
        print("Scaling for texture: ", self.organism_high_var_sprite.textures[TEXTURE_RIGHT].scale)

        print("Scaling height: ", self.organism_high_var_sprite.textures[0].height * self.organism_high_var_sprite.textures[TEXTURE_RIGHT].scale)
        # Put some crates on the ground
        # This shows using a coorinate list ot place sprites
        coordinate_range_min = [200, self.hist_floor+40]
        coordinate_range_max = [1000, self.hist_floor + 50]

        for coordinate in range(10):
            # Add a crate on the ground
            x_coordinate = numpy.random.randint(coordinate_range_min[0], coordinate_range_max[0]) 
            y_coordinate = numpy.random.randint(coordinate_range_min[1], coordinate_range_max[1])


            wall = arcade.Sprite("images/rock.png", TILE_SCALING)
            wall.position = [x_coordinate, y_coordinate]
            self.wall_list.append(wall)
            self.enemy_wall_list.append(wall)
            

         # Create the ground
        # This creates a loop to place multiple sprites horizontally (maybe they make up the floor?)
        for x in range(-500, 10000, 64):
            wall = arcade.Sprite("images/tiles/cloud.png", CLOUD_SCALING)
            wall.center_x = x
            wall.center_y = 510
            self.wall_list.append(wall)
            self.hist_wall_list.append(wall)
            self.enemy_wall_list.append(wall)

        mountain = arcade.Sprite("images/mountain.png", MOUNTAIN_SCALING)
        mountain.center_x = numpy.random.randint(200, 500)
        mountain.center_y = numpy.random.randint(150, 300)
        self.wall_list.append(mountain)
        self.enemy_wall_list.append(mountain)

        stander = arcade.Sprite("images/player_1/clean_charizard_ice.png", STATIC_CHARACTER_SCALING)
        stander.position = [55, 105]
        self.mate_list.append(stander)




        # Create the 'physics engine' 
        ### NOTE: CHANGE THIS TO PhysicsEngineSimple FOR GRAVITY-LESS PLAYERS ###
        self.physics_engine_mean = arcade.PhysicsEnginePlatformer(self.organism_mean_sprite, self.wall_list, GRAVITY)
        self.physics_engine_low_var = arcade.PhysicsEnginePlatformer(self.organism_low_var_sprite, self.wall_list, GRAVITY)
        self.physics_engine_high_var = arcade.PhysicsEnginePlatformer(self.organism_high_var_sprite, self.wall_list, GRAVITY)

        self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy, self.enemy_wall_list, GRAVITY)
        self.enemy_physics_engine_list.append(self.physics_engine_enemy)
        self.physics_engine_darwin = arcade.PhysicsEnginePlatformer(self.darwin_sprite, self.wall_list, GRAVITY)

        #self.physics_engine_hist_1 = arcade.PhysicsEnginePlatformer(self.hist_list[0], self.hist_wall_list, 0)
 

        # Histogram physics
        #self.physics_engine_hist_1 = arcade.PhysicsEnginePlatformer(self.hist_sprite_1, self.hist_list, HIST_GRAVITY)
        #self.physics_engine_hist_2 = arcade.PhysicsEnginePlatformer(self.hist_sprite_2, self.hist_list, HIST_GRAVITY)
        

        # Checks the status of all player sprites
        self.all_player_sprites = self.organism_mean_sprite and self.organism_low_var_sprite and self.organism_high_var_sprite

        # Checks on any player sprite
        self.any_player_sprite = self.organism_mean_sprite or self.organism_low_var_sprite or self.organism_high_var_sprite
        #self.physics_engine = arcade.PhysicsEnginePlatformer(self.organism_low_var_sprite, self.wall_list, GRAVITY)
        #self.physics_engine = arcade.PhysicsEnginePlatformer(self.organism_high_var_sprite, self.wall_list, GRAVITY)

    def make_enemy(self, interval):
            enemy = arcade.Sprite("images/red_gyarados_right.png", ENEMY_SCALING)
            enemy.center_x = -150
            enemy.center_y = 90
            physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy, self.enemy_wall_list, GRAVITY)
            self.enemy_physics_engine_list.append(physics_engine_enemy)
            self.enemy_list.append(enemy)
        

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        if self.current_state == "OPENING":
            self.draw_opening_screen()
            self.current_state = "OPENING RUNNING"
        
        if self.current_state == "OPENING" or "OPENING RUNNING":
            starting_viewport = self.get_viewport()
            output = "Evolution"
            arcade.draw_text(output, starting_viewport[0]+250, starting_viewport[2]+250, arcade.color.WHITE, 54)

        if self.current_state == "CHARACTER SELECTION":
            arcade.start_render()
            self.draw_selection_text()
            self.draw_characters()
            

        if self.current_state == "GAME":
            self.draw_game()
            

    def draw_opening_screen(self):
        
        mixer.music.play()

        
        
        
        

        arcade.set_background_color((0,0,0))

        #riding_night_sound.pause()



    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == "OPENING RUNNING":
            self.current_state = "CHARACTER SELECTION"
            mixer.music.fadeout(3000)
            print("Post-music")

        if self.current_state == "CHARACTER SELECTION":
            
            select = arcade.load_sound("sounds/select.wav")
            
            if button == arcade.MOUSE_BUTTON_LEFT:
                #for i in self.starters_list:
                #    print("A POKEMON: ", i)

                bulbasaur_check = self.starters_list[0].collides_with_point((x, y))
                charmander_check = self.starters_list[1].collides_with_point((x, y))
                squirtle_check = self.starters_list[2].collides_with_point((x, y))


            i = 0

            if bulbasaur_check == True:
                self.starter_organism = self.starter_organism_dict["bulbasaur"]
                arcade.play_sound(select)
                print("Bulbasaur!")
                i += 1
            elif charmander_check == True:
                self.starter_organism = self.starter_organism_dict["charmander"]
                arcade.play_sound(select)
                print("Charmander!")
                i += 1
            elif squirtle_check == True:
                self.starter_organism = self.starter_organism_dict["squirtle"]
                arcade.play_sound(select)
                print("Squirtle!")
                i += 1

            if i > 0:
                self.current_state = "GAME"
                self.setup()
                

    def draw_game(self):
        # NOTE: THIS IS WORKING TO PRODUCE EXTINCTION IN THE MIDDLE OF THE SCREEN!

        arcade.start_render()
        if self.current_music != self.game_music:
            self.current_music = self.game_music
            mixer.music.load(self.game_music)
            mixer.music.play()
            arcade.set_background_color((230, 143, 255))



        
        # Code to draw the screen goes here
        
        #Draw our sprites
        self.wall_list.draw()
        #self.coin_list.draw()
        self.player_list.draw()

        #self.mate_list.draw()
        self.enemy_list.draw()
        self.darwin_list.draw()

        if self.level_complete:
            self.make_histogram()

        if self.extinction:
            extinction_text = f"EXTINCTION!"
            arcade.draw_text(extinction_text, 100 + self.view_left, 300 + self.view_bottom, 
                         arcade.csscolor.WHITE, 60)

        if self.making_histogram == True:
            

            if not self.hist_time:
                self.hist_time = time.time()
            
            current_time = time.time()

            current_viewport = arcade.get_viewport()

            leftovers_text = f"WHO'S LEFT: "
            arcade.draw_text(leftovers_text, current_viewport[0] + 250, current_viewport[2] + 400, 
                         arcade.csscolor.WHITE, 40)

            low_var_base_x = current_viewport[0]
            
            # Draws the leftmost tail of the histogram only if none of the tiny guys died!
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
                    self.hist_list[2].center_y = self.hist_list[1].center_y + 50
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
                    self.hist_list[8].center_y = self.hist_list[7].center_y + 65
                    self.hist_list[8].center_x = high_var_base_x
                    self.hist_list[8].scale = self.organism_high_var_sprite.textures[TEXTURE_LEFT_FIRST_DEATH].scale
                    self.hist_list[8].draw()

            if self.organism_high_var_sprite.deaths < 1:
                if ((self.hist_time + 4.5) < current_time) and self.hist_list[9]:
                    self.hist_list[9].center_y = self.hist_floor + 15
                    self.hist_list[9].center_x = high_var_base_x + 100
                    self.hist_list[9].draw()

            self.ready_to_breed = True
            self.calculate_losses()
            #print(self.loss_list)
            self.making_histogram = False
            
            if self.level_complete and self.go_to_next_level:
                self.start_new_level(self.level)
                #self.level_complete = False
            


        



    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        breeding_coordinates = []
        current_viewport = arcade.get_viewport()

        #### NOT YET ABLE TO GET EVERYONE FLYING OFF AND BREEDING ####

        if key == arcade.key.ENTER:
            if self.ready_to_breed == True:
                current_viewport = arcade.get_viewport()
                breeding_coordinates = [
                [80, 100],
                [100, 100]
                ]
                #self.hist_list[0].change_x = 15
                #self.hist_list[0].change_y = 10
        if self.level_complete:
            if key == arcade.key.ENTER:
                self.go_to_next_level = True


        if (self.level_complete == False) and (self.extinction == False):
            if key == arcade.key.UP or key == arcade.key.W:
                ### UNCOMMENT LINES BELOW FOR JUMPING ABILITY/SOUND IN SIDE-TO-SIDE PLATFORMER ###
                #if self.physics_engine.can_jump():
                #self.organism_mean_sprite.change_y = ORGANISM_MEAN_JUMP_SPEED

                if self.physics_engine_mean.can_jump():
                    self.organism_mean_sprite.change_y = ORGANISM_MEAN_JUMP_SPEED
                
                if self.physics_engine_low_var.can_jump():
                    self.organism_low_var_sprite.change_y = ORGANISM_LOW_VAR_JUMP_SPEED
                
                if self.physics_engine_high_var.can_jump():
                    self.organism_high_var_sprite.change_y = ORGANISM_HIGH_VAR_JUMP_SPEED

                #arcade.play_sound(self.jump_sound)
            if key == arcade.key.DOWN or key == arcade.key.S:
                self.organism_mean_sprite.change_y = -ORGANISM_MEAN_MOVEMENT_SPEED
                self.organism_low_var_sprite.change_y = -ORGANISM_LOW_VAR_MOVEMENT_SPEED
                self.organism_high_var_sprite.change_y = -ORGANISM_HIGH_VAR_MOVEMENT_SPEED

            if key == arcade.key.LEFT or key == arcade.key.A:
                self.organism_mean_sprite.set_texture(self.organism_mean_sprite.current_left)
                self.organism_mean_sprite.change_x = -ORGANISM_MEAN_MOVEMENT_SPEED
                self.organism_low_var_sprite.set_texture(self.organism_low_var_sprite.current_left)
                self.organism_low_var_sprite.change_x = -ORGANISM_LOW_VAR_MOVEMENT_SPEED
                self.organism_high_var_sprite.set_texture(self.organism_high_var_sprite.current_left)
                self.organism_high_var_sprite.change_x = -ORGANISM_HIGH_VAR_MOVEMENT_SPEED

            
            if key == arcade.key.RIGHT or key == arcade.key.D:
                self.organism_mean_sprite.set_texture(self.organism_mean_sprite.current_right)
                self.organism_mean_sprite.change_x = ORGANISM_MEAN_MOVEMENT_SPEED
                self.organism_low_var_sprite.set_texture(self.organism_low_var_sprite.current_right)
                self.organism_low_var_sprite.change_x = ORGANISM_LOW_VAR_MOVEMENT_SPEED
                self.organism_high_var_sprite.set_texture(self.organism_high_var_sprite.current_right)
                self.organism_high_var_sprite.change_x = ORGANISM_HIGH_VAR_MOVEMENT_SPEED

                #self.enemy.change_x = ENEMY_MOVEMENT_SPEED
                #self.enemy.change_y = self.enemy.center_y - self.focal_organism.center_y

                self.start_time = int(time.time())


            if key:
                for enemy in self.enemy_list:
                    enemy.change_x = ENEMY_MOVEMENT_SPEED
                    enemy.change_y = self.focal_organism.change_y
                    
                    if (enemy.center_x < current_viewport[0]) or (enemy.center_x > (current_viewport[0] + current_viewport[1])) or (enemy.center_y < current_viewport[2]) or (enemy.center_y > (current_viewport[2] + current_viewport[3])):
                        enemy.remove_from_sprite_lists()

            """if key == arcade.key.TAB:
                if self.focus_counter < len(self.focal_organism_list)-1:
                    self.focus_counter += 1
                elif self.focus_counter == len(self.focal_organism_list)-1:
                    self.focus_counter = 0
                if (self.organism_low_var_sprite.deaths == 3) or (self.organism_mean_sprite.deaths == 4) or (self.organism_high_var_sprite.deaths == 3):
                    self.focus_counter = 0
                    self.bottom_dead = False
                    self.top_dead = False
                    self.mean_dead = False
                if len(self.player_list) == 0:
                    print("YOU'VE DIED!")
                self.focal_organism = self.player_list[self.focus_counter]"""

            #if self.focal_organism not in self.player_list:
                #self.focal_organism = self.focal_organism_list[0]
            # When Tab is pressed
            
            
            if key == arcade.key.KEY_1:
                if self.organism_low_var_sprite in self.player_list:
                    self.focal_organism = self.organism_low_var_sprite
                    print("Key noted!")
            if key == arcade.key.KEY_2:
                if self.organism_mean_sprite in self.player_list:
                    self.focal_organism = self.organism_mean_sprite
            if key == arcade.key.KEY_3:
                if self.organism_high_var_sprite in self.player_list:
                    self.focal_organism = self.organism_high_var_sprite





  

                # Increment the focus counter on to the next organism variant
                
                



             
            #### NEED TO MODIFY FOR HISTOGRAM SECTION TO WORK PROPERLY ####
            #if self.level_complete == True:
            #    if key == arcade.key.RIGHT:
            #        center = self.organism_mean_sprite.center_x
            #        self.organism_low_var_sprite.change_x = center - 1
            #        self.organism_high_var_sprite.change_x = center + 1


            
        



    def on_key_release(self, key, modifiers):
        """ Called whenever a key is pressed. """
        ### NOTE: IF YOU ELIMINATE THIS METHOD, YOU'LL HAVE CHARACTERS THAT KEEP MOVING IN ONE DIRECTION INDEFINITELY, ALA GRADIUS ###

        
        ### IF YOU WANT CHARACTERS TO MOVE FREELY (i.e. without gravity) UNCOMMENT W AND S ###
        if key == arcade.key.UP or key == arcade.key.W:
            self.organism_mean_sprite.change_y = 0
            self.organism_low_var_sprite.change_y = 0
            self.organism_high_var_sprite.change_y = 0

        if key == arcade.key.DOWN or key == arcade.key.S:
            self.organism_mean_sprite.change_y = 0
            self.organism_low_var_sprite.change_y = 0
            self.organism_high_var_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.organism_mean_sprite.change_x = 0
            self.organism_low_var_sprite.change_x = 0
            self.organism_high_var_sprite.change_x = 0
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.organism_mean_sprite.change_x = 0
            self.organism_low_var_sprite.change_x = 0
            self.organism_high_var_sprite.change_x = 0



    def update(self, delta_time):
        """ Movement and game logic """
        if self.ready_to_breed == True:
            self.breed()

        if len(self.player_list) == 0 and (self.making_histogram == False) and (self.level_complete == False):
            self.go_extinct()

        if self.level_complete==True:
            self.end_level()

        if self.current_state == "GAME":

            self.physics_engine_mean.can_jump()
            self.physics_engine_low_var.can_jump()
            self.physics_engine_high_var.can_jump()
            self.physics_engine_mean.increment_jump_counter()

            # Call update on all sprites (The sprites don't do much in this example, though.)
            self.physics_engine_mean.update()
            self.physics_engine_low_var.update()
            self.physics_engine_high_var.update()
            for physics_engine in self.enemy_physics_engine_list:
                physics_engine.update()
            self.physics_engine_darwin.update()

            self.enemy_list.update()

            self.hist_list.update()

            #self.physics_engine_hist_1.update()

            # Update histogram
            #self.physics_engine_hist_1.update()
            #self.physics_engine_hist_2.update()
            
            






            if self.level_complete:
                self.quick_sunset = True
                # Note: the increment value here is meaningless because quick sunset takes over
                self.sunset(self.start_time)


            # Accelerated sunset when the level is ending

            elif self.start_time and (self.level_complete == False) and (self.debriefing == False):
                
                self.sunset(self.start_time, 2)

            # In order to prevent constant calling of the method on update, adjust this attribute
            

            # Check for collision with Darwin (end level)
            darwin_hit_list = arcade.check_for_collision_with_list(self.organism_mean_sprite, self.darwin_list)
            darwin_hit_list2 = arcade.check_for_collision_with_list(self.organism_low_var_sprite, self.darwin_list)
            darwin_hit_list3 = arcade.check_for_collision_with_list(self.organism_high_var_sprite, self.darwin_list)

            # Creates a master list so that all characters can be checked at once
            master_darwin_list = [
            darwin_hit_list,
            darwin_hit_list2,
            darwin_hit_list3
            ]


            # When they reach Darwin
            for darwin_hit_list in master_darwin_list:

                for darwin in darwin_hit_list:
                    self.level_complete = True
                    darwin.remove_from_sprite_lists()
                    self.player_list = arcade.SpriteList()

                
                for player in darwin_hit_list:
                    #player.remove_from_sprite_lists()
                    if (self.level_complete == False) and (self.debriefing == False):
                        self.level_complete = True
                        arcade.play_sound(self.collect_coin_sound)
                        print("LEVEL OVER!")
                        


            # See if we hit any coins
            coin_hit_list = arcade.check_for_collision_with_list(self.organism_mean_sprite, self.coin_list)
            coin_hit_list2 = arcade.check_for_collision_with_list(self.organism_low_var_sprite, self.coin_list)
            coin_hit_list3 = arcade.check_for_collision_with_list(self.organism_high_var_sprite, self.coin_list)


            # Check to see if we've come into contact with any mates
            mate_hit_list = arcade.check_for_collision_with_list(self.organism_mean_sprite, self.mate_list)
            mate_hit_list2 = arcade.check_for_collision_with_list(self.organism_low_var_sprite, self.mate_list)
            mate_hit_list3 = arcade.check_for_collision_with_list(self.organism_high_var_sprite, self.mate_list)

            # Creates a master list so that all characters can be checked at once
            master_coin_list = [
            coin_hit_list,
            coin_hit_list2,
            coin_hit_list3
            ]

            # Creates a master list so that all characters can be checked at once
            master_mate_list = [
            mate_hit_list,
            mate_hit_list2,
            mate_hit_list3
            ]

            player_master_hit_hist = []
            for enemy in self.enemy_list:
                player_hit_list = arcade.check_for_collision_with_list(enemy, self.player_list)
                player_master_hit_hist.append(player_hit_list)
            #player_hit_list = arcade.check_for_collision_with_list(self.enemy, self.player_list)

            for player_hit_list in player_master_hit_hist:
                for player in player_hit_list:
                    self.check_invincibility(player)
                    if player.invincible == False:
                        if player == self.organism_low_var_sprite:
                            #self.self.CHARACTER_SCALING_LOW_VAR = self.self.CHARACTER_SCALING_LOW_VAR * 1.2
                            if self.organism_low_var_sprite.deaths < 3:
                                self.organism_low_var_sprite.deaths += 1
                                self.die_and_reincarnate(player)
                            self.bottom_dead = True
                            
                            if self.organism_low_var_sprite.deaths == 3:
                                player.remove_from_sprite_lists()

                            print("HUMPTY!")
                        elif player == self.organism_high_var_sprite:
                            #self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING_HIGH_VAR * 0.8
                            if self.organism_high_var_sprite.deaths < 3:
                                self.organism_high_var_sprite.deaths += 1
                                
                                self.die_and_reincarnate(player)

                            self.top_dead = True
                            if self.organism_high_var_sprite.deaths == 3:
                                player.remove_from_sprite_lists()
                        elif player == self.organism_mean_sprite:
                            if self.organism_mean_sprite.deaths < 4:
                                
                                self.organism_mean_sprite.deaths += 1
                                self.die_and_reincarnate(player)
                            self.mean_dead = True
                            if self.organism_mean_sprite.deaths == 4:
                                player.remove_from_sprite_lists()
                        
                        arcade.play_sound(self.collect_coin_sound)

    ####### NEED TO FIX BUG WHERE WHEN YOU DIED WHILE PLAYING THE LARGEST VAR YOU CAN'T TAB INTO OTHERS #####




            # --- Manage Scrolling ---
     
            # Only change the viewport if the level is yet unbeaten!
            if self.level_complete == False:


                # Track if we need to change the viewport
                changed = False

                ### NOTE: ALL OF THIS IS CURRENTLY WORKING CORRECTLY, BUT SOMETHING'S WRONG WITH WINDOW SIZING; FIX THIS TO MAKE SCROLLING WORK PROPERLY ###
                # Solved the above by inreasing the right viewport margin (in "constants" section above initializer)

                # Scroll left
                left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
                if self.focal_organism.left < left_boundary:
                    self.view_left -= left_boundary - self.focal_organism.left
                    changed = True

                # Scroll right
                right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
                if (self.focal_organism.right) > right_boundary:
                    self.view_left += self.focal_organism.right - right_boundary
                    changed = True

                # Scroll up
                top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
                if self.focal_organism.top > top_boundary:
                    self.view_bottom += self.focal_organism.top - top_boundary
                    changed = True

                # Scroll down
                bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
                if self.focal_organism.bottom < bottom_boundary:
                    self.view_bottom -= bottom_boundary - self.focal_organism.bottom
                    changed = True

                if changed:
                    # Only scroll to integers--otherwise we end up with pixels
                    # that don't line up on the screen
                    self.view_bottom = int(self.view_bottom)
                    self.view_left = int(self.view_left)

                    # Do the sscrolling
                    arcade.set_viewport(self.view_left,
                                        SCREEN_WIDTH + self.view_left,
                                        self.view_bottom,
                                        SCREEN_HEIGHT + self.view_bottom)



#### CURRENT ISSUE WITH SUNSET: IT UPDATES SO OFTEN THAT IT'S DIFFICULT TO FIND A WAY TO MAKE PYTHON
#### STOP UPDATING THE SUNSET.  TRY SETTING UP PARAMETERS SO THAT A CASCADE OF SWITCHES TURN ON/OFF
#### THE NEXT SUNSET STEP; MAYBE FADE_STAGE_X = TRUE WOULD DO THE TRICK?


    def check_invincibility(self, organism):
        current_time = time.time()
        

        if organism.invincibility_timer + 3 < current_time:
            organism.invincible = False
            
            organism.invincibility_timer = 0

    def invincible(self, organism):
        if organism.invincibility_timer == 0:
            organism.invincibility_timer = time.time()
            organism.invincible = True



    def die_and_reincarnate(self, organism):
        self.invincible(organism)
        if organism.deaths == 1:
            organism.current_left = TEXTURE_LEFT_FIRST_DEATH
            organism.current_right = TEXTURE_RIGHT_FIRST_DEATH
        elif organism.deaths == 2:
            organism.current_left = TEXTURE_LEFT_SECOND_DEATH
            organism.current_right = TEXTURE_RIGHT_SECOND_DEATH

        

    
    def sunset(self, start_sunset_time, increment = 3):
        # Sets up a super-fast sunset for the transition into the evaluation phase
        
        if self.quick_sunset == True:
            arcade.set_background_color((230, 143, 255))
            arcade.set_background_color((250, 243, 225))
            arcade.set_background_color((25, 25, 112))

        #if self.fade_stage_1 == False:
         #   print("###### NOTHING OCCURRED #######")
        current_time =int(time.time())
        #print(self.start_time, current_time)
        if self.quick_sunset == False:
            if (current_time > (start_sunset_time + increment*10)) and (self.fade_stage_11 == False):
                

                self.fade_stage_11 = True
                arcade.set_background_color((self.fade_red-20, self.fade_green, self.fade_blue))
                print("####### FADE 11 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)

            elif (current_time > (start_sunset_time + increment*9)) and (self.fade_stage_10 == False):
                self.fade_green -= 10

                self.fade_stage_10 = True
                arcade.set_background_color((self.fade_red, self.fade_green, self.fade_blue))
                print("####### FADE 10 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)

            elif (current_time > (start_sunset_time + increment*8)) and (self.fade_stage_9 == False):
                self.fade_green -= 10
                self.fade_red += 10
                self.fade_blue -= 100
                self.fade_stage_9 = True
                arcade.set_background_color((self.fade_red, self.fade_green, self.fade_blue))
                print("####### FADE 9 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)


            elif (current_time > (start_sunset_time + increment*7)) and (self.fade_stage_8 == False):
                self.fade_green -= 10
                self.fade_red += 10
                self.fade_stage_8 = True
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 8 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)
        
            elif (current_time > (start_sunset_time + increment*6)) and (self.fade_stage_7 == False):
                self.fade_green -= 10
                self.fade_stage_7 = True
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 7 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)
            
            elif (current_time > (start_sunset_time + increment*5)) and (self.fade_stage_6 == False):
                self.fade_green -= 10
                self.fade_stage_6 = True
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 6 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)
            
            elif (current_time > (start_sunset_time + increment*4)) and (self.fade_stage_5 == False):
                self.fade_green -= 10
                self.fade_stage_5 = True
     
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 5 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)
            
            elif (current_time > (start_sunset_time + increment*3)) and (self.fade_stage_4 == False):
                self.fade_green -= 10
                self.fade_stage_4 = True
     
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 4 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)

            elif (current_time > (start_sunset_time + increment*2)) and (self.fade_stage_3 == False):
                self.fade_green -= 10
                self.fade_red -= 10
                self.fade_stage_3 = True
     
                arcade.set_background_color((self.fade_red, self.fade_green, 238))
                print("####### FADE 3 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)

            elif (current_time > (start_sunset_time + increment)) and (self.fade_stage_2 == False):
                self.fade_green -= 10
                self.fade_red -= 10
                self.fade_stage_2 = True

                arcade.set_background_color((250, 243, 225))
                print("####### FADE 2 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)

            elif (current_time > start_sunset_time) and (self.fade_stage_1 == False):
                self.fade_green -= 10
                self.fade_red -= 10
                self.fade_stage_1 = True
            


                print("####### FADE 1 #########")
                print("Fade green:", self.fade_green)
                print("Fade red: ", self.fade_red)
                arcade.set_background_color((230, 143, 255))
            
        
    def renew_textures(self):
        self.player_list[0].textures[0] = arcade.load_texture(self.starter_organism, self.CHARACTER_SCALING)
        print("FROM RENEW", self.starter_organism)


    def draw_selection_text(self):
        new_viewport = self.get_viewport()
        output = "CHOOSE YOUR CHARACTER"
        arcade.draw_text(output, new_viewport[0]+50, new_viewport[2]+350, arcade.color.WHITE, 40)

    def draw_characters(self):
        current_viewport = self.get_viewport()

        bulbasaur = arcade.Sprite("images/bulbasaur_left.png", bulbasaur_scaling)
        charmander = arcade.Sprite("images/charmander_left.png", charmander_scaling)
        squirtle = arcade.Sprite("images/squirtle_left.png", squirtle_scaling)

        self.starters_list = arcade.SpriteList()
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
        #   starters_list[i].center_x = current_viewport[0] + (i)*50
        #   starters_list[i].center_y = current_viewport[2] + 250

        self.starters_list.draw()
        
        
            
    def end_level(self):
        self.level_complete = True
        #self.focal_organism = ""
        #print("Running sunset!")
        #for enemy in self.enemy_list:
        #    enemy.remove_from_sprite_lists()
        #for player in self.player_list:
        #    player.remove_from_sprite_lists()
        #for player in self.focal_organism_list:
        #    player.remove_from_sprite_lists()


        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.focal_organism_list = arcade.SpriteList()
        
        # Wait until the sunset has completed to switch "level complete" back off
        if self.fade_stage_11 == True:
            pass
            #self.level_complete = False
        
        self.view_left = -100

        for player in self.player_list:
            player.alpha = 0

        


        #self.player_list = arcade.SpriteList()

    def go_extinct(self):
        print("Extinct!")
        self.extinction = True

    def make_histogram(self):
        self.making_histogram = True
        #self.hist_sprite_1.change_y = 5
        

    # Works!
    def enter_debriefing(self):
        print("DEBRIEFING!")


#### PRODUCE NEXT GENERATION ####



    def start_new_level(self, level):

        # Resets this for the next go-around
        self.go_to_next_level = False

        # Reset the timer for the histogram
        self.hist_time = ""

        print(pop_keeper.mean_phenotypic_trait_value_list)
        self.level += 1

        sim.select_via_player(pop_keeper.current_gen, self.loss_list, pop_keeper)
        print(self.loss_list)
        sim.funcs.reproduce(pop_keeper, sim.classes.Organism)
        sim.funcs.evaluate_population(pop_keeper.current_gen, pop_keeper, sim.starter_species, sim.starter_trait)

        new_mean = pop_keeper.mean_phenotypic_trait_value_list[self.level-1]
        print("NEW MEAN: ", new_mean)
        self.CHARACTER_SCALING = new_mean
        self.setup(level, self.CHARACTER_SCALING)

        #### DEMO FOR NEW TEXTURES USING MULTIPLE CHARACTERS ####
        



        self.level_complete = False

        # Reset deaths
        self.organism_mean_sprite.deaths = 0
        self.organism_low_var_sprite.deaths = 0
        self.organism_high_var_sprite.deaths = 0

        self.top_dead = False
        self.bottom_dead = False
        self.mean_dead = False

        self.fade_stage_1 = False
        self.fade_stage_2 = False
        self.fade_stage_3 = False
        self.fade_stage_4 = False
        self.fade_stage_5 = False
        self.fade_stage_6 = False
        self.fade_stage_7 = False
        self.fade_stage_8 = False
        self.fade_stage_9 = False
        self.fade_stage_10 = False
        self.fade_stage_11 = False
        self.quick_sunset = False
        

    def breed(self):
        current_viewport = arcade.get_viewport()
        breeding_coordinates = [
                [80, 100],
                [100, 100]
        ]
        #self.hist_list[0].change_x = self.hist_list[0].center_x + current_viewport[0]
        #self.hist_list[0].change_y = self.hist_list[0].center_y + current_viewport[1]




        
        #thread = threading.Thread(target=self.change_background())
        #thread.daemon = True
        #thread.start()
        
    def calculate_losses(self):
        self.loss_list = [
        self.pop_0_alive,
        self.pop_1_alive,
        self.pop_2_alive,
        self.pop_3_alive,
        self.pop_4_alive,
        self.pop_5_alive,
        self.pop_6_alive,
        self.pop_7_alive,
        self.pop_8_alive,
        self.pop_9_alive,
        ]

        if self.organism_low_var_sprite.deaths >= 1:
            self.loss_list[0] = False
        if self.organism_low_var_sprite.deaths >= 2:
            self.loss_list[1] = False
        if self.organism_low_var_sprite.deaths >= 3:
            self.loss_list[2] = False
        
        if self.organism_mean_sprite.deaths >= 1:
            self.loss_list[3] = False
        if self.organism_mean_sprite.deaths >= 2:
            self.loss_list[4] = False
        if self.organism_mean_sprite.deaths >= 3:
            self.loss_list[5] = False
        if self.organism_mean_sprite.deaths >= 4:
            self.loss_list[6] = False

        if self.organism_high_var_sprite.deaths >= 1:
            self.loss_list[7] = False
        if self.organism_high_var_sprite.deaths >= 2:
            self.loss_list[8] = False
        if self.organism_high_var_sprite.deaths >= 3:
            self.loss_list[9] = False



        



def main():
    """ Main method """
    window = MyGame()
    print("initialized!")
    window.setup(window.level)
    print("Just ran setup!")
    arcade.run()



if __name__ == "__main__":
    main()
