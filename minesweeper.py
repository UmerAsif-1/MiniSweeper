import random
from datetime import datetime
from sweeperlib import (
    load_sprites,
    create_window,
    set_draw_handler,
    set_mouse_handler,
    start,
    clear_window,
    draw_background,
    begin_sprite_draw,
    prepare_sprite,
    draw_sprites,
)
class MinesweeperGame:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0] * width for _ in range(height)]
        self.revealed = [[False] * width for _ in range(height)]
        self.mines = set()
        self.start_time = None
        self.end_time = None
        self.turns = 0
        self.outcome = None

    def place_mines(self, first_click_x, first_click_y):
        """Place mines on the board"""
        possible_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        possible_positions.remove((first_click_x, first_click_y))
        self.mines = set(random.sample(possible_positions, self.num_mines))

        for mine_x, mine_y in self.mines:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    new_x, new_y = mine_x + dx, mine_y + dy
                    if 0 <= new_x < self.width and 0 <= new_y < self.height:
                        self.board[new_y][new_x] += 1

    def reveal_tile(self, x, y):
        """Reveal a tile on the board"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            print("Coordinates are outside the board. Please try again.")
            return

        if self.revealed[y][x]:
            print("This tile is already revealed. Please try again.")
            return

        self.revealed[y][x] = True
        self.turns += 1

        if (x, y) in self.mines:
            self.end_game("lose")
        elif self.board[y][x] == 0:
            for dx_1 in range(-1, 2):
                for dy_1 in range(-1, 2):
                    new_x, new_y = x + dx_1, y + dy_1
                    if 0 <= new_x < self.width and 0 <= new_y < self.height:
                        self.reveal_tile(new_x, new_y)

        if all(self.revealed[i][j] or (i, j) in self.mines for i in range(self.height) for j in range(self.width)):
            self.end_game("win")

    def end_game(self, result):
        """End the game with the specified result"""
        self.end_time = datetime.now()
        self.outcome = result

    def display_board(self):
        """Display the current state of the game board"""
        for y in range(self.height):
            for x in range(self.width):
                if self.revealed[y][x]:
                    if (x, y) in self.mines:
                        sprite_key = "x"
                    else:
                        sprite_key = str(self.board[y][x])
                else:
                    sprite_key = " "
                prepare_sprite(sprite_key, x * 40, y * 40)

    def display_statistics(self):
        """Display Statistics"""
        print("\nGame Statistics:")
        print(f"Start Time: {self.start_time}")
        print(f"End Time: {self.end_time}")
        print(f"Duration: {self.end_time - self.start_time}")
        print(f"Turns: {self.turns}")
        print(f"Outcome: {self.outcome}")
        print()

def draw():
    """Draw"""
    clear_window()
    draw_background()
    begin_sprite_draw()
    game.display_board()
    draw_sprites()

def mouse_handler(x, y, button, modifiers):
    """Handle mouse clicks here"""
    game.reveal_tile(x // 40, y // 40)
    game.display_board()

    if game.outcome is not None:
        exit_game()

def exit_game():
    """Exit the game"""
    print("Game over! You", game.outcome)
    game.display_statistics()

    while True:
        print("\nMain Menu:")
        print("1. Start a New Game")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            width, height, num_mines = 8, 8, 10  
            game.__init__(width, height, num_mines)
            game.start_time = datetime.now()
            first_click_x, first_click_y = random.randint(0, width - 1), random.randint(0, height - 1)
            game.place_mines(first_click_x, first_click_y)
            game.display_board()
            start()
            break
        elif choice == "2":
            print("Quitting the game.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    load_sprites("sprites")
    create_window()

    game = MinesweeperGame(width=8, height=8, num_mines=10)

    set_draw_handler(draw)
    set_mouse_handler(mouse_handler)

    game.start_time = datetime.now()
    first_click_x_1, first_click_y_1 = random.randint(0, game.width - 1), random.randint(0, game.height - 1)
    game.place_mines(first_click_x_1, first_click_y_1)
    game.display_board()
    start()
