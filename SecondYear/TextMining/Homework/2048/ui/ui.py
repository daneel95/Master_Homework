from tkinter import *

SIZE = 800
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
SCORE_TEXT_COLOR = "#7CFC00"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}

FONT = ("Verdana", 40, "bold")


class NoUI:
    def draw_board(self, board, score):
        pass

    def init_board(self, board):
        pass

    def destroy(self):
        pass


class DrawUI:
    def __init__(self):
        self.grid_cells = []
        self.tk = Tk()
        self.__init_grid()

    def __init_grid(self):
        self.tk.grid()
        self.background = Frame(master=self.tk, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        self.background.grid(row=0)
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(self.background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
        self.__create_text()
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.grid_columnconfigure(1, weight=1)

    def __create_text(self):
        cell = Frame(self.tk, bg=BACKGROUND_COLOR_GAME)
        cell.grid(row=1, sticky='ew')
        t = Label(master=cell, text="Score: 0", bg=BACKGROUND_COLOR_CELL_EMPTY, fg=SCORE_TEXT_COLOR, justify=CENTER, font=FONT)
        t.pack()
        self.text = t

    def __update_grid_cells(self, board, score):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = board[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.text.configure(text=str(score), bg=BACKGROUND_COLOR_GAME, fg=SCORE_TEXT_COLOR)
        self.tk.update_idletasks()

    def draw_board(self, board, score):
        # Update the drawing
        self.__update_grid_cells(board, score)
        # Draw the board
        self.tk.update()
        # Give it a delay
        self.tk.after(60)

    def init_board(self, board):
        self.__update_grid_cells(board, 0)
        self.tk.update()
        self.tk.after(5)

    def destroy(self):
        self.tk.after(500)
        self.tk.destroy()
