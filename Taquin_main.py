from tkinter import *
from Solver import Puzzle
from Solver import Solver

#création afficheur 3x3
fenetre = Tk()
board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
photos = []
for i in range(0, 16):
    photos.append(PhotoImage(file="./images/" + str(i) + ".png"))
Lph = photos[0:9]
can = Canvas(width=180 * 3, height=180 * 3, bg='white')
can.pack(side=TOP, padx=20, pady=20)
fenetre['bg'] = 'white'
fenetre.title('Tp AI')
puzzle = Puzzle(board, can, Lph)

#mélange des cases aléatoires dans le jeu de taquin 
#et affiche la meilleure solution trouvée
def melanger():
    global puzzle
    puzzle = puzzle.shuffle()
    solver = Solver(puzzle,fenetre)
    solution_largeur = solver.solve_largeur()
    solution_profondeur = solver.solve_profondeur()
    if not solution_profondeur:
        solution_profondeur= [0 for i in range(50)]
    solution_a = solver.solve_a()
    #on choisit la solution optimale parmi les 3 recherches pour afficher son démarche
    if len(solution_a) < len(solution_profondeur):
        if len(solution_a) < len(solution_largeur):
            solver.aff5(solution_a, i=0)
        else:
            solver.aff5(solution_largeur, i=0)
    else:
        if len(solution_profondeur) < len(solution_largeur):
            solver.aff5(solution_profondeur, i=0)
        else:
            solver.aff5(solution_largeur, i=0)

#configuration d'affichage
LAff = []
for row in puzzle.board:
    LAff.extend(row)
Button(text='melanger', command=melanger).pack(side=LEFT)
for k in range(len(Lph)):
    eff = can.create_image((30 + 150 * (k % 3)), 30 + (150 * (k // 3)), anchor=NW, image=Lph[0])
    aff = can.create_image((30 + 150 * (k % 3)), 30 + (150 * (k // 3)), anchor=NW, image=Lph[LAff[k]])
can.pack()
fenetre.mainloop()