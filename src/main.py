from src.games import TicTacToe

# task 1.2.1
ttt = TicTacToe()
ttt.run(1000, 'move at random')
ttt.draw()
ttt.run(1000, 'move at probability x_board')
ttt.draw()
ttt.run(1000, 'move at probability x_o_board')
ttt.draw()
ttt.run(1000, 'move at heuristic')
ttt.draw()
ttt.run(1000, 'move at heuristic forward')
ttt.draw()


