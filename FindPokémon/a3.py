import tkinter as tk
import random
from random import choice
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.font as tkfont
import os
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


class BoardModel:
    """
    board model, manages the data and defines rules and behaviors.
    """

    def __init__(self, grid_size, num_pokemon):
        """
        Construct a board with the given grid size and pokemon number.
        Parameters:
            grid_size (int): The size of the grid.
            num_pokemon (int): The number of pokemon.
        """
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._board_game = TALL_GRASS * self._grid_size * self._grid_size
        self._board_view = None
        self._pokemon_locations = self.generate_pokemons()
        self._pokeball = num_pokemon

    def get_grid_size(self):
        """(int): Returns the size of the grid."""
        return self._grid_size

    def reset_game(self):
        """Reset the game board."""
        self._board_game = TALL_GRASS * self._grid_size * self._grid_size

    def reset_pokeball_num(self):
        """Reset the pokeball number to equal to the pokemon number."""
        self._pokeball = self._num_pokemon

    def get_game(self):
        """(str)Return the game strung"""
        return self._board_game

    def change_pokeball_num(self, count):
        """Change the number of pokeball."""
        self._pokeball += count

    def get_pokeball_num(self):
        """(int)Return the number of pokeball."""
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
        cell_count = self._grid_size ** 2  # The number of cells.
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
        """(tuple)Return the pokemon locations."""
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
    """a frame of a status bar. """

    def __init__(self, master, num_pokemon, task=TASK_TWO):
        """
        Construct a frame in the task2 with the given grid size and pokemon number.
        Parameters:
            task (int): The task.
            num_pokemon (int): The number of pokemon.
        """
        super().__init__(master)
        self._task = task
        self._num_pokemon = num_pokemon

        if task == TASK_TWO:
            self.frame1 = tk.Frame(master, bg="white")
            self.frame1.pack(side=tk.LEFT, fill=tk.BOTH)
            self.frame4 = tk.Frame(self.frame1, bg="white")
            self.frame4.pack(side=tk.LEFT, padx=60)

            pokeball_image = get_image("./images/full_pokeball")
            self._pokeball_label3 = tk.Label(self.frame4, image=pokeball_image, bg="white")
            self._pokeball_label3.pokeball_image = pokeball_image
            self._pokeball_label3.pack(side=tk.LEFT, anchor=tk.N)
            self._pokeball_label2 = tk.Label(self.frame4, text=f"{num_pokemon - num_pokemon} attempted catches", bg="white")
            self._pokeball_label2.pack(side=tk.TOP, anchor=tk.NW)
            self._pokeball_label1 = tk.Label(self.frame4, text=f"{self._num_pokemon} pokeballs left", bg="white")
            self._pokeball_label1.pack(side=tk.TOP, anchor=tk.SW)


            self.frame2 = tk.Frame(master, bg="white")
            self.frame2.pack(side=tk.LEFT, fill=tk.BOTH)
            self._start_time = time.time()
            time_image = get_image("./images/clock")
            self._time_label3 = tk.Label(self.frame2, image=time_image, bg="white")
            self._time_label3.pokeball_image = time_image
            self._time_label3.pack(side=tk.LEFT, anchor=tk.NW)
            self._time_label2 = tk.Label(self.frame2, text=f"Time elapsed", bg="white")
            self._time_label2.pack(side=tk.TOP, anchor=tk.NW)
            self._time_label = tk.Label(self.frame2, text=f"{self.reset_time}", bg="white")

            self._time_label.pack(side=tk.TOP, anchor=tk.SW)

            self.update_time()
            self._timer = None

            self.frame3 = tk.Frame(master, bg="white")
            self.frame3.pack(side=tk.LEFT, fill=tk.BOTH)
            self.button1 = tk.Button(self.frame3, text="New game", command=self.new_game, bg="white")
            self.button1.pack(padx=30)
            self.button2 = tk.Button(self.frame3, text="Restart game", command=self.restart, bg="white")
            self.button2.pack(padx=30)

    def new_game(self):
        """Starting a new game with the game board same as the very beginning"""
        self._pokemon_game.new_game()

    def get_pokemon_game(self, pokemon_game):
        """Get the functions from the controller so that the new game and restart buttons do work """
        self._pokemon_game = pokemon_game

    def restart(self):
        """Redraw the whole game window."""
        self._pokemon_game.restart_game()

    def reset_time(self):
        """Reset the time of user uesed to be zero."""
        self._start_time = time.time()

    def update_pokeball_label(self, pokeball_num_left):
        """Update the pokeball number on the statues bar."""
        self._pokeball_label2.config(text=f"{self._num_pokemon - pokeball_num_left} attemped catches")
        self._pokeball_label1.config(text=f"{pokeball_num_left} pokeballs left")

    def time_elapsed(self):
        """(float)Return the current time of user used."""
        time_elapsed = time.time() - self._start_time
        return time_elapsed

    def update_time(self):
        """Update the time of user used per second."""
        minute = int(self.time_elapsed() // 60)
        second = int(self.time_elapsed() % 60)
        self._time_label.config(text=f"{minute} m {second} s")
        self._timer = self.after(1000, self.update_time)

    def stop_time(self):
        """Stop the time of user used."""
        self.after_cancel(self._timer)

    def get_saved_time(self):
        """(str)Return the saved time of user used ."""
        time_elapsed = self.time_elapsed() - 1.2  # remove the delay of start timing
        minute = int(time_elapsed) // 60
        second = int(time_elapsed) % 60
        return f"{minute} m {second} s"


class PokemonGame:
    """Game controller that manages communication between the board view and game model."""

    def __init__(self, master, grid_size=10, num_pokemon=15, task=TASK_TWO):
        """Create a pokemon game within a master
        Parameters:
            master (tk.Tk: Widget within which the board is placed.
            grid_size (int): The initially size of grid.
            num_pokemon (int): The initially number of pokemon.
            task (int): Set which task to present.
        """
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._board_model = None
        self._board_view = None
        self.draw()
        if self._task == TASK_TWO:
            self._menuBar = tk.Menu(self._master)
            self._master.config(menu=self._menuBar)
            self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
            self._menuBar.add_cascade(label="File", menu=self._fileMenu)
            self._fileMenu.add_command(label="Save Game", command=self.save_game)
            self._fileMenu.add_command(label="Load game", command=self.load_game)
            self._fileMenu.add_command(label="Restart game", command=self.restart_game)
            self._fileMenu.add_command(label="New game", command=self.new_game)
            self._fileMenu.add_command(label="Quit", command=self.quit)
            self._fileMenu.add_command(label="High score", command=self.high_score_board)

    def done(self):  # the done button on toplevel to close the toplevel window
        """Close the toplevel window"""
        self.quit.destroy()

    def high_score_board(self):
        """Create a high score board to show the top three users and their score"""
        self.quit = tk.Toplevel()
        frame1 = tk.Frame(self.quit)
        frame1.pack(fill=tk.BOTH)
        frame2 = tk.Label(frame1, text="High Score", fg="white", bg="pink")
        frame2.pack(fill=tk.BOTH)
        frame3 = tk.Label(self.quit, bg="white")
        frame3.pack(fill=tk.BOTH)
        button1 = tk.Button(frame3, text="done", command=self.done, bg="white")
        button1.pack()

        # Properly present the high score board while the number of the high score record is less than 3
        if len(self._board_view.load_top_three()) > 0:
            label2 = tk.Label(frame1,
                              text=f"{self._board_view.get_top_score()[0][0]}: {self._board_view.load_top_three()[0][1]} ",
                              bg="white")
            label2.pack(fill=tk.BOTH)
            if len(self._board_view.load_top_three()) > 1:
                label3 = tk.Label(frame1,
                                  text=f"{self._board_view.get_top_score()[1][0]}: {self._board_view.load_top_three()[1][1]} ",
                                  bg="white")
                label3.pack(fill=tk.BOTH)
                if len(self._board_view.load_top_three()) > 2:
                    label4 = tk.Label(frame1,
                                      text=f"{self._board_view.get_top_score()[2][0]}: {self._board_view.load_top_three()[2][1]} ",
                                      bg="white")
                    label4.pack(fill=tk.BOTH)

    def save_game(self):
        """Store all of the necessary current information of the game"""
        save_location = simpledialog.askstring("Save game", "please input a name?", parent=self._master)
        game_string = "game:" + self._board_model.get_game() + "\n"
        pokemon_num = "pokemon num:" + str(self._num_pokemon) + "\n"
        pokemon_location = "pokemon location:" + str(self._board_model.get_pokemon_location()) + "\n"
        grid_size = "grid size:" + str(self._board_model.get_grid_size()) + "\n"
        pokeball_left = "pokeball left:" + str(self._board_model.get_pokeball_num()) + "\n"
        time_used = "time:" + str(self._status.get_saved_time())
        file_path = f"{save_location}.txt"
        f = open(file_path, "w")
        f.write(game_string)
        f.write(pokemon_num)
        f.write(pokemon_location)
        f.write(grid_size)
        f.write(pokeball_left)
        f.write(time_used)
        f.close()

    def load_game(self):
        """Load all of the saved information of the game"""
        filename = simpledialog.askstring("load", "which level would u like to load?", parent=self._master)
        if not os.path.isfile(f"{filename}.txt"):
            ans = messagebox.showinfo("Invalid path", "Invalid path")
            if ans:
                filename = simpledialog.askstring("load", "which level would u like to load?", parent=self._master)
        with open(f"{filename}.txt", 'r') as file:
            game_list = []
            for line in file:
                line = line.strip()
                line_list = line.split(':')
                game_list.append(line_list)
            self._board_model._board_game = game_list[0][1]
            time_string = game_list[5][1]
            self._status._time_label.config(text=f"{time_string[0]} m {time_string[4]} s")

            self._status.update_pokeball_label(pokeball_num_left=int(game_list[4][1]))
            self._board_model.reset_pokeball_num()

            self._board_view.draw_board(self._board_model)

    def restart_game(self):
        """Restart the current game, including game timer. Pokemon locations
        should persist."""
        self._board_view.redraw()

    def new_game(self):
        """Restart to a new game (i.e. new pokemon locations). Use the same
        grid size and number of pokemon as the current game.
        """
        self._board_model.generate_pokemons()
        self._status.reset_time()
        self._board_view.redraw()

    def quit(self):
        """Prompt the player via messagebox to ask whether they are sure
        they would like to quit.If no, do nothing. If yes, window should close and program should terminate"""
        ans = messagebox.askyesno("confirm quit", "Would you like to quit?")
        if ans:
            self._master.destroy()

    def draw(self):
        """ Divide the game to task1 and task2, manage which task the user want to play """
        ft = tkfont.Font(family='Fixdsys', size=22, weight=tkfont.BOLD)
        game_label = tk.Label(bg="pink", fg="white", text="Pokemon: Got 2 Find Them All!", font=ft, height=1)
        game_label.pack(fill=tk.X)

        self._board_model = BoardModel(self._grid_size, self._num_pokemon)
        if self._task == TASK_ONE:
            self._board_view = BoardView(self._master, self._grid_size, self._grid_size * SQUARE_LENGTH)
        elif self._task == TASK_TWO:
            self._board_view = ImageBoardView(self._master, self._grid_size, self._grid_size * SQUARE_LENGTH)
        self._board_view.pack()
        self._board_view.draw_board(self._board_model)
        if self._task == TASK_TWO:
            self._status = StatusBar(self._master, self._num_pokemon)
            self._status.get_pokemon_game(self)
            self._board_view.get_status_bar(self._status)


def position_to_index(position, grid_size):
    """Convert the row, column coordinate in the grid to the game strings index.

    Parameters:
        position (tuple<int, int>): The row, column position of a cell.
        grid_size (int): The grid size of the game.

    Returns:
        (int): The index of the cell in the game string.
    """
    x, y = position
    return x * grid_size + y


def index_to_position(index):
    """Convert the the game strings index to row, column coordinate in the grid.

    Parameters:
        index (int): The index of the game string.

    Returns:
        (<tuple>): The position of the index in the game board.
    """
    x, y = index // 10, index % 10
    return x, y


class BoardView(tk.Canvas):
    """View of the pokemon game board"""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """Construct a board view using the grid size and board width .

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (int): The size of the grid.
            board_width (callable): The width of the board.
        """
        super().__init__(master, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._board_model = None
        self.config(height=self._board_width, width=self._board_width)
        self._status = None
        self._initial_box = None
        self.img_ref = []

    def draw_board(self, board: BoardModel):
        """Present the board of the game
        Parameters:
            board: BoardModel.
        """
        self._board_model = board
        self.delete("all")
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                character = self._board_model.get_game()[position_to_index((col, row), self._grid_size)]
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
        self.bind_clicks()

    def get_status_bar(self, status):
        """Get the data of the status bar
        Parameters:
            status:The data of the status bar.
        """
        self._status = status

    def bind_clicks(self):
        """Bind clicks on a label to the left and right click handlers.
        """
        self.bind("<Button-1>", lambda e: self._left_click((e.x, e.y)))
        self.bind("<Button-2>", lambda e: self._right_click((e.x, e.y)))
        self.bind("<Button-3>", lambda e: self._right_click((e.x, e.y)))

        self.bind("<Motion>", lambda e: self._highlight((e.x, e.y)))

    def _highlight(self, position):
        """Motion onto a grid square will cause a border to appear around the square that the cursor is on. Motion off
        a grid square will cause this border to disappear
        """
        new_box = self.get_bbox(position)
        if new_box != self._initial_box:
            if self._initial_box is not None:
                self.create_rectangle(self._initial_box, outline=None)
            self._initial_box = new_box
        self.create_rectangle(new_box, outline="red")

    def get_bbox(self, position):
        """While motion onto a grid square return the position of the motion
        Parameters:
            position(<tuple>):The position of the motion.
        Return(<tuple<tuples>>): A tuple of motion position tuples.
        """
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        x1 = x * SQUARE_LENGTH
        y1 = y * SQUARE_LENGTH
        x2 = x1 + SQUARE_LENGTH
        y2 = y1 + SQUARE_LENGTH
        return x1, y1, x2, y2

    def _left_click(self, position):
        """Handle left clicking on a cell. Calls the draw board method to present the new game board.
        """
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        index = position_to_index((y, x), self._grid_size)  # index of game string
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
        """Handle right clicking on a cell"""
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        index = position_to_index((y, x), self._grid_size)
        if self._board_model.get_game()[index] == TALL_GRASS and self._board_model.get_pokeball_num() > 0:
            self._board_model.replace_character_at_index(self._board_model.get_game(), index, ATTEMPTED_CATCH)
            self.draw_board(self._board_model)
            self.check_game_over()
        elif self._board_model.get_game()[index] == ATTEMPTED_CATCH:
            self._board_model.replace_character_at_index(self._board_model.get_game(), index, TALL_GRASS)
            self.draw_board(self._board_model)
            self.check_game_over()

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
        return position_to_index((row, col), self._grid_size)

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
        """ Returns the number of Pokemon in neighbouring cells.

        Parameters:
            index(int): the index to a cell.
        Returns:
            number_of_pokemons_surrounds(int): the number of pokemon surround target cell.
        """
        number_of_pokemons_surrounds = 0
        list_of_indexes = self.neighbour_directions(index)
        for x in list_of_indexes:
            if x in self._board_model.get_pokemon_location():
                number_of_pokemons_surrounds += 1
        return number_of_pokemons_surrounds

    def get_number_at_cell(self):
        """ Returns the number of Pokemon in neighbouring cells."""
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

        Returns:
            (bool): True if the player has won the game, false if not.
        """
        return TALL_GRASS not in self._board_model.get_game() and self._board_model.get_game().count(
            ATTEMPTED_CATCH) == len(self._board_model.get_pokemon_location())

    def check_lose(self):
        """Checking if the player has lost the game.

       Returns:
           (bool): True if the player has lost the game, false if not.

       """
        return EXPOSED_POKEMON in self._board_model.get_game()

    def get_attempted_catch(self):
        """Get the position of bokeballs.

       Returns:
           position_list(list): The list of bokeballs position.

       """
        position_list = []
        for index in self._board_model.get_game():
            if index == ATTEMPTED_CATCH:
                position_list.append(index)
        return position_list

    def check_game_over(self):
        """Check if the game is over and exit if so"""
        if self.check_win():
            for index in self._board_model.get_pokemon_location():
                self._board_model.replace_character_at_index(self._board_model.get_game(), index, EXPOSED_POKEMON)
            self.draw_board(self._board_model)
            messagebox.showinfo("You Win!", "You won! :D")
        elif self.check_lose():
            for index in self._board_model.get_pokemon_location():
                self._board_model.replace_character_at_index(self._board_model.get_game(), index, EXPOSED_POKEMON)
            self.draw_board(self._board_model)
            messagebox.showinfo("Game over", "You lose")


    def save_score(self):
        """Save the time of user used in a file, create one if do not have that file"""
        file_path = "score.txt"
        if not os.path.isfile(file_path):
            open(file_path, "w")
        user_score = str(self._status.get_saved_time())
        user_name = simpledialog.askstring(title="You won!", prompt=f"You won in {user_score}! Enter your name:")
        save_sting = f"{user_name}:{user_score}" + "\n"
        with open(file_path, "a") as file:
            file.write(save_sting)

    def save_top_three_score(self):
        """Save the top three times of users used in a file"""
        file_path = "top_three_score.txt"
        if not os.path.isfile(file_path):
            open(file_path, "w")
        with open(file_path, "w") as file:
            for scores in self.get_top_score():  # Store top three score
                user_score = f"{int(scores[1]) // 60} m {scores[1] % 60} s"  # Convert minutes to seconds
                user_name = scores[0]
                save_sting = f"{user_name}:{user_score}" + "\n"
                file.write(save_sting)

    def get_top_score(self):
        """Get the top three times of users used
           top_three(list): The list of the top three times.
        """
        file_path = "score.txt"
        get_scores = {}
        user_name_list = []
        with open(file_path, "r") as file:
            for line in file:
                user_name = line.strip().split(":")[0]
                user_name_list.append(user_name)
                user_score1 = line.strip().split(":")[1]
                user_score2 = int(user_score1[0]) * 60 + int(user_score1[4:6])
                get_scores[user_name] = user_score2
            get_scores2 = sorted(get_scores.items(), key=lambda x: x[1])  # Sort the scores
            top_three = get_scores2[0:3]  # Get the top three
        return top_three

    def load_top_three(self):
        """Load the top three times of users used from the saved file"""
        file_path = "top_three_score.txt"
        if not os.path.isfile(file_path):
            open(file_path, "w")
        top_scores = []
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                line_list = line.split(':')
                top_scores.append(line_list)
        return top_scores

    def redraw(self):
        """Redraw the whole game window."""
        self._status.reset_time()
        self._board_model.reset_game()
        self.draw_board(self._board_model)
        self._status.update_pokeball_label(pokeball_num_left=len(self._board_model.get_pokemon_location()))
        self._board_model.reset_pokeball_num()

    def random_pokemon_images(self):
        """Chose pokemon images at random."""
        pokemon_position = []
        for index in self._board_model.get_pokemon_location():
            index_to_position(index)
            pokemon_position.append(index_to_position(index))
        pokemon_list = ["charizard", "cyndaquil", "pikachu", "psyduck", "togepi", "umbreon"]
        for pokemon in pokemon_position:
            r = choice(pokemon_list)
            y, x = pokemon
            image = get_image(f"./images/pokemon_sprites/{r}")
            self.create_image(x * SQUARE_LENGTH + SQUARE_LENGTH / 2, y * SQUARE_LENGTH + SQUARE_LENGTH / 2,
                              image=image)
            self.img_ref.append(image)


class ImageBoardView(BoardView):
    """Image view of the pokemon game board, presenting if the task2 be chosen"""

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """Construct a imaged board view using the grid size and board width .

        Parameters:
            master (tk.Widget): Widget within which the board is placed.
            grid_size (int): The size of the grid.
            board_width (callable): The width of the board.
        """
        super().__init__(master, grid_size, board_width, *args, **kwargs)
        self.img_refe = []
        self._initial_box = None

    def draw_board(self, board: BoardModel):
        """Present the imaged board of the game
        Parameters:
            board: BoardModel.
        """
        image_num_list = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
        self.delete("all")
        self._board_model = board
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                character = self._board_model.get_game()[position_to_index((col, row), self._grid_size)]
                # Convert row and col to coordinate
                x1 = row * SQUARE_LENGTH
                y1 = col * SQUARE_LENGTH
                if character == TALL_GRASS:
                    image = get_image("./images/unrevealed")
                    self.create_image(x1 + SQUARE_LENGTH / 2, y1 + SQUARE_LENGTH / 2, image=image)
                    self.img_ref.append(image)
                elif character == EXPOSED_POKEMON:
                    self.random_pokemon_images()
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
        self.bind_clicks()

    def bind_clicks(self):
        """Bind clicks on the board to the left and right click handlers and the bind motion on the board.
        """
        self.bind("<Button-1>", lambda e: self._left_click((e.x, e.y)))
        self.bind("<Button-2>", lambda e: self._right_click((e.x, e.y)))
        self.bind("<Button-3>", lambda e: self._right_click((e.x, e.y)))
        self.bind("<Motion>", lambda e: self._highlight((e.x, e.y)))

    def _right_click(self, position):
        """Handle right clicking on a cell"""
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        index = position_to_index((y, x), self._grid_size)
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

    def _highlight(self, position):
        """Motion on tall grass squares will cause the grass to ‘rustle’
        """
        if position[0] >= 600 or position[1] >= 600:  # Make sure motion and highlight happen inside of the grid.
            return None
        new_box = self.get_bbox(position)
        index = int(position_to_index((new_box[1] / 60, new_box[0] / 60), self._grid_size))
        character = self._board_model.get_game()[index]
        if character == TALL_GRASS:
            if new_box != self._initial_box:
                if self._initial_box is not None:
                    image = get_image("./images/unrevealed")
                    self.create_image(int(self._initial_box[0] + SQUARE_LENGTH / 2),
                                      int(self._initial_box[1] + SQUARE_LENGTH / 2), image=image)
                    self.img_refe.append(image)
                    self.draw_board(self._board_model)
                self._initial_box = new_box
                image = get_image("./images/unrevealed_moved")
                self.create_image(int(self._initial_box[0] + SQUARE_LENGTH / 2),
                                  int(self._initial_box[1] + SQUARE_LENGTH / 2), image=image)
                self.img_refe.append(image)

    def get_bbox(self, position):
        """While motion onto a grid square return the position of the motion
        Parameters:
            position(<tuple>):The position of the motion.
        Return(<tuple<tuples>>): A tuple of motion position tuples.
        """
        x, y = position
        x //= SQUARE_LENGTH
        y //= SQUARE_LENGTH
        x1 = x * SQUARE_LENGTH
        y1 = y * SQUARE_LENGTH
        x2 = x1 + SQUARE_LENGTH
        y2 = y1 + SQUARE_LENGTH
        return x1, y1, x2, y2
    def check_game_over(self):
        """Check if the game is over and exit if so"""
        if self.check_win():
            self.random_pokemon_images()
            self._status.stop_time()
            ans = messagebox.showinfo("You Win!", "You won! :D")
            if ans:
                self.save_score()
                self.save_top_three_score()
                self._master.destroy()
        if self.check_lose():
            self._status.stop_time()
            ans = messagebox.askyesno("Game over", "You lose! Would you like to try again?")
            if ans:
                self._status.reset_time()
                self._status.update_time()
                self.redraw()
            else:
                self._master.destroy()


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
    """ Main function
    """
    root = tk.Tk()
    root.title("Pokemon: Got 2 find them all!")

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
