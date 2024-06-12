import tkinter as tk
import random
from random import choice
from tkinter import messagebox
from tkinter import simpledialog
import time

TASK_ONE = 1
TASK_TWO = 2
SQUARE_LENGTH = 60

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
        self._board_view = None
        self._pokemon_locations = self.generate_pokemons()
        self._pokeball = num_pokemon

    def get_grid_size(self):
        return self._grid_size

    def reset_label(self):
        self.generate_pokemons()

    def reset_game(self):
        self._board_game = TALL_GRASS * self._grid_size * self._grid_size

    def reset_pokeball_num(self):
        self._pokeball = self._num_pokemon

    def get_game(self):
        return self._board_game

    def change_pokeball_num(self, count):
        self._pokeball += count

    def get_pokeball_num(self):
        return self._pokeball

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


class StatusBar(tk.Frame):
    def __init__(self, master, num_pokemon):
        super().__init__(master)
        self.frame1 = tk.Frame(master, bg="white")
        self.frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        pokeball_image = get_image("./images/full_pokeball")
        self._pokeball_label3 = tk.Label(self.frame1, image=pokeball_image, bg="white")
        self._pokeball_label3.pokeball_image = pokeball_image
        self._pokeball_label3.pack(side=tk.LEFT, padx=55, anchor=tk.N)
        self._pokeball_label2 = tk.Label(self.frame1, text=f"{5 - num_pokemon} attemped catches", bg="white")
        self._pokeball_label2.pack(side=tk.TOP, anchor=tk.NW)
        self._pokeball_label1 = tk.Label(self.frame1, text=f"{num_pokemon} pokeballs left", bg="white")
        self._pokeball_label1.pack(side=tk.TOP, anchor=tk.SW)

        # pokeball_image = get_image("./images/unrevealed")
        # self._pokeball_label3(image=pokeball_image)

        self.frame2 = tk.Frame(master, bg="white")
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH)
        self._start_time = time.time()
        time_image = get_image("./images/clock")
        self._time_label3 = tk.Label(self.frame2, image=time_image, bg="white")
        self._time_label3.pokeball_image = time_image
        self._time_label3.pack(side=tk.LEFT, padx=20, anchor=tk.N)
        self._time_label2 = tk.Label(self.frame2, text=f"Time elapsed", bg="white")
        self._time_label2.pack(side=tk.TOP, anchor=tk.N)
        self._time_label = tk.Label(self.frame2, text=f" 0 m 0 s", bg="white")
        self._time_label.pack(side=tk.TOP, anchor=tk.SW, padx=20)

        self.update_time()
        self._timer = None

        self.frame3 = tk.Frame(master, bg="white")
        self.frame3.pack(side=tk.LEFT, fill=tk.BOTH)
        self.button1 = tk.Button(self.frame3, text="New game", command=self.press1, bg="white")
        self.button1.pack(expand=1)
        self.button2 = tk.Button(self.frame3, text="Restart game", command=self.press2, bg="white")
        self.button2.pack()

        # photo = tk.PhotoImage(file="./images/full_pokeball")
        # self._image_label = tk.Label(master,image=photo)
        # self._image_label.pack(padx=50, anchor=tk.W)

    def press1(self):
        pass

    def press2(self):
        pass

    def reset_time(self):
        self._start_time = time.time()

    def update_pokeball_label(self, pokeball_num_left):
        self._pokeball_label2.config(text=f"{5 - pokeball_num_left} attemped catches")
        self._pokeball_label1.config(text=f"{pokeball_num_left} pokeballs left")

    def update_time(self):
        time_elapsed = int(time.time() - self._start_time)
        minute = time_elapsed // 60
        second = time_elapsed % 60
        self._time_label.config(text=f"{minute} m {second} s")
        self._timer = self.after(1000, self.update_time)

    def stop_time(self):
        self.after_cancel(self._timer)

    def get_save_time(self):
        time_elapsed = int(time.time() - self._start_time)
        minute = time_elapsed // 60
        second = time_elapsed % 60
        return f"{minute} m {second} s"

    # def create_layout(frame):
    #     img_gif = Tkinter.PhotoImage(file='img_gif.gif')
    #     label_img = Tkinter.Label(root, image=img_gif)
    #     label_img.pack()


