import arcade

# Constants for sizing of cards
CARD_SCALE = 0.6
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
SCREEN_TITLE = "Kali Solitaire"
# Card backend
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Class for the main Program
class kalisol(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Sets up game, Call to restart
    def setup(self):
        pass

    # Renders Screen
    def on_draw(self):
        self.clear
    
    # X and Y coords of mouse clicks with key modifiers
    def on_mouse_press(self):
        pass

    # When user clicks to release
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    # When user moves the mouse
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

# Card Sprite Class
class card(arcade.Sprite):
    # Card Constructor
    def __init__(self, suit, value, scale=1):
        # Attributes for the suitand value
        self.suit = suit
        self.value = value

        # Image for sprite faceup
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        # Calls parent class properties
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

# The main program
def main():
    window = kalisol()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()