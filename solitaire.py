import arcade
import random

# Constants For Window Sizing
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Tux Solitaire"

# Constants for sizing of cards
CARD_SCALE = 2.5
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# Constants for Sizing of mats for cards to be placed
MAT_PERCENT_OVERSIZE = .35
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# Placement location of mats
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
MAT_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Constants for making stacks on mats
MAX_CARDS = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
STACK_PILE1 = 2
STACK_PILE2 = 3
STACK_PILE3 = 4
STACK_PILE4 = 5
STACK_PILE5 = 6
STACK_PILE6 = 7
STACK_PILE7 = 8
WIN_PILE_1 = 9
WIN_PILE_2 = 10
WIN_PILE_3 = 11
WIN_PILE_4 = 12

# Distance of cards in stack
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Constants for Locations
top_right_x = SCREEN_WIDTH - MAT_WIDTH / 2 - MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
top_right_y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card backend
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


# Class for the main Program
class kalisol(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.border_width = 5

        # Sprite List for mats
        self.pmat_list = None
        # Sprite list with all cards
        self.card_list = None
        # Sets variables of held card and original location to nothing and establishes
        self.held_cards = None
        self.held_card_og_position = None

        
    # Sets up game, Call to restart
    def setup(self):
        self.card_list = arcade.SpriteList()

        # Sets variables of held card and original location to null
        self.held_card = []
        self.held_card_og_position = []

        # Setup for card mats
        self.pmat_list = arcade.SpriteList()

        # Face Down mat
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, top_right_y
        self.pmat_list.append(pile)

        # Face Up mats
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + MAT_SPACING, top_right_y
        self.pmat_list.append(pile)

        # Shuffles the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Seven active play mats
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = top_right_x - i * MAT_SPACING, MIDDLE_Y
            self.pmat_list.append(pile)

        # Win criteria top mats
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = top_right_x - i * MAT_SPACING, TOP_Y
            self.pmat_list.append(pile)

        # Sprite lists all cards regardless of pile
        self.card_list = arcade.SpriteList()

        #   Create Each Card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, top_right_y
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

        # Draw the Mats
        self.pmat_list.draw()

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
            self.held_card = [primary_card]
            self.held_card_og_position = [self.held_card[0].position]
            self.pull_to_top(self.held_card[0])


    # When user clicks to release
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # ignores if no cards held
        if len(self.held_card) == 0:
            return
        
        # Finds nearest pile and checks to see if they are touching
        pile, distance = arcade.get_closest_sprite(self.held_card[0], self.pmat_list)
        reset_position = True
        if arcade.check_for_collision(self.held_card[0], pile):
            # Move each held card to the centre of the pile
            for x, dropped_card in enumerate(self.held_card):
                dropped_card.position = pile.center_x, pile.center_y

            reset_position = False

        # Releases the cards and returns to og location if invalid placement
        if reset_position:
            for pile_index, card in enumerate(self.held_card):
                card.position = self.held_card_og_position[pile_index]

        # Sets held card to null
        self.held_card = []

    # When user moves the mouse
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # move held card with the mouse
        for card in self.held_card:
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