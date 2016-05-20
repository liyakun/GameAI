from Tkinter import *
from connect_four import ConnectFour
from time import sleep


class GUI:
    elementSize = 80
    gridBorder = 3
    gridColor = "#AAA"
    p1Color = "#4096EE"
    p2Color = "#FF1A00"
    backgroundColor = "#FFFFFF"
    isAtRandom = False

    def __init__(self, master):
        self.master = master

        master.title('Connect Four')
        
        label = Label(master, text="Connect Four")
        label.grid(row=0)

        button = Button(master, text="New Game, you can play by yourself!", command=self._newGameButton)
        button.grid(row=1)

        button1 = Button(master, text="New Game (random automatic moves)!", command=self._newGameButtonRandom)
        button1.grid(row=2)

        button1 = Button(master, text="New Game - optimized moves!", command=self._newGameButtonOptimized)
        button1.grid(row=3)

        
        self.canvas = Canvas(master, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=4)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=5)

        self.canvas.bind('<Button-1>', self._canvasClick)
        self.newGame()

    def drawGameState(self):
        #sleep(0.3)
        max_row = self.game.size['r'] -1
        for c in range(self.game.size['c']):
            for r in range(self.game.size['r']):

                x0 = c*self.elementSize
                y0 = (max_row-r)*self.elementSize
                x1 = (c+1)*self.elementSize
                y1 = ((max_row-r)+1)*self.elementSize
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
        self.drawGrid()
        self.drawGameState()
        self.master.update() # Rerender window

        self._updateCurrentPlayer()

    def _updateCurrentPlayer(self):
        
        self.game.update_player()
        
        p = None
        if(self.game.player == 1):
            p = self.p1  
        else: 
            p = self.p2
        self.currentPlayerVar.set('Current player: ' + p)

    def drawAndCheckForWinning(self):
        self.drawGameState()            
        # evaluate game state
        if self.game.move_was_winning_move(self.game.gameState, self.game.player):
            self.game.noWinnerYet = False
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.player == 1:
                winner = self.p1
            else:
                winner = self.p2
            t = winner + ' won!'
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")
        elif( self.game.move_still_possible(self.game.gameState) == 0 ):
            self.game.noWinnerYet = False
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            self.canvas.create_text(x, y, text='there is a draw', font=("Helvetica", 32), fill="#333")

    def _canvasClick(self, event):
        if not self.game.noWinnerYet: return
        if self.game.move_was_winning_move(self.game.gameState, self.game.player): return
        
        c = event.x // self.elementSize
        if (0 <= c < self.game.size['c']):
            if(self.drop(c)):
                self.drawAndCheckForWinning()
                self._updateCurrentPlayer()
    
    def sleepInGame(self):
        sleep(0.2)
        self.master.update() # Rerender window


    def runRandomGame(self, isSleep):
        while(self.game.noWinnerYet ):
            if(self.drop(1)):
                self.drawAndCheckForWinning()
                self._updateCurrentPlayer()
                self.sleepInGame()
    
    def runOptimizedGame(self, isSleep):
        while(self.game.noWinnerYet ):
            self.game.move_min_max(self.game.gameState, 1,2)
            self.drawAndCheckForWinning()
            self._updateCurrentPlayer()
            self.sleepInGame()

    def _newGameButton(self):
        self.gameType = 0;
        self.newGame()


    def _newGameButtonRandom(self):
        self.gameType = 1;
        self.newGame()
        self.runRandomGame(True)


    def _newGameButtonOptimized(self):
        self.gameType = 2;
        self.newGame()
        self.runOptimizedGame(True)
        # connect here optimization

root = Tk()
app = GUI(root)

root.mainloop()
