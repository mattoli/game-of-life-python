import os, random
from patterns.patterns import *


# Cell
class Cell:
    def __init__(self, x, y):
        # Cell coordinates for convinience
        self.x = x
        self.y = y

        # neighbour count
        self.live_neighbour_count = 0

        # Init cell with dead status
        self._is_alive = False

    # Get _is_alive method & Property is_alive
    def _get_is_alive(self):
        return self._is_alive
    is_alive = property(_get_is_alive)

    # Set cell to alive/dead
    # Defaults to alive=True, pass False to set dead
    def set_alive(self, alive=True):
        self._is_alive = alive

    def _get_print_char(self):
        # is_alive use 'x', else use '-'
        if self.is_alive == True:
            return 'x'
        return '-'
    print_char = property(_get_print_char)

# Board
class Board:
    def __init__(self, num_cols, num_rows):
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._temp_board = None

        self.board = self._init_board()

    # init blank (all dead) board
    def _init_board(self):
        return [[Cell(x, y) for y in range(self._num_cols)] for x in range(self._num_rows)]

    '''
    Update methods
    handle board generations, etc
    '''
    # Flatten board to 1D
    def _flatten_board(self, board):
        for g in board:
            if isinstance(g, list):
                yield from self._flatten_board(g)
            else:
                yield g

    # Add Pattern at x, y coordinates
    def add_pattern(self, x, y, pattern):
        # Coordinates refer to top left cell of pattern
        for r, row in enumerate(pattern.pattern):
            for c, cell in enumerate(row):
                self.board[r+x][c+y].set_alive(cell)

    # generate random board
    def randomize(self):
        for row in self.board:
            for cell in row:
                if random.randint(1,5) < 3:
                    cell.set_alive(True)
                else:
                    cell.set_alive(False)
    
    # Get neighbour coordinates from cell coordinates
    def _get_neighbour_coords(self, cell):
        for x in range(cell.x - 1, cell.x + 2):
            for y in range(cell.y -1, cell.y + 2):
                if (x, y) != (cell.x, cell.y):
                    yield (x, y)

    # Check neighbours
    def _set_live_neighbour_count(self, cell):
        # Get neighbour coords
        neighbour_coords = [n for n in self._get_neighbour_coords(cell)]
        # Get live neighbours & set count
        live_neighbours = [cell for cell in self._flatten_board(self._temp_board) if (cell.x, cell.y) in neighbour_coords and cell.is_alive]
        cell.live_neighbour_count = len(live_neighbours)
        return cell
        
    
    # Get neighbour count for each cell on _temp_board
    def _set_neighbour_counts(self):
        self._temp_board = [list(map(self._set_live_neighbour_count, row)) for row in self.board]

    # Evolve 
    def _evolve_cell(self, cell):
        if cell.live_neighbour_count < 2:
            # Underpopulation, cell dies
            cell.set_alive(False)
        elif cell.live_neighbour_count < 4 and cell.is_alive == True:
            # Statis, cell survives
            pass
        elif cell.live_neighbour_count == 3 and cell.is_alive == False:
            # Reproduction, cell comes to life
            cell.set_alive(True)
        else:
            # Cell must be surrounded by > 3 living cells
            # Overpopulation, cell dies
            cell.set_alive(False)
        return cell

    # Evolve board to next generation
    def next(self):
        self._temp_board = self.board.copy()

        # set neighbour counts
        self._set_neighbour_counts()

        self.board = [list(map(self._evolve_cell, row)) for row in self.board]


    '''
    Print methods
    '''

    # create a print string of current board
    def _create_print(self):
        return '\n'.join([''.join([cell.print_char for cell in row]) for row in self.board])

    # print the board
    def print_board(self):
        print(self._create_print())






class Main:
    
    def __init__(self, generations=100, num_cols=50, num_rows=25):
        generations = generations
        num_cols = num_cols
        num_rows = num_rows

        # Init patterns
        self.patterns = Patterns()
        self.patterns.add_all_patterns()
        print(self.patterns.patterns)
        # Init blank board
        self.init_board(num_cols, num_rows)

    # Clear output     
    def clear_out(self):
        # use 'cls' to clear for Windows
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            # use 'clear' for posix

    def init_board(self, num_cols=50, num_rows=15):
        self.board = Board(num_cols=num_cols, num_rows=num_rows)

    def run(self, generations=100):

        # add glider gun
        self.board.add_pattern(1, 1, self.patterns.patterns['gosperglidergun'])

        gen_count = 1
        while gen_count <= generations:
            self.clear_out()
            print(f'Generation {gen_count}/{generations}')
            
            self.board.print_board()
            
            gen_count += 1
            # evolve next generation
            self.board.next()
        print(f'Completed {generations} generations')




if __name__ == '__main__':
    Main().run()
