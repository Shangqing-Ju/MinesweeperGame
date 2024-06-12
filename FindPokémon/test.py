import tkinter as tk
import random

TASK_ONE = 1
TASK_TWO = 2
SQUARE_LENGTH = 50

TALL_GRASS = "#"
SHORT_GRASS = "~"
ATTEMPTED_CATCH = "@"
EXPOSED_POKEMON = "*"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")


class BoardModel:  # data
    def __init__(self, grid_size, num_pokemon):
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._board_game = TALL_GRASS * self._grid_size * self._grid_size
        self._pokemon_locations = self.generate_pokemons()

    def get_game(self):
        return self._board_game

    def generate_pokemons(self):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            num_pokemon (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = self._grid_size ** 2
        pokemon_locations = ()

        for _ in range(self._num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)

            pokemon_locations += (index,)
            self._pokemon_locations = pokemon_locations
        return self._pokemon_locations

    def get_pokemon_location(self):
        return self._pokemon_locations

    def replace_character_at_index(self, game, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        self._board_game = game[:index] + character + game[index + 1:]
        return self._board_game
    # def get_pokemon_locations(self):

    def index_in_direction(self, index, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
          | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.\
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate

        col = index % self._grid_size
        row = index // self._grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self._grid_size and 0 <= row < self._grid_size):
            return None
        return self._board_view.get_position_to_index((row, col), self._grid_size)

    def neighbour_directions(self, index):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, direction)
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    def number_at_cell(self, pokemon_locations, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self.get_game()[index] != TALL_GRASS:
            return int(self.get_game()[index])

        number = 0
        for neighbour in self.neighbour_directions(index):
            if neighbour in pokemon_locations:
                number += 1
        return number

    def get_number_at_cell(self):
        return self.number_at_cell

class PokemonGame:  # controller
    def __init__(self, master, grid_size=10, num_pokemon=15, task=TASK_ONE):
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._board_model = None
        self._board_view = None
        self.draw()

    def draw(self):
        game_label = tk.Label(bg="pink", text="Pokemon: Got 2 Find Them All!", height=1)
        game_label.pack(fill=tk.X)

        self._board_model = BoardModel(10, 10)
        self._board_view = BoardView(self._master, self._grid_size, self._grid_size*SQUARE_LENGTH)
        self._board_view.pack()
        self._board_view.draw_board(self._board_model)


class BoardView(tk.Canvas):  # gui
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._board_model = None
        self.config(height=self._board_width, width=self._board_width)

    def draw_board(self, board: BoardModel):
        self._board_model = board
        self.delete("all")
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                character = self._board_model.get_game()[self.position_to_index((col, row), self._grid_size)]
                x1 = row * SQUARE_LENGTH
                y1 = col * SQUARE_LENGTH
                if character == TALL_GRASS:
                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="dark green")
                elif character == ATTEMPTED_CATCH:
                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="yellow")
                elif character == SHORT_GRASS:

                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="green")
                    self.create_text(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, text=str(self._board_model.get_number_at_cell()))
                self.bind("<Button-1>", lambda e: self._left_click((e.x, e.y)))
                self.bind("<Button-2>", lambda e: self._right_click((e.x, e.y)))
                self.bind("<Button-3>", lambda e: self._right_click((e.x, e.y)))

    def _left_click(self, position):
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        # self._board_model.get_game()  # game string
        index = self.position_to_index((y, x), self._grid_size)  # index of game string
        print(index)
        if self._board_model.get_game()[index] == TALL_GRASS:
            self._board_model.replace_character_at_index(self._board_model.get_game(), index, SHORT_GRASS)
            self.draw_board(self._board_model)

        if index in self._board_model.get_pokemon_location():
            for index in self._board_model.get_pokemon_location():
                self._board_model.replace_character_at_index(self._board_model.get_game(), index, ATTEMPTED_CATCH)
                self.draw_board(self._board_model)
        print(self._board_model.get_pokemon_location())
        print(self._board_model.get_game())
        # elif character == EXPOSED_POKEMON

    def _right_click(self, position):
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        x1 = x * SQUARE_LENGTH
        y1 = y * SQUARE_LENGTH
        self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="red")

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * grid_size + y

    def get_position_to_index(self, position, grid_size):
        return self.position_to_index


def get_image(image_name):
    """(tk.PhotoImage) Get a image file based on capability.

    If a .png doesn't work, default to the .gif image.
    """
    try:
        image = tk.PhotoImage(file=image_name + ".png")
    except tk.TclError:
        image = tk.PhotoImage(file=image_name + ".gif")
    return image


def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 find them all!")

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()