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
import arcade.text as text
import sim_for_game as sim
#import character_selection as cs


pop = sim.starter_list
pop_keeper = sim.pop_holder

starting_mean = pop_keeper.mean_phenotypic_trait_value_list[0]


bulbasaur_scaling = 0.01
charmander_scaling = 0.01
squirtle_scaling = 0.02

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
MOUNTAIN_SCALING = 0.5
BOUNDARY_TREE_SCALING = 0.40

STATIC_CHARACTER_SCALING = 0.1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
ENEMY_SCALING = 0.1

# Set the speed at which the character increments
ORGANISM_MEAN_MOVEMENT_SPEED = 20
ORGANISM_LOW_VAR_MOVEMENT_SPEED = 20
ORGANISM_HIGH_VAR_MOVEMENT_SPEED = 20
ENEMY_MOVEMENT_SPEED = 1

# Note: Changing the gravity not only affects the speed at which your character is pulled back to Earth but also the distance upward it can travel
# Note: If you lower the gravity enough, you can "jump" in mid-air (i.e. fly) if your character has enough jump strength
GRAVITY = 1.0
HIST_GRAVITY = 0.1
ORGANISM_MEAN_JUMP_SPEED = 10
ORGANISM_LOW_VAR_JUMP_SPEED = 6
ORGANISM_HIGH_VAR_JUMP_SPEED = 20


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
        self.pre_intro_textures = []
        self.pre_intro_1 = ""
        self.pre_intro_2 = ""
        self.pre_intro_3 = ""
        self.pre_intro_1_started = False
        self.pre_intro_2_started = False
        self.pre_intro_3_started = False
        
        self.CHARACTER_SCALING = 0.2 * starting_mean
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
        self.love_music = 'sounds/love.wav'
        self.current_music = mixer.music.load(self.intro_music)

        
        self.intro_pokemon = None
        self.intro_venusaur = None
        self.intro_charizard = None
        self.intro_gyarados = None


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

        self.jake = None

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

        self.current_state = "PREOPENING"

        self.species_selected = False

        self.starter_organism_dict = {
        "bulbasaur" : "images/bulbasaur_left.png",
            "charmander" : "images/charmander_left.png",
            "squirtle" : "images/squirtle_left.png"
        
        }
        self.starter_organism = "images/player_1/clean_charizard.png"
        self.starter_string = ""


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

        # Switches the histogram to "fade-in" mode
        self.hist_fading_in = False
        
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
        

        self.jake = arcade.Sprite("images/jakepresents.png", scale=0.5)
        self.jake.fading_in = True
        self.jake.faded = False
        self.jake.fade_count = 0

        self.jake.textures = []
        texture = arcade.load_texture("images/warlak3.png", scale=0.5)
        self.jake.textures.append(texture)

        self.warlak = arcade.Sprite("images/warlak1.png", scale=0.05)
        self.warlak_pre = False
        self.warlak.fading_in = True
        self.warlak.faded = False

        self.qg_pokemon = arcade.Sprite("images/qg_pokemon.png", scale = 0.5)
        

        self.pre_2_ready = False

        self.start_game = False

        self.horse_bet_on = ""


        self.intro_pokemon = []
        self.intro_gyarados = arcade.Sprite("images/intro_pokemon/gyarados_left.png", scale = 0.4)
        self.intro_charizard = arcade.Sprite("images/intro_pokemon/clean_charizard.png", scale = 0.4)
        self.intro_venusaur = arcade.Sprite("images/intro_pokemon/venusaur.png", scale = 0.25)

        self.intro_pokemon.append(self.intro_venusaur)
        self.intro_pokemon.append(self.intro_charizard)
        self.intro_pokemon.append(self.intro_gyarados)

        for i in self.intro_pokemon:
            i.fading_in = True
            i.fading_out = False
        

        self.jaketexture = arcade.load_texture("images/jakepresents.png")
             
        self.var = pop_keeper.additive_genetic_variance_list[self.level-1]
        print("First variance:", self.var)
        self.std_dev = numpy.sqrt(self.var)
        # Set the mean organism scale based on the starter choice
        
        

        self.update_scaling(self.starter_string)

        


        self.pokemon_medley = "sounds/pokemon_medley.wav"

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
        self.hist_sprite_1.center_x = 100

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

        self.selection_calculated = False


        self.heart_list = arcade.SpriteList()
        self.honeymoon_ready = False

        self.prof_oak = arcade.Sprite("images/prof_oak.png", 1)
        self.prof_oak_dialogue = False
        self.prof_oak_key_pressed_1 = False
        self.prof_oak_key_pressed_2 = False

        # First set of dialogue images
        self.oak1_m1_of_9 = arcade.Sprite("images/oak1/oak1-1.png")
        self.oak1_m2_of_9 = arcade.Sprite("images/oak1/oak1-2.png")
        self.oak1_m3_of_9 = arcade.Sprite("images/oak1/oak1-3.png")
        self.darwin1_m4_of_9 = arcade.Sprite("images/oak1/oak1-4.png")
        self.darwin1_m5_of_9 = arcade.Sprite("images/oak1/oak1-5.png")
        self.oak1_m6_of_9 = arcade.Sprite("images/oak1/oak1-6.png")
        self.darwin1_m7_of_9 = arcade.Sprite("images/oak1/oak1-7(revised).png")
        self.darwin1_m8_of_9 = arcade.Sprite("images/oak1/oak1-8.png")
        self.oak1_m9_of_9 = arcade.Sprite("images/oak1/oak1-9.png")

        self.oak1_list = []

        self.oak1_list.append(self.oak1_m1_of_9)
        self.oak1_list.append(self.oak1_m2_of_9)
        self.oak1_list.append(self.oak1_m3_of_9)
        self.oak1_list.append(self.darwin1_m4_of_9)
        self.oak1_list.append(self.darwin1_m5_of_9)
        self.oak1_list.append(self.oak1_m6_of_9)
        self.oak1_list.append(self.darwin1_m7_of_9)
        self.oak1_list.append(self.darwin1_m8_of_9)
        self.oak1_list.append(self.oak1_m9_of_9)

        # Second set of dialogue images
        self.oak2_m1_of_5 = arcade.Sprite("images/oak2/oak2-1.png")
        self.darwin2_m2_of_5 = arcade.Sprite("images/oak2/oak2-2.png")
        self.oak2_m3_of_5 = arcade.Sprite("images/oak2/oak2-3.png")
        self.oak2_m4_of_5 = arcade.Sprite("images/oak2/oak2-4.png")
        self.oak2_m5charmander_of_5 = arcade.Sprite("images/oak2/oak2-5(charmander).png")
        self.oak2_m5squirtle_of_5 = arcade.Sprite("images/oak2/oak2-5(squirtle).png")
        self.oak2_m5bulbasaur_of_5 = arcade.Sprite("images/oak2/oak2-5(bulbasaur).png")

        self.oak2_list = []

        self.oak2_list.append(self.oak2_m1_of_5)
        self.oak2_list.append(self.darwin2_m2_of_5)
        self.oak2_list.append(self.oak2_m3_of_5)
        self.oak2_list.append(self.oak2_m4_of_5)
        self.oak2_list.append(self.oak2_m5charmander_of_5)
        self.oak2_list.append(self.oak2_m5squirtle_of_5)
        self.oak2_list.append(self.oak2_m5bulbasaur_of_5)

        

        # Second set of dialogue images
        self.oak3_m1_of_6 = arcade.Sprite("images/oak3/oak3-1.png")
        self.oak3_m2_of_6 = arcade.Sprite("images/oak3/oak3-2.png")
        self.oak3_m3_of_6 = arcade.Sprite("images/oak3/oak3-3.png")
        self.oak3_m4_of_6 = arcade.Sprite("images/oak3/oak3-4.png")
        self.darwin3_m5_of_6 = arcade.Sprite("images/oak3/oak3-5.png")
        self.oak3_m6_of_6 = arcade.Sprite("images/oak3/oak3-6.png")
        

        self.oak3_list = []

        self.oak3_list.append(self.oak3_m1_of_6)
        self.oak3_list.append(self.oak3_m2_of_6)
        self.oak3_list.append(self.oak3_m3_of_6)
        self.oak3_list.append(self.oak3_m4_of_6)
        self.oak3_list.append(self.darwin3_m5_of_6)
        self.oak3_list.append(self.oak3_m6_of_6)
        


        



        self.oak4_list = []

        self.dialogue_master_list = []

        self.dialogue_master_list.extend(self.oak1_list)
        self.dialogue_master_list.extend(self.oak2_list)
        self.dialogue_master_list.extend(self.oak3_list)
        self.dialogue_master_list.extend(self.oak4_list)
        
        for i in self.dialogue_master_list:
            i.fading_in = True
            i.fading_out = False
            i.scale = 0.4
        

        self.darwin_dialogue = False

        for i in range(50):
            heart = arcade.Sprite("images/heart.png", scale = 0.01)
            heart.has_point = False
            heart.growing = False
            self.heart_list.append(heart)


        for i in self.hist_list:
            i.mating_point = False
            i.pairing = ""
            i.point = ""
            i.paired_x = False
            i.paired_y = False
            i.faded_in = False

        self.paired_count = 0

    
        self.breeding_coordinates = []

        self.used_coords = []

        self.hist_coords_given = False

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


        #### EXPERIMENTAL: TRYING TO CREATE TEN DIFFERENT VARIANTS ACROSS A GRADIENT ####
        self.organism_var1_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var2_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var3_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var4_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var5_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var6_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var7_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var8_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var9_sprite = arcade.Sprite(self.starter_organism)
        self.organism_var10_sprite = arcade.Sprite(self.starter_organism)

        self.experimental_list = arcade.SpriteList()

        self.experimental_list.append(self.organism_var1_sprite)
        self.experimental_list.append(self.organism_var2_sprite)
        self.experimental_list.append(self.organism_var3_sprite)
        self.experimental_list.append(self.organism_var4_sprite)
        self.experimental_list.append(self.organism_var5_sprite)
        self.experimental_list.append(self.organism_var6_sprite)
        self.experimental_list.append(self.organism_var7_sprite)
        self.experimental_list.append(self.organism_var8_sprite)
        self.experimental_list.append(self.organism_var9_sprite)
        self.experimental_list.append(self.organism_var10_sprite)


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
        self.organism_mean_sprite.alpha = 50
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
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)

        # First Death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        # Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)

        # Second Death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING)
        self.organism_mean_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING)
        #self.organism_mean_sprite.textures.append(texture)


        # Textures for the smallest variant of the organism
        # No deaths
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR)
        #self.organism_low_var_sprite.textures.append(texture)
        

        # First death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.1)
        #self.organism_low_var_sprite.textures.append(texture)

        # Second death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        self.organism_low_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        self.organism_low_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_LOW_VAR*1.2)
        #self.organism_low_var_sprite.textures.append(texture)


        # Textures for the largest variant of the organism
        # No deaths
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR)
        #self.organism_high_var_sprite.textures.append(texture)

        # First death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.9)
        #self.organism_high_var_sprite.textures.append(texture)

        # Second death
        texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
        self.organism_high_var_sprite.textures.append(texture)
        texture = arcade.load_texture(self.starter_organism, mirrored=True, scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
        self.organism_high_var_sprite.textures.append(texture)
        #Eliminating mated texture
        #texture = arcade.load_texture(self.starter_organism, scale=self.CHARACTER_SCALING_HIGH_VAR*0.8)
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
        #arcade.schedule(self.make_enemy, 5)
        
        self.enemy_list.append(self.enemy)

        # Set up Darwin (end of level)
        self.darwin_sprite = arcade.Sprite("images/darwin.png")

        self.darwin_sprite.sound_effect_annoyed = "sounds/darwin_annoyed.wav"
        self.darwin_annoyed_sound = arcade.load_sound(self.darwin_sprite.sound_effect_annoyed)
        self.darwin_sound_1_played = False

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

        stander = arcade.Sprite(self.starter_organism, STATIC_CHARACTER_SCALING)
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


    def redefine_hist_sprites(self):

        self.hist_list = arcade.SpriteList()
        
        self.hist_sprite_1 = arcade.Sprite(self.starter_organism, self.CHARACTER_SCALING_LOW_VAR)
        self.hist_sprite_1.center_y = self.hist_floor - 5
        self.hist_sprite_1.center_x = 100

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

    def update_scaling(self, starter_string):
        if "bulbasaur" == starter_string:
            if self.level == 1:
                self.CHARACTER_SCALING = bulbasaur_scaling * starting_mean
                print("Bulbasaur updated!")
                self.var = self.var * bulbasaur_scaling
                print("New variance:", self.var)
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.005)
                # A demo for the "1-10" mode: this will be two standard deviations smaller than the mean
                self.CHARACTER_SCALING_VAR_1 = self.CHARACTER_SCALING - (self.std_dev*2)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.005)
                #print("Scaled to bulbasaur")
            elif self.level > 1:
                self.CHARACTER_SCALING = bulbasaur_scaling * self.CHARACTER_SCALING
                print("Bulbasaur updated!")
                self.var = self.var * bulbasaur_scaling
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.005)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.005)


        elif "charmander" == starter_string:
            if self.level == 1:
                self.CHARACTER_SCALING = charmander_scaling * starting_mean
                print("charmander updated!")
                self.var = self.var * charmander_scaling
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.005)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.005)
                
                #print("Scaled to charmander")
            elif self.level > 1:
                self.CHARACTER_SCALING = charmander_scaling * self.CHARACTER_SCALING
                print("charmander updated!")
                self.var = self.var * charmander_scaling
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.005)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.005)

        elif "squirtle" == starter_string:
            if self.level == 1:
                self.CHARACTER_SCALING = squirtle_scaling * starting_mean
                print("squirtle updated!")
                self.var = self.var * squirtle_scaling
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.007)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.007)
                #print("Scaled to squirtle")
            elif self.level > 1:
                self.CHARACTER_SCALING = squirtle_scaling * self.CHARACTER_SCALING
                print("squirtle updated!")
                self.var = self.var * squirtle_scaling
                self.std_dev = numpy.sqrt(self.var)
                self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - (self.var * 0.007)
                self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + (self.var * 0.007)
        
        else:
            self.CHARACTER_SCALING = 0.2 * starting_mean
            self.CHARACTER_SCALING_LOW_VAR = self.CHARACTER_SCALING - pop_keeper.additive_genetic_variance_list[self.level-1]
            self.CHARACTER_SCALING_HIGH_VAR = self.CHARACTER_SCALING + pop_keeper.additive_genetic_variance_list[self.level-1]
            print("NO INDICATION!")

    def scale_everyone(self):
        self.organism_var1_sprite.scale = self.CHARACTER_SCALING - (self.std_dev*2)
        print(self.organism_var1_sprite.scale)
        self.organism_var2_sprite.scale = self.CHARACTER_SCALING - (self.std_dev*1.5)
        print(self.organism_var1_sprite.scale)
        self.organism_var3_sprite.scale = self.CHARACTER_SCALING - (self.std_dev)
        self.organism_var4_sprite.scale = self.CHARACTER_SCALING - (self.std_dev*0.5)
        self.organism_var5_sprite.scale = self.CHARACTER_SCALING - (self.std_dev*0.25)
        self.organism_var6_sprite.scale = self.CHARACTER_SCALING + (self.std_dev*0.25)
        self.organism_var7_sprite.scale = self.CHARACTER_SCALING + (self.std_dev*0.5)
        self.organism_var8_sprite.scale = self.CHARACTER_SCALING + (self.std_dev*1)
        self.organism_var9_sprite.scale = self.CHARACTER_SCALING + (self.std_dev*1.5)
        self.organism_var1_sprite.scale = self.CHARACTER_SCALING + (self.std_dev*2)

    def make_enemy(self, interval):
            enemy = arcade.Sprite("images/red_gyarados_right.png", ENEMY_SCALING)
            enemy.center_x = -150
            enemy.center_y = 90
            physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy, self.enemy_wall_list, GRAVITY)
            self.enemy_physics_engine_list.append(physics_engine_enemy)
            self.enemy_list.append(enemy)
        

    def on_draw(self):
        """ Render the screen. """
        starting_viewport = arcade.get_viewport()
        arcade.start_render()
        if self.current_state == "PREOPENING":
            self.draw_opening_screen()
            if self.current_state == "OPENING":

                self.current_state = "OPENING_RUNNING"


        if self.current_state == "OPENING_RUNNING":
            starting_viewport = self.get_viewport()
            
            mixer.music.play()
            self.qg_pokemon.alpha = 0
            self.intro_venusaur.alpha = 0
            
            self.current_state = "OPENING_RUNNING_2"
        if self.current_state == "OPENING_RUNNING_2":
            
            
            self.qg_pokemon.center_x = starting_viewport[0] + 370
            self.qg_pokemon.center_y = starting_viewport[2] + 160
            self.qg_pokemon.draw()

            for i in self.intro_pokemon:
                i.center_x = starting_viewport[0] + 370
                i.center_y = starting_viewport[2] + 400
        

            if not self.qg_pokemon.alpha == 255:
                self.qg_pokemon.alpha += 1
            #if not self.intro_venusaur.alpha >= 254:
            #    self.intro_venusaur.alpha += 2

            self.fade_in_sequence(self.intro_pokemon, 0, 3, lower_threshold=5, upper_threshold=10)


            for i in range(1):
                counter = 0
                for i in self.intro_pokemon:
                    if i.alpha < 5:
                        counter += 1
                if counter >= 3:
                    for i in self.intro_pokemon:
                        print("Hit that button!")
                        i.fading_in = True
                        i.fading_out = False
                        i.alpha = 255


        if self.current_state == "OAK1":
            
            
            self.draw_prof_oak()
            for message in self.oak1_list:
                self.position_oak_text(message)
                
         
            
            #self.fade_in_and_out_better(self.oak1_list[0])
            

            self.oak1_list[1].center_y = self.oak1_list[0].center_y - 30
            self.oak1_list[1].center_x = self.oak1_list[0].center_x + 107
            self.oak1_list[2].center_y = self.oak1_list[1].center_y - 35
            self.oak1_list[2].center_x = self.oak1_list[1].center_x + 22
           
            #self.fade_in_and_out_better(self.oak1_list[0])
            #self.fade_in_and_out_better(self.oak1_list[1])
            #self.fade_in_and_out_better(self.oak1_list[2])



            #self.oak1_list[0].draw()

            self.fade_in_sequence(self.oak1_list, 1, 4, rate_out=2)
            
            if (self.oak1_list[2].alpha >= 230) and (self.oak1_list[2].alpha < 255):
                self.darwin_dialogue = True

            if self.darwin_dialogue == True:
                #self.prof_oak_dialogue = False
                self.draw_charles_darwin()
                if self.darwin_sound_1_played == False:
                    annoyed = arcade.load_sound("sounds/darwin_annoyed.wav")
                    annoyed.play()
                    self.darwin_sound_1_played = True



                self.draw_darwin_text(self.oak1_list[3])
                self.draw_darwin_text(self.oak1_list[4])

                self.oak1_list[4].center_y -= 40
                self.oak1_list[4].center_x += 50



                self.fade_in_and_out_better(self.oak1_list[3], rate_in=6, rate_out=1)
                self.fade_in_and_out_better(self.oak1_list[4], rate_in=3, rate_out=1)

            if self.oak1_list[4].alpha < 250:
                self.oak1_list[5].center_x = self.oak1_list[0].center_x + 100
                self.oak1_list[5].center_y = self.oak1_list[0].center_y

                self.oak1_list[6].center_x = self.oak1_list[3].center_x
                self.oak1_list[6].center_y = self.oak1_list[3].center_y

                self.oak1_list[7].center_x = self.oak1_list[3].center_x - 40
                self.oak1_list[7].center_y = self.oak1_list[3].center_y - 40

                self.oak1_list[8].center_x = self.oak1_list[0].center_x + 100
                self.oak1_list[8].center_y = self.oak1_list[0].center_y
                
                

                self.fade_in_sequence(self.oak1_list, 0, 9, rate_out=4)

                
               


            #self.oak1_list[1].draw()
            #self.oak1_list[2].draw()



        if self.current_state == ("SPECIES_SELECTION"):
            
            arcade.start_render()
            self.draw_species_selection_text()
            self.draw_characters()
        elif self.current_state == ("SELECT_FOCUS"):
            arcade.start_render()
            self.draw_species_selection_text()

        elif self.current_state == ("FOCUS_SELECTED"):
            arcade.start_render()
            self.draw_species_selection_text()


        if self.current_state == "GAME":
            self.draw_game()


    def draw_focus_choice_text(self):
        pass


    def position_oak_text(self, message):
        new_viewport = arcade.get_viewport()
        
        
        message.center_x = new_viewport[0] + 150
        message.center_y = new_viewport[2] + 200


    def fade_in_and_out_better(self, target, rate_in=1, rate_out=1):

        if (target.fading_in == True) and (target.alpha == 255):
            target.alpha = 0

        if target.fading_in == True:
            target.alpha += rate_in

        if (target.fading_in == True) and target.alpha > 240:
            target.fading_in = False
            target.fading_out = True

        if (target.fading_out == True) and (target.alpha > 0):
            target.alpha -= rate_out

        elif (target.fading_out == True) and (target.alpha <= 0):
            target.alpha = 0

        if target.alpha > 0:
            target.draw()


        #if (target.fading_in == True) and (target.alpha == 255):
        #    target.alpha = 0
        #    print("it happened again!")
        
        #elif (target.alpha < 255) and (target.fading_in == True):
        #    target.alpha += 2
            #print("increasing")
        
        #elif (target.alpha > 245) and (target.fading_in == True):
        #    target.fading_in = False
        #    target.fading_out = True
        #    print("A switch")
        
        #elif (target.fading_out == True):
        #    target.alpha -= 1
            #print("Decreasing")
        
        #elif (target.fading_out == True) and (target.alpha == 0):
        #    target.alpha = 0
        #    print("Triggered!")
        
        


    def fade_in_sequence(self, target_list, start_range, end_range, rate_in=1, rate_out=1, lower_threshold=100, upper_threshold=255):
        self.fade_in_and_out_better(target_list[0], rate_in, rate_out)
        
        for i in range(len(target_list[start_range:end_range])):
            if (target_list[i-1].alpha < upper_threshold) and (target_list[i-1].fading_out == True):
                self.fade_in_and_out_better(target_list[i], rate_in, rate_out)
                #### CURRENTLY AN ISSUE WHERE THE FIRST ONE FLICKERS--FIX THIS BY MAKING THIS METHOD NOT APPLY TO THE ONE CALLED ALONE BEFOREHAND ###
            elif (target_list[i].fading_out == True) or (target_list[i].alpha != 255):
                self.fade_in_and_out_better(target_list[i], rate_in, rate_out)

                #if target_list[i].alpha <= 125 and (target_list[i].fading_out == False):
                #    if ((i+1) < len(target_list)) and (target_list[i-1].fading_out == False):
                #        target_list[i+1].alpha = 0
                
               #     else:
                #        pass
                #elif target_list[i].alpha >= 125:
                    #target_list[i].draw()




    def draw_darwin_text(self, message):
        new_viewport = arcade.get_viewport()
        
        
        message.center_x = new_viewport[0] + 300
        message.center_y = new_viewport[2] + 400

        
       
            


    def draw_charles_darwin(self):
        starting_viewport = arcade.get_viewport()

        self.darwin_sprite.set_texture(0)

        self.darwin_sprite.center_x = starting_viewport[0] + 100
        self.darwin_sprite.center_y = starting_viewport[2] + 500

        self.darwin_sprite.draw()



    def draw_prof_oak(self):
        starting_viewport = arcade.get_viewport()



        self.prof_oak.center_x = starting_viewport[0] + 620
        self.prof_oak.center_y = starting_viewport[2] + 100
            
        if self.prof_oak.alpha == 255:
            self.prof_oak.alpha = 0
        self.prof_oak.draw()
        if self.prof_oak.alpha <= 245:
            self.prof_oak.alpha += 5
        

            
    def increase_opacity(self, target):
        target.alpha += 2
        
        self.pre_intro_1_started = True
        if target.faded == True:
            self.pre_intro_2_started = True
         #   self.warlak_pre = True

    def decrease_opacity(self, target):
        target.alpha -= 2
        self.pre_intro_1_started = True
        if target.faded == True:
            self.pre_intro_2_started = True
        #    self.warlak_pre = True
        


    def fade_in_and_out(self, target, switch):
        if switch == False:
            target.alpha = 0
            target.fading_in = True
            
            
        target.draw()
        

        if (target.alpha < 255) and (target.fading_in == True):
            self.increase_opacity(target)
            
        if target.alpha >= 255:
            target.fading_in = False
        
        if (target.fading_in == False) and (target.alpha > 0):
            self.decrease_opacity(target)
        if (target.alpha <= 0):
            target.faded = True
            if target.fade_count > 1:
                self.current_state = "OPENING"
            target.fade_count += 1
            self.pre_2_ready = True

            


    def draw_opening_screen(self):
        arcade.set_background_color((0,0,0))
        
        viewport = arcade.get_viewport()
        
        if not self.pre_2_ready:
            self.jake.center_x = viewport[0] + 400
            self.jake.center_y = viewport[2] + 300
            self.fade_in_and_out(self.jake, self.pre_intro_1_started)
        
        #self.increase_opacity()
        

        if self.jake.alpha == 0:
            self.jake.set_texture(0)
        
        if self.pre_2_ready == True:  
              
            self.jake.center_x = viewport[0] + 400
            self.jake.center_y = viewport[2] + 360
            self.fade_in_and_out(self.jake, self.pre_intro_2_started)
            #self.fade_in_and_out(self.warlak, self.warlak_pre)
            

        #if (self.jake.faded == True) and (self.pre_2_ready == True):
        #    self.current_state = "OPENING"






        if self.current_state == "OPENING":
            
            self.current_state = "OPENING_RUNNING"
        if self.current_state == "OPENING_RUNNING":
            mixer.music.play()
            print("In opening running 1")

        
        
        
        

        

        #riding_night_sound.pause()



    def on_mouse_press(self, x, y, button, modifiers):
        select = arcade.load_sound("sounds/select.wav")

        if self.current_state == "OPENING_RUNNING_2":
            self.current_state = "OAK1"
            mixer.music.fadeout(3000)
            medley = mixer.music.load(self.pokemon_medley)
            mixer.music.play()
            print("Post-music")

        elif self.current_state == "OAK1":
            self.current_state = "SPECIES_SELECTION"

        if self.current_state == "SELECT_FOCUS":

            for i in self.hist_list:
                new_check = i.collides_with_point((x, y))
                if new_check == True:
                    self.horse_bet_on = i.scale
                    arcade.play_sound(select)
                    self.current_state = "FOCUS_SELECTED"
        
        if self.current_state == "SPECIES_SELECTION":
            
            
            
            if button == arcade.MOUSE_BUTTON_LEFT:
                #for i in self.starters_list:
                #    print("A POKEMON: ", i)

                bulbasaur_check = self.starters_list[0].collides_with_point((x, y))
                charmander_check = self.starters_list[1].collides_with_point((x, y))
                squirtle_check = self.starters_list[2].collides_with_point((x, y))


            i = 0

            if len(self.starter_string) < 1:
                if bulbasaur_check == True:
                    self.starter_organism = self.starter_organism_dict["bulbasaur"]
                    self.starter_string = "bulbasaur"
                    
                    arcade.play_sound(select)
                    #self.current_state = "SPECIES CHOSEN"
                    #print("Bulbasaur!")
                    i += 1
                elif charmander_check == True:
                    self.starter_organism = self.starter_organism_dict["charmander"]
                    self.starter_string = "charmander"
                    arcade.play_sound(select)
                    
                    #self.current_state = "SPECIES CHOSEN"
                    #print("Charmander!")
                    i += 1
                elif squirtle_check == True:
                    self.starter_organism = self.starter_organism_dict["squirtle"]
                    self.starter_string = "squirtle"
                    arcade.play_sound(select)
                    
                    #self.current_state = "SPECIES CHOSEN"
                    #print("Squirtle!")
                    i += 1

                if i > 0:
                    self.species_selected = True

            print("Oak is still talking: ", self.prof_oak_dialogue)
            

                

    

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

        self.hist_coords_given = True


    def draw_game(self):
        # NOTE: THIS IS WORKING TO PRODUCE EXTINCTION IN THE MIDDLE OF THE SCREEN!

        arcade.start_render()
        if self.current_music != self.game_music and self.level_complete == False:
            self.current_music = self.game_music
            mixer.music.load(self.game_music)
            mixer.music.play()
            arcade.set_background_color((230, 143, 255))


        new_viewport = arcade.get_viewport()

        mean_text = f"Average size: {str(pop_keeper.mean_phenotypic_trait_value_list[self.level-1])[:4]}"
        var_text = f"Additive genetic variance: {str(pop_keeper.additive_genetic_variance_list[self.level-1])[:4]}"

        arcade.draw_text(mean_text, new_viewport[0] + 450, new_viewport[2] + 500, 
                         arcade.csscolor.WHITE, 10)


        arcade.draw_text(var_text, new_viewport[0] + 450, new_viewport[2] + 480, 
                         arcade.csscolor.WHITE, 10)
        
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

            new_viewport = arcade.get_viewport()

            if not self.ready_to_breed:
                #leftovers_text = f"WHO'S LEFT: "
                #arcade.draw_text(leftovers_text, new_viewport[0] + 250, new_viewport[2] + 400, 
                #         arcade.csscolor.WHITE, 40)
                pass

            if self.honeymoon_ready == True:
                self.heart_list.draw()

            low_var_base_x = new_viewport[0]

            if self.hist_coords_given == False:
                self.give_hist_coordinates(new_viewport)
            
            # Note: Viewport bottom is -57 and current hist_list[1] is 115 - 50


            if self.hist_fading_in == False:
                for i in self.hist_list:
                    i.alpha = 0

            self.hist_fading_in = True

            if self.hist_fading_in == True:
                for i in self.hist_list:
                    if (i.alpha < 255) and (i.faded_in == False):
                        i.alpha += 5
                    elif i.alpha == 255:
                        i.alpha = 255
                        i.faded_in = True



            

            

            # Draws the leftmost tail of the histogram only if none of the tiny guys died!

            # Leftmost column, only individual (1/1)
            self.hist_list[0].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT].scale
            #self.hist_list[0].center_x = low_var_base_x + 200
            self.hist_list[0].draw()

            if self.organism_low_var_sprite.deaths >= 1:
                if (self.hist_list[0].alpha > 0) and (self.hist_list[0].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[0].alpha -= 5
            

            
            
            # Second column from the left, top spot (2/2)
            self.hist_list[1].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT_SECOND_DEATH].scale
                #self.hist_list[1].center_x = low_var_base_x + 285
            self.hist_list[1].draw()
            if self.organism_low_var_sprite.deaths >= 3:
                if (self.hist_list[1].alpha > 0) and (self.hist_list[1].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[1].alpha -= 5


            # Second column from the left, bottom spot (1/2)
            self.hist_list[2].scale = self.organism_low_var_sprite.textures[TEXTURE_LEFT_FIRST_DEATH].scale
            self.hist_list[2].draw()


            if self.organism_low_var_sprite.deaths >= 2:
                if (self.hist_list[2].alpha > 0) and (self.hist_list[2].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[2].alpha -= 5
            

            # Third column from the left, uppermost spot (4/4)
            self.hist_list[3].draw()
            if self.organism_mean_sprite.deaths >= 4:
                if (self.hist_list[3].alpha > 0) and (self.hist_list[3].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[3].alpha -= 5


            # Third column from the left, penultimate spot (3/4)
            if self.organism_mean_sprite.deaths >= 3:
                if (self.hist_list[4].alpha > 0) and (self.hist_list[4].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[4].alpha -= 5
            self.hist_list[4].draw()

            # Third column from the left, second from the bottom (2/4)
            if self.organism_mean_sprite.deaths >= 2:
                if (self.hist_list[5].alpha > 0) and (self.hist_list[5].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[5].alpha -= 5
            self.hist_list[5].draw()

            # Third column from the left, bottom spot (1/4)
            if self.organism_mean_sprite.deaths >= 1:
                if (self.hist_list[6].alpha > 0) and (self.hist_list[6].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[6].alpha -= 5
            self.hist_list[6].draw()

            # Second from right column, bottom individual (1/2)
            if self.organism_high_var_sprite.deaths >= 3:
                if (self.hist_list[7].alpha > 0) and (self.hist_list[7].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[7].alpha -= 5
            self.hist_list[7].scale = self.organism_high_var_sprite.textures[TEXTURE_LEFT_SECOND_DEATH].scale
            self.hist_list[7].draw()

            # Second-from-right column, top individual (2/2)
            if self.organism_high_var_sprite.deaths >= 2:
                if (self.hist_list[8].alpha > 0) and (self.hist_list[8].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[8].alpha -= 5
            self.hist_list[8].scale = self.organism_high_var_sprite.textures[TEXTURE_LEFT_FIRST_DEATH].scale
            self.hist_list[8].draw()

            # Rightmost column, only individual (1/1)
            if self.organism_high_var_sprite.deaths >= 1:
                if (self.hist_list[9].alpha > 0) and (self.hist_list[9].faded_in == True) and (self.prof_oak_key_pressed_2):
                    self.hist_list[9].alpha -= 5
            self.hist_list[9].draw()
            
            
            

            
            self.calculate_losses()

            #if self.making_histogram == True:
                #self.get_change_after_selection()
            
            if self.selection_calculated == False:
                print(self.selection_calculated)
                self.get_change_after_selection()
                self.selection_calculated = True


            if self.prof_oak_key_pressed_1 == True:
                    
                    self.prof_oak_dialogue = True
                    if self.prof_oak_dialogue == True:
                        self.draw_prof_oak()
                        for message in self.oak4_list:
                            self.position_oak_text(message)
                    
            


            #print(self.loss_list)
            #self.making_histogram = False
            
            if self.level_complete and self.go_to_next_level:
                
                self.start_new_level(self.level)
                #self.level_complete = False
            


        

    def set_breeding_coordinates(self, viewport):
        left = viewport[0]
        width = viewport[1] 
        bot = viewport[2]
        height = viewport[3]

        self.breeding_coordinates = [
                # First pair
                
                # Left
                [left + 500, 100],
                #Right
                [left + 550, 100],

                # Second pair

                # Left
                [left + 150, 200],
                #Right
                [left + 200, 200],

                # Third pair

                # Left
                [left + 250, 450],
                #Right
                [left + 300, 450],

                # Fourth pair

                # Left
                [left + 260, 300],
                #Right
                [left + 310, 300],

                # Fifth pair

                # Left
                [left + 320, 100],
                #Right
                [left + 370, 100]

        ]


    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        
        current_viewport = arcade.get_viewport()

        #### NOT YET ABLE TO GET EVERYONE FLYING OFF AND BREEDING ####
        if key:
            if (self.current_state == "SPECIES_SELECTION") and (len(self.starter_string) > 1):
                self.current_state = "SELECT_FOCUS"

            if (len(self.starter_string) > 1) and (self.current_state == "READY_FOR_GAME"):
                self.start_game = True
            if self.current_state == ("PREOPENING"):
                self.current_state = "OPENING_RUNNING"
                print("getting it...")
            if self.current_state == "GAME":
                if self.prof_oak_key_pressed_1 == True:
                    self.prof_oak_key_pressed_2 = True

                if self.making_histogram == True:
                    self.prof_oak_key_pressed_1 = True

                    

        if (key == arcade.key.SPACE) and (self.level_complete == True):
            if self.prof_oak_key_pressed_2 == True:
                self.ready_to_breed = True
                print("Ready to breed?", self.ready_to_breed)
                
        
        if key == arcade.key.ENTER:
            if self.current_state == "PREOPENING":
                pass
            if self.ready_to_breed == True:
                current_viewport = arcade.get_viewport()
                
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
                    self.organism_mean_sprite.change_y = int(ORGANISM_MEAN_JUMP_SPEED)
                
                if self.physics_engine_low_var.can_jump():
                    self.organism_low_var_sprite.change_y = int(ORGANISM_LOW_VAR_JUMP_SPEED)
                
                if self.physics_engine_high_var.can_jump():
                    self.organism_high_var_sprite.change_y = int(ORGANISM_HIGH_VAR_JUMP_SPEED)

                #arcade.play_sound(self.jump_sound)
            if key == arcade.key.DOWN or key == arcade.key.S:
                self.organism_mean_sprite.change_y = -int(ORGANISM_MEAN_MOVEMENT_SPEED)
                self.organism_low_var_sprite.change_y = -int(ORGANISM_LOW_VAR_MOVEMENT_SPEED)
                self.organism_high_var_sprite.change_y = -int(ORGANISM_HIGH_VAR_MOVEMENT_SPEED)

            if key == arcade.key.LEFT or key == arcade.key.A:
                self.organism_mean_sprite.set_texture(self.organism_mean_sprite.current_left)
                self.organism_mean_sprite.change_x = -int(ORGANISM_MEAN_MOVEMENT_SPEED)
                self.organism_low_var_sprite.set_texture(self.organism_low_var_sprite.current_left)
                self.organism_low_var_sprite.change_x = -int(ORGANISM_LOW_VAR_MOVEMENT_SPEED)
                self.organism_high_var_sprite.set_texture(self.organism_high_var_sprite.current_left)
                self.organism_high_var_sprite.change_x = -int(ORGANISM_HIGH_VAR_MOVEMENT_SPEED)

            
            if key == arcade.key.RIGHT or key == arcade.key.D:
                self.organism_mean_sprite.set_texture(self.organism_mean_sprite.current_right)
                self.organism_mean_sprite.change_x = int(ORGANISM_MEAN_MOVEMENT_SPEED)
                self.organism_low_var_sprite.set_texture(self.organism_low_var_sprite.current_right)
                self.organism_low_var_sprite.change_x = int(ORGANISM_LOW_VAR_MOVEMENT_SPEED)
                self.organism_high_var_sprite.set_texture(self.organism_high_var_sprite.current_right)
                self.organism_high_var_sprite.change_x = int(ORGANISM_HIGH_VAR_MOVEMENT_SPEED)

                #self.enemy.change_x = ENEMY_MOVEMENT_SPEED
                #self.enemy.change_y = self.enemy.center_y - self.focal_organism.center_y

                self.start_time = int(time.time())


            if key:
                for enemy in self.enemy_list:
                    enemy.change_x = int(ENEMY_MOVEMENT_SPEED)
                    enemy.change_y = int(self.focal_organism.change_y)
                    
                    if (enemy.center_x > self.darwin_sprite.center_x) or (enemy.center_y < current_viewport[2]) or (enemy.center_y > (current_viewport[2] + current_viewport[3])):
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
            
            for org in self.player_list:
                org.alpha = 50
            
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

            self.focal_organism.alpha = 255









  

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

            #self.enemy_list.update()

            self.hist_list.update()

            #self.physics_engine_hist_1.update()

            # Update histogram
            #self.physics_engine_hist_1.update()
            #self.physics_engine_hist_2.update()
            
            






            if self.level_complete:
                self.quick_sunset = True
                # Note: the increment value here is meaningless because quick sunset takes over
                #self.sunset(self.start_time)


            # Accelerated sunset when the level is ending

            elif self.start_time and (self.level_complete == False) and (self.debriefing == False):
                
                pass
                #self.sunset(self.start_time, 2)

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
                    mixer.music.fadeout(5000)
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


    def draw_species_selection_text(self):
        new_viewport = self.get_viewport()

        self.draw_prof_oak()
        self.draw_charles_darwin()
        for message in self.oak2_list:
            self.position_oak_text(message)

        self.oak2_list[0].center_x += 100

        self.oak2_list[1].center_y += 300
        self.oak2_list[1].center_x += 150

        self.oak2_list[2].center_y -= 50
        self.oak2_list[2].center_x += 90
        
        self.oak2_list[3].center_y -= 100
        self.oak2_list[3].center_x += 80

        self.fade_in_sequence(self.oak2_list, 0, 4)

        self.prof_oak_dialogue = True

        for i in self.oak2_list[3:]:
            i.center_x += 100
            i.center_y += 50

        if self.starter_string:
            for i in self.oak2_list[:4]:
                i.alpha = 0
        if self.starter_string == "charmander":
            self.fade_in_and_out_better(self.oak2_list[4], rate_in=5)

        elif self.starter_string == "squirtle":
            self.fade_in_and_out_better(self.oak2_list[5], rate_in=5)

        elif self.starter_string == "bulbasaur":
            self.fade_in_and_out_better(self.oak2_list[6], rate_in=5)


        self.redefine_hist_sprites()
        self.give_hist_coordinates(new_viewport)
        #print(self.starter_string)
        
        if self.starter_string:
            # The problem is that if you keep doing this, it creates a recursive loop
            # Where you're always multiplying the thing by itself, a smalll fraction, plus another small fraction
            self.update_scaling(self.starter_string)
            self.scale_everyone()

            print(self.CHARACTER_SCALING)
            


        

            

        if (self.current_state == "SELECT_FOCUS") or (self.current_state == "FOCUS_SELECTED"):
            
            self.draw_charles_darwin()
            self.draw_prof_oak()
            for i in self.oak2_list:
                i.alpha = 0
            self.draw_population_choice_text()
            self.draw_choosable_histogram()
            


        if self.start_game == True:
            self.current_state = "GAME"
            self.setup()

        #output = "CHOOSE YOUR CHARACTER"
        #arcade.draw_text(output, new_viewport[0]+50, new_viewport[2]+350, arcade.color.WHITE, 40)


    def draw_choosable_histogram(self):
        if self.current_state == "SELECT_FOCUS":
            for i in self.hist_list:
                i.center_x -= 140
                
                i.draw()

    def draw_population_choice_text(self):
        if self.current_state == "SELECT_FOCUS":
            for i in self.oak3_list:
                self.position_oak_text(i)
                i.center_x += 350
                i.center_y += 150
            self.oak3_list[4].center_y += 150
            self.oak3_list[4].center_x -= 150

            self.oak3_list[1].center_y -= 50
            self.oak3_list[3].center_y -= 50

            self.fade_in_sequence(self.oak3_list, 0, 6)
            

    def draw_characters(self):
        current_viewport = self.get_viewport()

        bulbasaur = arcade.Sprite("images/bulbasaur_left.png", bulbasaur_scaling*5)
        charmander = arcade.Sprite("images/charmander_left.png", charmander_scaling*5)
        squirtle = arcade.Sprite("images/squirtle_left.png", squirtle_scaling*5)

        self.starters_list = arcade.SpriteList()
        self.starters_list.append(bulbasaur)
        self.starters_list.append(charmander)
        self.starters_list.append(squirtle)   

        
        bulbasaur.center_x = int(current_viewport[0] + 120)
        bulbasaur.center_y = int(current_viewport[2] + 350)

        charmander.center_x = int(current_viewport[0] + 370)
        charmander.center_y = int(current_viewport[2] + 350)

        squirtle.center_x = int(current_viewport[0] + 620)
        squirtle.center_y = int(current_viewport[2] + 350)

        #for i in range(len(starters_list)):
        #   starters_list[i].center_x = current_viewport[0] + (i)*50
        #   starters_list[i].center_y = current_viewport[2] + 250

        self.starters_list.draw()


        self.draw_prof_oak()
        
        
            
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

    def get_change_after_selection(self):
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
        print("Mean before scaling: ", self.CHARACTER_SCALING)


    def start_new_level(self, level):

        # Resets this for the next go-around
        self.go_to_next_level = False

        #self.get_change_after_selection()
        self.setup(level, self.CHARACTER_SCALING)

        #### DEMO FOR NEW TEXTURES USING MULTIPLE CHARACTERS ####
        



        self.level_complete = False
        self.ready_to_breed = False
        self.making_histogram = False

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
        if self.current_music != self.love_music:
            self.current_music = self.love_music
            mixer.init()
            mixer.music.load(self.love_music)
            mixer.music.play()
            mixer.music.fadeout(6000)
            print("Should've played!")

        #self.honeymoon_ready = True
        self.set_breeding_coordinates(current_viewport)
        
        for i in range(len(self.hist_list)):
            g = i - 1

            breeding_coordinates = self.breeding_coordinates

            if self.hist_list[g].mating_point == False:
                # Establish semi-permanent mating coordinates for each organism
                self.hist_list[g].point = numpy.random.randint(0, len(breeding_coordinates))
            
            # Shorthand
            point = self.hist_list[g].point

            # Flip a switch so that all organisms don't continue to get new points
            if breeding_coordinates[point] not in self.used_coords:
                self.hist_list[g].mating_point = True
        
            
            

            
            
            
            if self.hist_list[g].center_x == breeding_coordinates[point][0]:
                self.hist_list[g].change_x = 0
                self.hist_list[g].paired_x = True
            elif self.hist_list[g].center_x > (breeding_coordinates[point][0]):
                self.hist_list[g].change_x = -5
            elif self.hist_list[g].center_x < (breeding_coordinates[point][0]):
                self.hist_list[g].change_x = 5
            

            


            
            if self.hist_list[g].center_y > (breeding_coordinates[point][1]):
                self.hist_list[g].change_y = -5
            elif self.hist_list[g].center_y < (breeding_coordinates[point][1]):
                self.hist_list[g].change_y = 5
            else:
                self.hist_list[g].change_y = 0
                self.hist_list[g].paired_y = True

            

            self.used_coords.append(breeding_coordinates[point])
        if not self.paired_count >= 10:
            self.paired_count = 0

            for i in self.hist_list:
                if (i.paired_y and i.paired_x) == True:
                    self.paired_count += 1
        if self.paired_count >= 10:
            self.honeymoon()


            #if len(breeding_coordinates[pairing]) == 0:
               # breeding_coordinates.pop(breeding_coordinates.index(breeding_coordinates[pairing]))
        
            
            

        
        
        


    def honeymoon(self):
        self.honeymoon_ready = True
        new_viewport = arcade.get_viewport()
        random_mating = "Random Mating!"
        arcade.draw_text(random_mating, new_viewport[0] + 450, new_viewport[2] + 500, 
                         arcade.csscolor.WHITE, 40)
        for i in self.hist_list:
            i.change_y = 5

        for heart in self.heart_list:
            if heart.has_point == False:
                heart.center_x = numpy.random.randint(new_viewport[0]-100, new_viewport[1]-200)
                heart.center_y = numpy.random.randint(new_viewport[2], new_viewport[3])
                heart.has_point = True
            if heart.growing == True:
                heart.scale += 0.001
            elif heart.growing == False:
                heart.scale -= 0.001
            if heart.scale <= 0.01:
                heart.growing = True
            elif heart.scale >= 0.04:
                heart.growing = False
        
        
        

        
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