class PokemonGame:  # controller
    def __init__(self, master, grid_size=10, num_pokemon=5, task=TASK_TWO):
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._board_model = None
        self._board_view = None
        self.draw()
        # frame1 = tk.Frame(master, bg="blue")
        # frame1.pack()
        # self.button1 = tk.Button(frame1, text="button1", bg="green")
        # self.button1.pack()
        self._menuBar = tk.Menu(self._master)
        self._master.config(menu=self._menuBar)
        self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
        self._menuBar.add_cascade(label="File", menu=self._fileMenu)
        self._fileMenu.add_command(label="Save Game", command=self.save_game)
        self._fileMenu.add_command(label="Load game", command=self.load_game)
        self._fileMenu.add_command(label="Restart game", command=self.restart_game)
        self._fileMenu.add_command(label="New game", command=self.new_game)
        self._fileMenu.add_command(label="Quit", command=self.quit)

    def save_game(self):
        data1 = "game:" + self._board_model.get_game() + "\n"
        data2 = "pokemon num:" + str(self._board_model.get_pokeball_num()) + "\n"
        data3 = "pokemon location:" + str(self._board_model.get_pokemon_location()) + "\n"
        data4 = "grid size:" + str(self._board_model.get_grid_size()) + "\n"
        data5 = "pokeball number:" + str(self._board_model.get_pokeball_num()) + "\n"
        data6 = "time:" + str(self._status.get_save_time())
        file_path = "game_info.txt"
        f = open(file_path, "w")
        f.write(data1)
        f.write(data2)
        f.write(data3)
        f.write(data4)
        f.write(data5)
        f.write(data6)
        f.close()

    def load_game(self, filename):
        pass
        # simpledialog.askstring("Input", "What level would you like to play?",
        #                                      parent=self._master)
        # # if self._level is not None:
        # #     self.reset_game()
        # # with open(filename, 'r') as file:
        # #     for line in file:
        # #         line = line.strip()
        # #         print(line)

    def restart_game(self):
        pass

    def new_game(self):
        pass

    def quit(self):
        ans = messagebox.askyesno("confirm quit", "Would you like to quit?")
        if ans:
            self._master.destroy()

    def draw(self):
        game_label = tk.Label(bg="pink", text="Pokemon: Got 2 Find Them All!", height=1)
        game_label.pack(fill=tk.X)

        self._board_model = BoardModel(self._grid_size, self._num_pokemon)
        if self._task == TASK_ONE:
            self._board_view = BoardView(self._master, self._grid_size, self._grid_size * SQUARE_LENGTH)
        elif self._task == TASK_TWO:
            self._board_view = ImageBoardView(self._master, self._grid_size, self._grid_size * SQUARE_LENGTH)
        self._board_view.pack()
        self._board_view.draw_board(self._board_model)
        self._status = StatusBar(self._master, self._num_pokemon)
        self._board_view.get_status_bar(self._status)

        # self._status.pack()


