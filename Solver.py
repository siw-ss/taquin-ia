import random
import itertools
import collections
import time
from tkinter import *


class Node:

    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if parent:
            self.g = parent.g + 1
        else:
            self.g = 0
        self.h = puzzle.h2()

    @property
    def state(self):
        return str(self.puzzle)

    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        return self.puzzle.solved

    @property
    def actions(self):
        return self.puzzle.actions

    def __str__(self):
        return str(self.puzzle) + ' ,g:' + str(self.g) + ' ,h:' + str(self.h)

    def f(self):
        return self.g + self.h


class Solver:

    def __init__(self, start, fenetre):
        self.start = start
        self.fenetre = fenetre

    def solve_largeur(self):
        print("Recherche de solution en largeur")
        start_time = time.perf_counter()
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        visitee = 0
        while queue:
            node = queue.pop()
            if node.solved:
                end_time = time.perf_counter()
                z = list(node.path)
                print("solution trouvée en", len(z) - 1, " coups")
                print("temps de resolution ", end_time-start_time, " s")
                print("nombre de noeds visitees ", len(seen))
                return z
            visitee+=1
            for move, action in node.actions:
                child = Node(move(), node, action)
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

    def solve_profondeur(self):
        print("Recherche de solution en profondeur")
        start_time = time.perf_counter()
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        visitee = 0
        while queue:
            node = queue.pop()
            if node.solved:
                end_time = time.perf_counter()
                z = list(node.path)
                print("solution trouvée en", len(z) - 1, " coups")
                print("temps de resolution ", end_time-start_time, " s")
                print("nombre de noeds visitees ", visitee)
                return z
            visitee+=1
            if node.g < 40:
                for move, action in node.actions:
                    child = Node(move(), node, action)
                    if child.state not in seen:
                        queue.append(child)
                        seen.add(child.state)
        end_time = time.perf_counter()
        print("aucun solution trouvee")
        print("temps de recherche ", end_time-start_time, " s")
        print("nombre de noeds visitees ", visitee)
            
                

    def solve_a(self):
        print("Recherche de solution en a*")
        start_time = time.perf_counter()
        ouvertSet = set([Node(self.start).state])
        ouvert = [Node(self.start)]
        fermeSet = set()
        ferme = []
        while len(ouvert) > 0:
            node = min(ouvert,key= lambda e: e.f())
            if node.solved:
                end_time = time.perf_counter()
                z = list(node.path)
                print("solution trouvée en", len(z) - 1, " coups")
                print("temps de resolution ", end_time - start_time, " s")
                print("nombre de noeds visitees ", len(ferme))
                return z
            ouvert.remove(node)
            ouvertSet.remove(node.state)
            ferme.append(node)
            fermeSet.add(node.state)
            for move, action in node.actions:
                child = Node(move(), node, action)
                if child.state in ouvertSet:
                    for i in ouvert:
                        if(i.state == child.state and i.g< child.g):
                            i.parent = node
                            i.g = child.g
                            break
                elif child.state in fermeSet:
                    continue
                else :
                    ouvert.append(child)
                    ouvertSet.add(child.state)
                
        print("not found")

    def aff5(self, p, i=1):
        node = p[0]
        p = p[1:]
        x = node.puzzle.convL()
        print("coup", i, " : ", x)
        node.puzzle.afficher2(x)
        if p:
            self.fenetre.after(500, self.aff5, p, i + 1)
        else:
            print("fin")


class Puzzle:

    def __init__(self, board, root, Lph):
        self.width = len(board[0])
        self.board = board
        # self.top = tkinter.Toplevel(root)
        self.can = root
        self.Lph = Lph

    @property
    def solved(self):

        tab = []
        sol = True
        for i in range(self.width):
            tab.extend(self.board[i])
        for j in range(len(tab) - 2):
            if tab[j] != (tab[j + 1] - 1):
                return False
        if tab[-1] != 0:
            sol = False
        return sol

    @property
    def actions(self):
        def create_move(at, to):
            return lambda: self.move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'R': (i, j - 1),
                      'L': (i, j + 1),
                      'D': (i - 1, j),
                      'U': (i + 1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                        self.board[r][c] == 0:
                    move = create_move((i, j), (r, c)), action
                    moves.append(move)
        return moves

    def shuffle(self):
        puzzle = self
        for k in range(50):
            puzzle = random.choice(puzzle.actions)[0]()
        x = puzzle.convL()
        print(x)
        self.afficher2(x)
        self = puzzle
        puzzle.board = self.board
        return puzzle

    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board, self.can, self.Lph)

    def move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def afficher2(self, liste1):
        "afficher les images sur le canvas"
        for k in range(len(liste1)):
            eff = self.can.create_image((30 + 150 * (k % self.width)), 30 + (150 * (k // self.width)), anchor=NW,
                                        image=self.Lph[0])
            aff = self.can.create_image((30 + 150 * (k % self.width)), 30 + (150 * (k // self.width)), anchor=NW,
                                        image=self.Lph[liste1[k]])

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def convL(self):
        L = []
        for row in self.board:
            L.extend(row)
        return L

    def h(self):
        h = -1
        i = 0
        for ligne in self.board:
            j = 1
            for case in ligne:
                if (i * self.width + j) != case:
                    h += 1
                j += 1
            i += 1
        return h

    def h2(self):
        h = 0
        i = 0
        for ligne in self.board:
            j = 0
            for case in ligne:
                x = (case - 1) // self.width
                y = (case - 1) % self.width
                if ((i != x) or j != y) and case != 0:
                    h += abs(i - x) + abs(j - y)
                j += 1
            i += 1
        return h

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row
