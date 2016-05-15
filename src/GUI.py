#! /usr/bin/env python3

from Tkinter import *
from connect_four_for_GUI import ConnectFour

class GUI:
    elementSize = 50
    gridBorder = 3
    gridColor = "#AAA"
    p1Color = "#4096EE"
    p2Color = "#FF1A00"
    backgroundColor = "#FFFFFF"
    gameOn = False
    isAtRandom = False
    

    def __init__(self, master):
        self.master = master

        master.title('Connect Four')
        
        label = Label(master, text="Connect Four")
        label.grid(row=0)

        button = Button(master, text="New Game!", command=self._newGameButton)
        button.grid(row=1)

        button1 = Button(master, text="New Game (random moves)!", command=self._newGameButtonRandom)
        button1.grid(row=2)
        
        self.canvas = Canvas(master, width=200, height=50, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=3)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=4)

        self.canvas.bind('<Button-1>', self._canvasClick)
        self.newGame()


    def draw(self):
        for c in range(self.game.size['c']):
            for r in range(self.game.size['r']):

                x0 = c*self.elementSize
                y0 = r*self.elementSize
                x1 = (c+1)*self.elementSize
                y1 = (r+1)*self.elementSize
                if self.game.gameState[r][c] == 1:
                    fill = self.p1Color
                    self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill = fill, outline=self.gridColor)

                elif self.game.gameState[r][c] == (-1):
                    fill = self.p2Color
                    self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill = fill, outline=self.gridColor)


    def drawGrid(self):
        x0, x1 = 0, self.canvas.winfo_width()
        for r in range(1, self.game.size['r']):
            y = r*self.elementSize
            self.canvas.create_line(x0, y, x1, y, fill=self.gridColor)

        y0, y1 = 0, self.canvas.winfo_height()
        for c in range(1, self.game.size['c']):
            x = c*self.elementSize
            self.canvas.create_line(x, y0, x, y1, fill=self.gridColor)


    def drop(self, column):
        return self.game.drop(column)


    def newGame(self):
        # Ask for players' names
        self.p1 = 'Blue'
        self.p2 = 'Red'

        # Ask for grid size
        columns = 7
        rows = 6
        
        self.game = ConnectFour(self.isAtRandom, columns=columns, rows=rows)
        self.canvas.delete(ALL)
        self.canvas.config(width=(self.elementSize)*columns,
                           height=(self.elementSize)*rows)
        self.master.update() # Rerender window
        self.drawGrid()
        self.draw()

        self._updateCurrentPlayer()

        self.gameOn = True


    def _updateCurrentPlayer(self):
        p = None
        self.game.player *= (-1)
        if(self.game.player == 1):
            p = self.p1  
        else: 
            p = self.p2
        self.currentPlayerVar.set('Current player: ' + p)


    def _canvasClick(self, event):
        if not self.gameOn: return
        if self.game.move_was_winning_move(self.game.gameState, self.game.player): return
        
        c = event.x // self.elementSize
        
        if (0 <= c < self.game.size['c']):
            if(self.drop(c)):
                self.draw()            
                # evaluate game state
                if self.game.move_was_winning_move(self.game.gameState, self.game.player):
                    noWinnerYet = False
                    x = self.canvas.winfo_width() // 2
                    y = self.canvas.winfo_height() // 2
                    winner = None
                    if self.game.player == 1:
                        winner = self.p1
                    else:
                        winner = self.p2
                    t = winner + ' won!'
                    self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")
                elif( self.game.move_still_possible(self.game.gameState) == 0 ):
                    x = self.canvas.winfo_width() // 2
                    y = self.canvas.winfo_height() // 2
                    self.canvas.create_text(x, y, text='there is a draw', font=("Helvetica", 32), fill="#333")
                
                self._updateCurrentPlayer()

    def _newGameButton(self):
        self.isAtRandom = False
        self.newGame()

    def _newGameButtonRandom(self):
        self.isAtRandom = True
        self.newGame()

root = Tk()
app = GUI(root)

root.mainloop()
