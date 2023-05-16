########################################################
# adapted from Python Aracde Example Games
#
# 💻 Experiment with the settings, see what you discover!
########################################################


import arcade


# 💻 Try changing these numbers to adjust the scale of the game
TILE_SCALING = 1
PLAYER_SCALING = 1

# Grid Size
SPRITE_PIXEL_SIZE = 28
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Screen Settings
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
SCREEN_TITLE = "Map Making"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 20
VIEWPORT_RIGHT_MARGIN = 60
VIEWPORT_LEFT_MARGIN = 60

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 20
GRAVITY = 1.1


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.game_over = False
        self.score = 0
        
     
        """Set up the game and initialize the variables."""

        # Set up the player
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            "assets/sprites/slime.png",
            PLAYER_SCALING,
        )

        self.player_sprite.center_x = 250
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)

        # sets up map
        map_name = "assets/map/forest_map.tmj"

        layer_options = {
            "Walls": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
            "End": {"use_spatial_hash": True}
        }

        # read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=TILE_SCALING
        )

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # sets wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.end_list = self.tile_map.sprite_lists["End"]
        self.background_list = self.tile_map.sprite_lists["Background"]

  
        # sets the background color
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        # Keep player from running through the wall_list layer
        walls = [self.wall_list, ]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=GRAVITY
        )

        # sets up camera 
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # center camera on user
        self.pan_camera_to_user()


    def on_draw(self):
        """
        Render the screen.
        """

        # These commands must happen before we start drawing
        self.camera.use()
        self.clear()

        # draw all the map
        self.background_list.draw()
        self.end_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        # draws the sprites
        self.player_list.draw()

        if self.game_over == True:
            x_pos = self.player_sprite.center_x+100
            y_pos = self.player_sprite.center_y+100
            text_size = 25

            arcade.draw_text(f"Score: {self.score}", x_pos, y_pos, arcade.color.WHITE, text_size)
    

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # if player hits the 'End' map layer, end game
        if arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.end_list
        ):
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()


        # if player collides with a coin
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.coin_list
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
           

        # pans camera to the user
        self.pan_camera_to_user(panning_fraction=0.12)

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """ Manage Scrolling """

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 3
        )
        
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)


if __name__ == "__main__":
    window = MyGame()
    arcade.run()