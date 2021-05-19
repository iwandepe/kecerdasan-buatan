from csp import *
from timeit import default_timer as timer

class SudokuCSP(CSP):

    def __init__(self, board):

        self.domains = {}
        self.neighbors = {}
        
        for v in range(81):
            self.neighbors.update({str(v): {}})
        for i in range(9):
            for j in range(9):
                name = (i * 9 + j)
                var = str(name)
                self.add_neighbor(var, self.get_row(i) | self.get_column(j) | self.get_square(i, j))
                # if the board has a value in cell[i][j] the domain of this variable will be that number
                if board[i][j] != 0:
                    self.domains.update({var: str(board[i][j])})
                else:
                    self.domains.update({var: '123456789'})

        CSP.__init__(self, None, self.domains, self.neighbors, different_values_constraint)

    # returns the right square box given row and column index
    def get_square(self, i, j):
        if i < 3:
            if j < 3:
                return self.get_square_box(0)
            elif j < 6:
                return self.get_square_box(3)
            else:
                return self.get_square_box(6)
        elif i < 6:
            if j < 3:
                return self.get_square_box(27)
            elif j < 6:
                return self.get_square_box(30)
            else:
                return self.get_square_box(33)
        else:
            if j < 3:
                return self.get_square_box(54)
            elif j < 6:
                return self.get_square_box(57)
            else:
                return self.get_square_box(60)

    # returns the square of the index's variabile, it must be 0, 3, 6, 27, 30, 33, 54, 57 or 60
    def get_square_box(self, index):
        tmp = set()
        tmp.add(str(index))
        tmp.add(str(index+1))
        tmp.add(str(index+2))
        tmp.add(str(index+9))
        tmp.add(str(index+10))
        tmp.add(str(index+11))
        tmp.add(str(index+18))
        tmp.add(str(index+19))
        tmp.add(str(index+20))
        return tmp

    def get_column(self, index):
        return {str(j) for j in range(index, index+81, 9)}

    def get_row(self, index):
            return {(str(x + index * 9)) for x in range(9)}

    def add_neighbor(self, var, elements):
        # we dont want to add variable as its self neighbor
        self.neighbors.update({var: {x for x in elements if x != var}})

class SudokuGame:
    def __init__(self):
        self.original_board = [[0 for j in range(9)] for i in range(9)]

    def set_board(self, which):
        if which == 1:
            self.original_board[0] = [0, 6, 0, 3, 0, 0, 8, 0, 4]
            self.original_board[1] = [5, 3, 7, 0, 9, 0, 0, 0, 0]
            self.original_board[2] = [0, 4, 0, 0, 0, 6, 0, 0, 7]
            self.original_board[3] = [0, 9, 0, 0, 5, 0, 0, 0, 0]
            self.original_board[4] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.original_board[5] = [7, 1, 3, 0, 2, 0, 0, 4, 0]
            self.original_board[6] = [3, 0, 6, 4, 0, 0, 0, 1, 0]
            self.original_board[7] = [0, 0, 0, 0, 6, 0, 5, 2, 3]
            self.original_board[8] = [1, 0, 2, 0, 0, 9, 0, 8, 0]
        elif which == 2:
            self.original_board[0] = [7, 9, 0, 4, 0, 2, 3, 8, 1]
            self.original_board[1] = [5, 0, 3, 0, 0, 0, 9, 0, 0]
            self.original_board[2] = [0, 0, 0, 0, 3, 0, 0, 7, 0]
            self.original_board[3] = [0, 0, 0, 0, 0, 5, 0, 0, 2]
            self.original_board[4] = [9, 2, 0, 8, 1, 0, 7, 0, 0]
            self.original_board[5] = [4, 6, 0, 0, 0, 0, 5, 1, 9]
            self.original_board[6] = [0, 1, 0, 0, 0, 0, 2, 3, 8]
            self.original_board[7] = [8, 0, 0, 0, 4, 1, 0, 0, 0]
            self.original_board[8] = [0, 0, 9, 0, 8, 0, 1, 0, 4]
        elif which == 3:
            self.original_board[0] = [0, 3, 0, 5, 0, 6, 2, 0, 0]
            self.original_board[1] = [8, 2, 0, 0, 0, 1, 0, 0, 4]
            self.original_board[2] = [6, 0, 7, 8, 3, 0, 0, 9, 1]
            self.original_board[3] = [0, 0, 0, 0, 0, 0, 0, 2, 9]
            self.original_board[4] = [5, 0, 0, 6, 0, 7, 0, 0, 3]
            self.original_board[5] = [3, 9, 0, 0, 0, 0, 0, 0, 0]
            self.original_board[6] = [4, 5, 0, 0, 8, 9, 1, 0, 2]
            self.original_board[7] = [9, 0, 0, 1, 0, 0, 0, 4, 6]
            self.original_board[8] = [0, 0, 3, 7, 0, 4, 0, 5, 0]

    def start(self, inf):
        sudoku = SudokuCSP(self.original_board)

        self.start = timer()
        print("sebelum back track")
        
        self.display_board(self.original_board)
        solution = backtracking_search(sudoku, select_unassigned_variable=mrv, order_domain_values=unordered_domain_values,
                                inference=inf)
        print("setelah back track")
        self.end = timer()
        if solution:
            print("\nSolusi ditemukan")
            for i in range(9):
                if i in [3, 6]:
                    print("------+-------+------")
                for j in range(9):
                    if j in [3, 6]:
                        print("|", end=' ')
                    index = i * 9 + j
                    print(str(solution[str(index)]) + " ", end='')
                print()
        else:
            print("\nSolusi tidak ditemukan, Cek kembali initial board")
        self.bt = sudoku.n_bt

    def display_board(self, board):
        for i in range(9):
            if i in [3, 6]:
                print("------+-------+------")
            for j in range(9):
                if j in [3, 6]:
                    print("|", end=' ')
                index = i * 9 + j
                print(str(board[i][j]) + " ", end='')
            print()
        

def main():
    time = []
    back_track = []

    # inf = no_inference
    inf = forward_checking
    # inf = mac

    which = 1

    s1 = SudokuGame()
    s1.set_board(which)
    s1.start(inf)
    back_track.append(s1.bt)

if __name__ == '__main__':
    main()