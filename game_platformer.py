############################################
# 💻 Experiment with the settings, see what you discover!
############################################


import arcade
from helpers import fixCrash

class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """

        self.screen_width = 800
        self.screen_height = 600

        super().__init__(
            width = self.screen_width, 
            height = self.screen_height, 
            title = "Game 1")


        # Physics
        self.MOVEMENT_SPEED = 5
        self.JUMP_SPEED = 25
        self.GRAVITY = 1.1

        # game over
        self.game_over = False
        
     
        """Set up the game and initialize the variables."""

        # Set up the player
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            "assets/sprites/slime.png",
            scale = 2,
            center_x = 250,
            center_y = 270,
        )

        # loads another version of the sprite image, flipped 
        texture = arcade.load_texture("assets/sprites/slime.png",
                                      flipped_horizontally=True)
        
        self.player_sprite.textures.append(texture)

    
        self.player_list.append(self.player_sprite)

        # sets up map
        map_name = "assets/map/forest_map.tmj" 

        layer_options = {
            "Walls": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
            "End": {"use_spatial_hash": True}
        }

        # map scaling
        self.TILE_SCALING = 2
        self.SPRITE_PIXEL_SIZE = 128
        self.GRID_PIXEL_SIZE = self.SPRITE_PIXEL_SIZE * self.TILE_SCALING

        # read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, 
            layer_options=layer_options,
              scaling=self.TILE_SCALING
        )

        self.end_of_map = self.tile_map.width * self.GRID_PIXEL_SIZE

        # sets wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.end_list = self.tile_map.sprite_lists["End"]
        self.background_list = self.tile_map.sprite_lists["Background"]
  
        # sets the background color
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        # Keep player from running through the wall_list layer
        walls = [self.wall_list]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=self.GRAVITY
        )

        # sets up camera 
        self.camera = arcade.Camera(self.screen_width, self.screen_height)

        # center camera on user
        self.pan_camera_to_user()

        # creates score
        self.score = 0


    def on_draw(self):
        """
        Render the screen.
        """

        # if game is not over, draw everything

        if self.game_over == False:
            self.camera.use()
            self.clear()

            # draws the player
            self.player_list.draw()
            
            # draws the map layers
            self.background_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()
            self.end_list.draw()

            # draws the score
            arcade.draw_text(
                f"Score: {self.score}",
                self.camera.position[0] + 25,  
                self.camera.position[1]+ 550,  
                arcade.color.BLACK,
                20,  
        )
  
        # else, the game is over - only draw text
        else :
            self.clear()

            arcade.draw_text(
                f"Game Over",
                self.camera.position[0]+ self.screen_width/3,
                self.camera.position[1]+ self.screen_height/2,
                arcade.color.BLACK,
                40
            )

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key == arcade.key.W:
            self.player_sprite.change_y = self.JUMP_SPEED

        elif key == arcade.key.A:
            self.player_sprite.change_x = -self.MOVEMENT_SPEED

            # switches the current player's sprite texture to face to the left
            self.player_sprite.texture = self.player_sprite.textures[1]

        elif key == arcade.key.D:
            self.player_sprite.change_x = self.MOVEMENT_SPEED

            # switches the current player's sprite texture to face to the right
            self.player_sprite.texture = self.player_sprite.textures[0]

        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # prevent the player from falling off the left side of the map
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0


        # if player hits the 'End' map layer, end game
        if arcade.check_for_collision_with_list(self.player_sprite, self.end_list):
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()


        # manages if a player hits a coin
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Pan to the user
        self.pan_camera_to_user(panning_fraction=0.12)

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """ Manage Scrolling """

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/3)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)


if __name__ == "__main__":
    fixCrash()
    window = MyGame()
    arcade.run()