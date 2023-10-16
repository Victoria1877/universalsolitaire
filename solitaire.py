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
MAT_HEIGHT = int((CARD_HEIGHT * MAT_PERCENT_OVERSIZE) * 3)
MAT_HEIGHTC = int(MAT_HEIGHT / 3)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# Placement location of mats
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHTC / 2 - MAT_HEIGHTC * VERTICAL_MARGIN_PERCENT - 5
MIDDLE_Y = (TOP_Y - MAT_HEIGHTC - MAT_HEIGHTC * VERTICAL_MARGIN_PERCENT) /1.5
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
top_right_y = SCREEN_HEIGHT - MAT_HEIGHTC / 2 - MAT_HEIGHTC * VERTICAL_MARGIN_PERCENT
BOTTOM_Y = MAT_HEIGHTC / 2 + MAT_HEIGHTC * VERTICAL_MARGIN_PERCENT - 5
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT + 5
PLAY_MAT_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT + 110

# Card backend
CARD_VALUES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
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
        self.visual_mat_list = None
        self.dmat_list = None
        
    # Sets up game, Call to restart
    def setup(self):
        self.card_list = arcade.SpriteList()

        # Sets variables of held card and original location to null
        self.held_card = []
        self.held_card_og_position = []

        # Setup for card mats
        self.pmat_list = arcade.SpriteList()
        self.visual_mat_list = arcade.SpriteList()
        self.dmat_list = arcade.SpriteList()

        #ACTUAL MAPS
            # Face Down mat
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_GREEN)
        pile.position = START_X, top_right_y
        self.pmat_list.append(pile)

            # Face Up mats
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_GREEN)
        pile.position = START_X + MAT_SPACING, top_right_y
        self.pmat_list.append(pile)

            # Seven active play mats
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.DARK_GREEN)
            pile.position = PLAY_MAT_X + i * MAT_SPACING -10, MIDDLE_Y + 170
            self.pmat_list.append(pile)

            # Win criteria top mats
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.color.DARK_GREEN)
            pile.position = top_right_x - i * MAT_SPACING - 10, TOP_Y
            self.pmat_list.append(pile)

        # VISUAL MATS 
        visual_mat_list = arcade.SpriteList()
        for i in range(7):
            visual_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_OLIVE_GREEN)
            visual_mat.position = PLAY_MAT_X + i * MAT_SPACING -10, MIDDLE_Y + 170
            self.visual_mat_list.append(visual_mat)
        for i in range(4):
            visual_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_OLIVE_GREEN)
            visual_mat.position = top_right_x - i * MAT_SPACING - 10, TOP_Y
            self.visual_mat_list.append(visual_mat)
        # Face Down mat
        visual_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_OLIVE_GREEN)
        visual_mat.position = START_X, top_right_y
        self.visual_mat_list.append(visual_mat)

        # Face Up mats
        visual_mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHTC, arcade.csscolor.DARK_OLIVE_GREEN)
        visual_mat.position = START_X + MAT_SPACING, top_right_y
        self.visual_mat_list.append(visual_mat)



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

        for pile_no in range(STACK_PILE1, STACK_PILE7 + 1):

            # Deal proper number of cards for that pile
            for j in range(pile_no - STACK_PILE1 + 1):
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # print("meow" + card.value + card.suit + " j " + str(j) + " pno " + str(pile_no))
                self.piles[pile_no].append(card)

                card.position = self.pmat_list[pile_no].position
                self.pull_to_top(card)

            # Flip up the top cards
        for i in range(STACK_PILE1, STACK_PILE7 + 1):
            self.piles[i][-1].face_up()

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
        self.visual_mat_list.draw()
        self.dmat_list.draw()

        # Draw the Cards
        self.card_list.draw()

    def on_resize(self, width: float, height: float):
        self.border_width = min(width, height) * 0.02
        super().on_resize(width, height)

    def on_mouse_press(self, x, y, button, key_modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        if len(cards) > 0:
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # what pile card is in
            pile_index = self.cards_pile(primary_card)

            if pile_index == BOTTOM_FACE_DOWN_PILE:
                for i in range(3):
                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    card = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    card.face_up()
                    card.position = self.pmat_list[BOTTOM_FACE_UP_PILE].position
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card)
                    self.piles[BOTTOM_FACE_UP_PILE].append(card)
                    self.pull_to_top(card)

            elif primary_card.is_face_down:
                primary_card.face_up()
            else:
                self.held_card = [primary_card]
                self.held_card_og_position = [self.held_card[0].position]
                self.pull_to_top(self.held_card[0])

                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_card.append(card)
                    self.held_card_og_position.append(card.position)
                    self.pull_to_top(card)

        else:
            mats = arcade.get_sprites_at_point((x, y), self.pmat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pmat_list.index(mat)

                # Is it turned over draw pile
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Flip the deck back over
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
                        card.position = self.pmat_list[BOTTOM_FACE_DOWN_PILE].position


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
        current_pile = self.cards_pile(card)
        if current_pile is not None:
            self.rm_cards_pile(card)                 
            self.piles[pile_index].append(card)


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # If we don't have any cards, who cares
        if len(self.held_card) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_card[0], self.pmat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_card[0], pile):

            # What pile is it?
            pile_index = self.pmat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.cards_pile(self.held_card[0]):
                    pass

            # Is it on a middle play pile?
            elif STACK_PILE1 <= pile_index <= STACK_PILE7:

                topCard = self.held_card[0]
                topCardValue = int(topCard.value)
                topCardSuit = topCard.suit

                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    top_card_value = int(top_card.value)
                    top_card_suit = str(top_card.suit)

                    if top_card_value == topCardValue + 1:
                        if (top_card_suit == "Hearts" or top_card_suit == "Diamonds") and (topCardSuit == "Clubs" or topCardSuit == "Spades"):
                            for i, dropped_card in enumerate(self.held_card):
                                dropped_card.position = top_card.center_x, top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                            for card in self.held_card:
                                self.change_cards_pile(card, pile_index)
                            reset_position = False
                        elif (topCardSuit == "Hearts" or topCardSuit == "Diamonds") and (top_card_suit == "Clubs" or top_card_suit == "Spades"):
                            for i, dropped_card in enumerate(self.held_card):
                                dropped_card.position = top_card.center_x, top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                            for card in self.held_card:
                                self.change_cards_pile(card, pile_index)
                            reset_position = False
                        else:
                            pass
                    else:
                        pass

                else:
                    # Are there no cards in the middle play pile?
                    if topCardValue == 13:
                        for i, dropped_card in enumerate(self.held_card):
                            dropped_card.position = pile.center_x, pile.center_y - CARD_VERTICAL_OFFSET * i
                        for card in self.held_card:
                            self.change_cards_pile(card, pile_index)
                        reset_position = False

            # Release on top play pile? And only one card held?
            elif WIN_PILE_1 <= pile_index <= WIN_PILE_4 and len(self.held_card) == 1:
                topCard = self.held_card[0]
                topCardValue = int(topCard.value)
                topCardSuit = topCard.suit
                print(topCardValue)
                if len(self.piles[pile_index]) > 0:

                    wPileCard = self.piles[pile_index][-1]
                    wPileCardValue = int(wPileCard.value)
                    wPileCardSuit = wPileCard.suit
                    print(wPileCard.value)

                    if topCardValue == wPileCardValue + 1:
                        if topCardSuit == wPileCardSuit:
                            # Move position of card to pile
                            self.held_card[0].position = pile.position
                            # Move card to card list
                            for card in self.held_card:
                                self.change_cards_pile(card, pile_index)
                            reset_position = False
                        else:
                            pass
                    else:
                        pass
                else:
                    if topCardValue==1:
                        self.held_card[0].position = pile.position
                        for card in self.held_card:
                            self.change_cards_pile(card, pile_index)
                        reset_position = False
                    else:
                        pass

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_card):
                card.position = self.held_card_og_position[pile_index]

        # We are no longer holding cards
        self.held_card = []

        excluded_piles = [0, 1, 9, 10, 11, 12]
        for mat_index, pile in enumerate(self.pmat_list):
            if mat_index not in excluded_piles and self.piles[mat_index] and self.piles[mat_index][-1].is_face_down:
                if self.piles[mat_index] and self.piles[mat_index][-1].is_face_down:
                    self.piles[mat_index][-1].face_up()
        else:
            pass

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
        if symbol == arcade.key.ESCAPE:
            print("Returning Cards for Debug... ")
            for pile_index, card in enumerate(self.held_card):
                card.position = 100, 100, 100
                self.held_card = []
                self.held_card_og_position = []
                self.rm_cards_pile(card)                 

# Card Sprite Class
class Card(arcade.Sprite):

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"static/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False

        # Call the parent
        super().__init__(CARDBACK, scale, hit_box_algorithm="None")

    def face_down(self):
        self.texture = arcade.load_texture(CARDBACK)
        self.is_face_up = False
    
    def face_up(self):
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        return not self.is_face_up

# The main program
def main():
    window = kalisol()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()