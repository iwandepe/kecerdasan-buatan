# Kode Program untuk menyelesaikan 8 Puzzle problem
# dengan menggunakan algoritma A* dan Greedy Best First Search

import time

class State:
    def __init__(self, data, cost, heur):
        self.data = data
        self.cost = cost
        self.heur = heur

    def generate_child(self):
        x, y = 0, 0
        for i in range(3):
            for j in range(3):
                if self.data[i][j] == 0:
                    x, y = i, j

        movements = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

        children = []

        for movement in movements:
            if self.check_legal_move(movement[0], movement[1]):
                child = self.create_child(x, y, movement[0], movement[1])
                children.append(child)

        return children

    def check_legal_move(self, x, y):
        if (x >= 0 and x < 3 and y >= 0 and y < 3):
            return True
        return False

    def create_child(self, x1, y1, x2, y2):
        temp_state = []
        temp_state = self.duplicate_data()

        temp = temp_state[x2][y2]
        temp_state[x2][y2] = temp_state[x1][y1]
        temp_state[x1][y1] = temp
        return State(temp_state, self.cost+1, 0)

    def duplicate_data(self):
        temp = []
        for row in self.data:
            t = []
            for col in row:
                t.append(col)
            temp.append(t)
        return temp

    def print_state(self):
        print("Cost:", self.cost)
        print("Heur:", self.heur)
        for row in self.data:
            for col in row:
                print(col, end=" ")
            print()
        print()


class Puzzle:
    def __init__(self):

        # Inisialisasi data dari start state dan gaol state

        # Kasus pertama
        start_data = [[1, 4, 3],
                      [5, 2, 6],
                      [7, 8, 0]]
        goal_data = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

        # Kasus kedua
        # start_data = [[1, 3, 6],
        #               [2, 4, 8],
        #               [0, 5, 7]]
        # goal_data = [[1, 2, 3],
        #              [4, 5, 6],
        #              [7, 8, 0]]

        # Kasus contoh soal
        # start_data = [[2, 8, 3],
        #               [1, 6, 4],
        #               [7, 0, 5]]
        # goal_data = [[1, 2, 3],
        #              [8, 0, 4],
        #              [7, 6, 5]]

        # Kasus tugas minggu tiga
        # start_data = [[7, 2, 4],
        #               [5, 0, 6],
        #               [8, 3, 1]]
        # goal_data = [[0, 1, 2],
        #              [3, 4, 5],
        #              [6, 7, 8]]

        startHeur = self.oop(start_data, goal_data)

        self.start = State(start_data, 0, startHeur)
        self.goal = State(goal_data, 0, 0)

        self.open = []
        self.closed = []

    def f(self, state):
        return state.cost + state.heur

    def oop(self, start, goal):

        heur = 0
        for i in range(3):
            for j in range(3):
                if (start[i][j] != goal[i][j] and start[i][j] != 0):
                    heur += 1
        return heur

    def is_checked(self, state):

        for open_state in self.open:
            if open_state.data == state:
                return True
        for closed_state in self.closed:
            if closed_state.data == state:
                return True

        return False

    def a_search(self):

        begin = time.time()
        self.open.append(self.start)
        iteration_count = 1

        while True:
            cur_state = self.open[0]

            children = cur_state.generate_child()
            for child in children:
                child.heur = self.oop(child.data, self.goal.data)
                if not self.is_checked(child.data):
                    self.open.append(child)

            self.closed.append(cur_state)
            del self.open[0]

            self.open.sort(key=lambda state: self.f(state), reverse=False)

            if cur_state.heur == 0:
                print("A*")
                print("GOAL STATE FOUND:")
                print("Lots of iteration:", iteration_count)
                print("Open state", len(self.open))
                print("Closed state", len(self.closed))
                cur_state.print_state()
                break

            iteration_count += 1

        print("--- %s seconds ---\n" % (time.time() - begin))

    def greedy_search(self):
        begin = time.time()
        self.open.append(self.start)
        iteration_count = 1

        while True:
            cur_state = self.open[0]

            children = cur_state.generate_child()
            for child in children:
                child.heur = self.oop(child.data, self.goal.data)
                if not self.is_checked(child.data):
                    self.open.append(child)

            self.closed.append(cur_state)
            del self.open[0]

            self.open.sort(key=lambda state: state.heur, reverse=False)

            if cur_state.heur == 0:
                print("Greedy Best First Search")
                print("Goal state found")
                print("Lots of iteration:", iteration_count)
                print("Open state", len(self.open))
                print("Closed state", len(self.closed))
                cur_state.print_state()
                break

            iteration_count += 1

        print("--- %s seconds ---\n" % (time.time() - begin))


def main():

    puzzleA = Puzzle()
    puzzleA.a_search()

    puzzleB = Puzzle()
    puzzleB.greedy_search()


main()
