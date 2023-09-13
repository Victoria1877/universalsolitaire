import arcade
import random

# Constants For Window Sizing
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Tux Solitaire"

# Card Backs
CARDBACK = "static/cards/cardBack.png"

# Constants for sizing of cards
CARD_SCALE = 2.4
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
CARD_VERTICAL_OFFSET = CARD_HEIGHT * (CARD_SCALE / 10) * 0.3

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

        # Sprite List for mats, all cards, held card and original location, dropped cards, and list of piles
        self.pmat_list = None
        self.card_list = None
        self.held_cards = None
        self.held_card_og_position = None
        self.piles = None
        
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

        # Shuffles the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(MAX_CARDS)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)

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
            primary_card = cards[-1]
            pile_index = self.cards_pile(primary_card)

            self.held_card = [primary_card]
            self.held_card_og_position = [self.held_card[0].position]
            self.pull_to_top(self.held_card[0])            

            card_index = self.piles[pile_index].index(primary_card)
            for i in range(card_index + 1, len(self.piles[pile_index])):
                card = self.piles[pile_index][i]
                self.held_card.append(card)
                self.held_card_og_position = [card.position]
                self.pull_to_top(card) 

    # Establishes the pile a card is in
    def cards_pile(self, card):
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
            
    # Removes the card from the pile list
    def rm_cards_pile(self, card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break
            

    # Moves the card to a new pile
    def change_cards_pile(self, card, pile_index):
        self.rm_cards_pile(card)                 
        self.piles[pile_index].append(card)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Ignore if no cards are held
        if len(self.held_card) == 0:
            return
    
        # Finds nearest pile and checks if they are touching
        pile, distance = arcade.get_closest_sprite(self.held_card[0], self.pmat_list)
        reset_position = True
    
        # Check for collision with a pile
        if arcade.check_for_collision(self.held_card[0], pile):
            pile_index = self.pmat_list.index(pile)
        
            # If it's the same pile as the original, do nothing
            if pile_index == self.cards_pile(self.held_card[0]):
                pass
        
            # Check for placement on bottom of stack
            elif STACK_PILE1 <= pile_index <= STACK_PILE7:
                bottom_position = pile.center_y - CARD_VERTICAL_OFFSET * len(self.piles[pile_index])
                for x, dropped_card in enumerate(self.held_card):
                    dropped_card.position = pile.center_x, bottom_position - CARD_VERTICAL_OFFSET * x
            
                # Move the card to the bottom of the pile
                for card in self.held_card:
                    self.change_cards_pile(card, pile_index)

                reset_position = False
        
            # For placing on win pile
            elif WIN_PILE_1 <= pile_index <= WIN_PILE_4:
                for x, dropped_card in enumerate(self.held_card):
                    dropped_card.position = pile.center_x, pile.center_y

                # Move the card to the bottom of the pile
                for card in self.held_card:
                    self.change_cards_pile(card, pile_index)

                reset_position = False

        # Releases the cards and returns to original location if invalid placement
        if reset_position:
            print(self.held_card_og_position)
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
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            print("Restarting... ")
            self.setup()
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            print("Returning Cards... ")
            for pile_index, card in enumerate(self.held_card):
                card.position = self.held_card_og_position[pile_index]

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