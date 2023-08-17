import arcade

# Constants for sizing of cards
CARD_SCALE = 1.0
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# Constants for Sizing of mats for cards to be placed
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Constants For Window Sizing
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Tux Solitaire"

# Card backend
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Connection to Spritesheet
#card_sprite_sheet = arcade.load_spritesheet("/static/cardspritesheet.png", rows=4, cols=13)


# Class for the main Program
class kalisol(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.border_width = 5

        # Sprite list with all cards
        self.card_list = None
        # Sets variables of held cards and their original location to nothing and establishes
        self.held_cards = None
        self.held_cards_og_position = None
        
    # Sets up game, Call to restart
    def setup(self):
        self.card_list = arcade.SpriteList()

        # Sets variables of held cards and their original location to null
        self.held_cards = []
        self.held_cards_og_position = []

        # Create Each Card
        #for card_suit in CARD_SUITS:
         #   for card_value in CARD_VALUES:
          #      card = Card(card_suit, card_value, CARD_SCALE)
           #     card.position = START_X, BOTTOM_Y
            #    self.card_list.append(card)
        card_sprite_sheet = arcade.load_spritesheet("/static/cardlist.png", rows=1, cols=13)
        for suit_index, suit in enumerate(CARD_SUITS):
            for value_index, value in enumerate(CARD_VALUES):
                card_sprite = card_sprite_sheet[suit_index][value_index]
                card = Card(suit, value, card_sprite)
                self.card_list.append(card)

    def pull_to_top(self, card: arcade.Sprite):
        # Puts card on top of rendering order (appears last -> on top of other objects)
        self.card_list.remove(card)
        self.card_list.append(card)

    # Renders Screen
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.set_background_color(arcade.color.DARK_GREEN)

        # Draw a border around the window (X, Y, Width, Height, Colour, Width)
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            self.width - self.border_width,
            self.height - self.border_width,
            arcade.color.GOLDEN_BROWN,  # Border color
            border_width=self.border_width  # Border width
        )

        # Draw the Cards
        self.card_list.draw()

    def on_resize(self, width: float, height: float):
        self.border_width = min(width, height) * 0.02
        super().on_resize(width, height)

    # X and Y coords of mouse clicks with key modifiers
    def on_mouse_press(self, x, y, button, key_modifiers):
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        if len(cards) > 0:
            # takes the top card, saves position, and Pulls to top
            primary_card = cards[-1]
            self.held_cards = [primary_card]
            self.held_cards_original_position = [self.held_cards[0].position]
            self.pull_to_top(self.held_cards[0])


    # When user clicks to release
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # ignores if no cards held
        if len(self.held_cards) == 0:
            return

        # Sets held cards to null
        self.held_cards = []

    # When user moves the mouse
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # move held cards with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

# Card Sprite Class
class Card(arcade.Sprite):

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"static/cards/card{self.suit}{self.value}.png"

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

# The main program
def main():
    window = kalisol()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()