class BoardView(tk.Canvas):  # gui

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._board_model = None
        self.config(height=self._board_width, width=self._board_width)
        self._status = None
        self.img_ref = []

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
                elif character == EXPOSED_POKEMON:
                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="yellow")
                elif character == ATTEMPTED_CATCH:
                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="red")
                elif int(character) in range(9):
                    self.create_rectangle(x1, y1, x1 + SQUARE_LENGTH, y1 + SQUARE_LENGTH, fill="green")
                    self.create_text(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, text=character)

    def get_status_bar(self, status):
        self._status = status

    def bind_clicks(self):
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
            if index in self._board_model.get_pokemon_location():
                for index in self._board_model.get_pokemon_location():
                    self._board_model.replace_character_at_index(self._board_model.get_game(), index, EXPOSED_POKEMON)

                self.draw_board(self._board_model)
                self.check_game_over()
            else:
                number = self.number_at_cell(index)
                self._board_model.replace_character_at_index(self._board_model.get_game(), index, str(number))

                self.draw_board(self._board_model)
                self.check_game_over()
                if number == 0:
                    for index in self.big_fun_search(index):
                        if self._board_model.get_game()[index] != ATTEMPTED_CATCH:
                            self._board_model.replace_character_at_index(self._board_model.get_game(), index,
                                                                         str(self.number_at_cell(index)))
                    self.draw_board(self._board_model)

    def _right_click(self, position):
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        index = self.position_to_index((y, x), self._grid_size)
        if self._board_model.get_game()[index] == TALL_GRASS and self._board_model.get_pokeball_num() > 0:
            self._board_model.replace_character_at_index(self._board_model.get_game(), index, ATTEMPTED_CATCH)
            self._board_model.change_pokeball_num(-1)
            self._status.update_pokeball_label(self._board_model.get_pokeball_num())
            self.draw_board(self._board_model)
            self.check_game_over()
        elif self._board_model.get_game()[index] == ATTEMPTED_CATCH:
            self._board_model.replace_character_at_index(self._board_model.get_game(), index, TALL_GRASS)
            self._board_model.change_pokeball_num(+1)
            self._status.update_pokeball_label(self._board_model.get_pokeball_num())
            self.draw_board(self._board_model)
            self.check_game_over()

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

    def index_to_position(self, index):
        x, y = index // 10, index % 10
        return x, y

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
        return self.position_to_index((row, col), self._grid_size)

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

    def number_at_cell(self, index):
        """n returns the number of Pokemon in neighbouring cells.

        Parameters:
            game(str): game string
            pokemon_locations(int): index of pokemon locations.
            grid_size(int): size of game.
            index(int): the index to a cell.
        Returns:
            number_of_pokemons_surrounds(int): the number of pokemon surround target cell.
        """
        number_of_pokemons_surrounds = 0
        list_of_indexes = self.neighbour_directions(index)
        for x in list_of_indexes:
            if x in self._board_model.get_pokemon_location():
                number_of_pokemons_surrounds += 1
        number = number_of_pokemons_surrounds
        return number

    def get_number_at_cell(self):
        return self.number_at_cell

    def big_fun_search(self, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self._board_model.get_game()[index] == ATTEMPTED_CATCH:
            return queue

        number = self.number_at_cell(index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._board_model.get_game()[neighbour] != ATTEMPTED_CATCH:
                    number = self.number_at_cell(neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def check_win(self):
        """Checking if the player has won the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

        Returns:
            (bool): True if the player has won the game, false if not.

        """
        return TALL_GRASS not in self._board_model.get_game() and self._board_model.get_game().count(
            ATTEMPTED_CATCH) == len(self._board_model.get_pokemon_location())

    def check_lose(self):
        return EXPOSED_POKEMON in self._board_model.get_game()

    def check_game_over(self):
        """Check if the game is over and exit if so"""
        if self.check_win():
            self.random_pokemon_images()
            self._status.stop_time()
            messagebox.showinfo("You Win!", "You won! :D")
            self._master.destroy()
        if self.check_lose():
            ans = messagebox.askyesno("Game over", "Would you like to try again?")
            if ans:
                self.redraw()
            else:
                self._master.destroy()

    def redraw(self):
        """Redraw the whole game window."""
        self.draw_board(self._board_model)
        self._status.reset_time()
        self._board_model.reset_game()
        self.draw_board(self._board_model)
        self._status.update_pokeball_label(pokeball_num_left=len(self._board_model.get_pokemon_location()))
        self._board_model.reset_pokeball_num()

    def random_pokemon_images(self):
        pokemon_position = []
        for index in self._board_model.get_pokemon_location():
            self.index_to_position(index)
            pokemon_position.append(self.index_to_position(index))
        pokemon_list = ["charizard", "cyndaquil", "pikachu", "psyduck", "togepi", "umbreon"]
        for pokemon in pokemon_position:
            r = choice(pokemon_list)
            y, x = pokemon
            image = get_image(f"./images/pokemon_sprites/{r}")
            self.create_image(x * SQUARE_LENGTH + SQUARE_LENGTH / 2, y * SQUARE_LENGTH + SQUARE_LENGTH / 2,
                              image=image)
            self.img_ref.append(image)


class ImageBoardView(BoardView):
    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self.img_ref = []

    def draw_board(self, board: BoardModel):

        # pokemon_position = []

        image_num_list = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
        # pokemon_list = ["charizard", "cyndaquil", "pikachu", "psyduck", "togepi", "umbreon"]
        self.delete("all")
        self._board_model = board
        print(self._board_model.get_pokemon_location())
        # for index in self._board_model.get_pokemon_location():
        #     self.index_to_position(index)
        #     pokemon_position.append(self.index_to_position(index))

        for row in range(self._grid_size):
            for col in range(self._grid_size):
                character = self._board_model.get_game()[self.position_to_index((col, row), self._grid_size)]
                x1 = row * SQUARE_LENGTH
                y1 = col * SQUARE_LENGTH
                if character == TALL_GRASS:
                    image = get_image("./images/unrevealed")
                    self.create_image(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, image=image)
                    self.img_ref.append(image)
                elif character == EXPOSED_POKEMON:
                    self.random_pokemon_images()
                    # for pokemon in pokemon_position:
                    #     r = choice(pokemon_list)
                    #     y, x = pokemon
                    #     image = get_image(f"./images/pokemon_sprites/{r}")
                    #     self.create_image(x * SQUARE_LENGTH + SQUARE_LENGTH / 2, y * SQUARE_LENGTH + SQUARE_LENGTH / 2,
                    #                       image=image)
                    #     self.img_ref.append(image)
                elif character == ATTEMPTED_CATCH:
                    image = get_image("./images/pokeball")
                    self.create_image(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, image=image)
                    self.img_ref.append(image)
                elif int(character) == 0:
                    image = get_image("./images/zero_adjacent")
                    self.create_image(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, image=image)
                    self.img_ref.append(image)
                elif int(character) in range(1, 9):
                    image = get_image(f"images/{image_num_list[int(character)]}" + "_adjacent")
                    self.create_image(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, image=image)
                    self.img_ref.append(image)

                self.bind("<Button-1>", lambda e: self._left_click((e.x, e.y)))
                self.bind("<Button-2>", lambda e: self._right_click((e.x, e.y)))
                self.bind("<Button-3>", lambda e: self._right_click((e.x, e.y)))




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
