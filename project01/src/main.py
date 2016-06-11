from games import TicTacToe

# task 1.2.1
ttt = TicTacToe()
#ttt.run(1000, 'move at random')
#ttt.draw(True)
ttt.run(1000, 'move at probability x_board')
ttt.draw(False)
ttt.run(1000, 'move at probability x_o_board')
ttt.draw(False)
ttt.run(1000, 'move at heuristic')
ttt.draw(False)
ttt.run(1000, 'move at heuristic forward')
ttt.draw(False)


