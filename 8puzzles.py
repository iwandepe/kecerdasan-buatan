# Kode Program untuk menyelesaikan 8 Puzzle problem
# dengan menggunakan algoritma A* dan Greedy Best First Search

import time


class State:
    '''
    Class yang merepresentasikan suatu state

    Atribut
    ------------------
    data: list of list
        Menyimpan data
    cost: int
        Cost yang dibutuhkan dari state awal menuju ke state saat ini
    heur: int
        Heuristik function, estimasi jarak dari state sekarang ke state tujuan
    '''

    def __init__(self, data, cost, heur):
        self.data = data
        self.cost = cost
        self.heur = heur

    def generate_child(self):
        # Fungsi untuk generate perpindahan dari state

        # Mencari index pada state yang memiliki nilai kosong (0)
        x, y = 0, 0
        for i in range(3):
            for j in range(3):
                if self.data[i][j] == 0:
                    x, y = i, j

        # Inisialisasi 4 macam pergerakan yang mungkin
        movements = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

        # Inisialisi children array dengan nilai kosong untuk menyimpan
        # hasil dari generate children
        children = []

        for movement in movements:

            # Setiap pergerakan dicek apakah pergerakan legal atau tidak
            if self.check_legal_move(movement[0], movement[1]):

                # Jika pergerakan legal maka dibuat state baru dan
                # ditambahkan pada array children
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
    '''
    Sebuah class yang merepresentasikan permainan 8 puzzle

    Atribut
    -------
    start: State
        Menyimpan start state dari permainan
    goal: State
        Menyimpan goal state dari permainan
    open: List of State
        Menyimpan state yang dikunjungi tapi belum selesai di eksplorasi
    closed: List of State
        Menyimpan state yang sudah dikunjungin dan sudah selesai di eksplorasi
    '''

    def __init__(self):

        # Inisialisasi data dari start state dan gaol state

        # Kasus pertama
        start_data = [[1, 4, 3],
                      [5, 2, 6],
                      [7, 8, 0]]

        # Kasus kedua
        # start_data = [[1, 3, 6],
        #               [2, 4, 8],
        #               [0, 5, 7]]
        goal_data = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]

        # Menghitung heuristik function dari state awal
        startHeur = self.oop(start_data, goal_data)

        # Inisialisasi start state dan goal state
        self.start = State(start_data, 0, startHeur)
        self.goal = State(goal_data, 0, 0)

        # Inisialisasi open and closed dengan nilai kosong
        self.open = []
        self.closed = []

    def f(self, state):
        return state.cost + state.heur

    def oop(self, start, goal):
        # Fungsi untuk menghitung estimasi jarak dari state saat ini ke state tujuan
        # Fungsi ini menghitung jumlah angka yang salah penempatan

        heur = 0
        for i in range(3):
            for j in range(3):
                if (start[i][j] != goal[i][j] and start[i][j] != 0):
                    heur += 1
        return heur

    def is_checked(self, state):
        # Fungsi untuk mengecek apakah sebuah state sudah pernah dicek sebelumnya atau tidak

        for open_state in self.open:
            if open_state.data == state:
                return True
        for closed_state in self.closed:
            if closed_state.data == state:
                return True

        return False

    def a_search(self):
        # Fugnsi untuk melakukan pencarian dari state awal sampai ke state tujuan dengan algoritma A*

        begin = time.time()
        self.open.append(self.start)
        iteration_count = 1

        while True:
            cur_state = self.open[0]

            # Mencari perubahan state yang mungkin lalu
            # dimasukkan ke open state
            children = cur_state.generate_child()
            for child in children:
                child.heur = self.oop(child.data, self.goal.data)
                if not self.is_checked(child.data):
                    self.open.append(child)

            # Menghapus state yang baru saja di-eksplor dari open state
            # dan memasukkan ke closed state
            self.closed.append(cur_state)
            del self.open[0]

            # Mengurutkan state yang masih belum selesai dieksplorasi
            # urut sesuai dari hasil fungsi f yang paling kecil
            self.open.sort(key=lambda state: self.f(state), reverse=False)

            # Jika heuristik function sama dengan 0
            # maka solusi sudah ditemukan dan keluar loop
            if cur_state.heur == 0:
                print("GOAL STATE FOUND:")
                print("Lots of iteration:", iteration_count)
                print("Open state", len(self.open))
                print("Closed state", len(self.closed))
                cur_state.print_state()
                break

            # Melanjutkan loop dengan state baru yang memiliki nilai
            # heuristik function paling kecil
            iteration_count += 1

        print("--- %s seconds ---\n" % (time.time() - begin))

    def greedy_search(self):
        # Fugnsi untuk melakukan pencarian dari state awal sampai ke state tujuan
        begin = time.time()
        self.open.append(self.start)
        iteration_count = 1

        while True:
            cur_state = self.open[0]

            # Mencari perubahan state yang mungkin lalu
            # dimasukkan ke open state
            children = cur_state.generate_child()
            for child in children:
                child.heur = self.oop(child.data, self.goal.data)
                if not self.is_checked(child.data):
                    self.open.append(child)

            # Menghapus state yang baru saja di-eksplor dari open state
            # dan memasukkan ke closed state
            self.closed.append(cur_state)
            del self.open[0]

            # Mengurutkan state yang masih belum selesai dieksplorasi
            # urut sesuai dari hasil fungsi heuristik yang paling kecil
            self.open.sort(key=lambda state: state.heur, reverse=False)

            # Jika heuristik function sama dengan 0
            # maka solusi sudah ditemukan dan keluar loop
            if cur_state.heur == 0:
                print("Goal state found")
                print("Lots of iteration:", iteration_count)
                print("Open state", len(self.open))
                print("Closed state", len(self.closed))
                cur_state.print_state()
                break

            # Melanjutkan loop dengan state baru yang memiliki nilai
            # heuristik function paling kecil
            iteration_count += 1

        print("--- %s seconds ---\n" % (time.time() - begin))


def main():

    puzzleA = Puzzle()
    puzzleA.a_search()

    puzzleB = Puzzle()
    puzzleB.greedy_search()


if __name__ == '__main__':
    main()
