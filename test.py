import arcade

CARD_WIDTH = 140
CARD_HEIGHT = 190
CARD_SCALE = 0.6

class Card(arcade.Sprite):
    def __init__(self, x, y, texture):
        super().__init__(texture, CARD_SCALE)
        self.center_x = x
        self.center_y = y

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Texture Management Example")
        self.card_list = None

    def setup(self):
        self.card_list = arcade.SpriteList()

        # Load the sprite sheet texture
        sprite_sheet_texture = arcade.load_texture("static/Cardlist.png")

        # Define the suit and index for the suit you want to create sprites for
        target_suit = "Diamonds"
        suit_index = 1  # Diamonds is usually the second suit in a standard deck

        for value_index, value in enumerate(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]):
            # Calculate the x-coordinate within the sprite sheet
            x_coord = CARD_WIDTH * value_index
            y_coord = CARD_HEIGHT * suit_index

            # Create a new image for the cropped texture
            cropped_texture = arcade.load_texture(CARD_WIDTH, CARD_HEIGHT)

            # Blit the cropped region onto the new image
            cropped_texture.blit(0, 0, CARD_WIDTH, CARD_HEIGHT, sprite_sheet_texture, x_coord, y_coord)

            card = Card(0, 0, cropped_texture)
            self.card_list.append(card)

    def on_draw(self):
        arcade.start_render()
        self.card_list.draw()

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
