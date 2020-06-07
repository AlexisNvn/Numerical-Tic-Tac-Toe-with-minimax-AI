<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

# Numerical Tic Tac Toe - WHO Academy coding challenge
Alexis Navarian - 07/06/2020 <br/>

**Submission** <br/>
Submission is given as WHO Academy - Numerical Tic Tac Toe.ipynb (Jupyter Notebook File) <br/>
A simple python script is also available, see : WHO Academy - Numerical Tic Tac Toe.py (but I still recommend the .ipynb)

**Dependencies** <br/>
The project has been realized using :
- Python 3.7
- Numpy (every version should work)
- Jupyter Notebook (every version should work)

***Rules :***
- Turn by turn game on a n x n board
- Goal is to make a line, column or diagonal equal to n(n^2+1)/2.   Ex : n = 3 -> 15
- Player 1 can only use odd numbers while Player 2 can only use even numbers.   Ex : n = 3 -> P1 : [1,3,5,7] - P2 : [2,4,6,8]

***Assumptions :***
- One number can't be placed twice. Once a number is placed, it disappear from the list of possibilities.
- A player wins only if a row/column/diagonal is FULL and its sum is equal to 15 (for n=3).   Ex : (7 8 EmptyCell) doesn't work

***Coding idea :***
- Super class Player that have "numbers" as attributes, which is the list of available numbers to the player. 
- Class Human_Player and AI_Player inherits from the Player class and have a specific function "get_move".
- Human_Player "get_move" function uses user input 
- AI_player "get_move" function uses the game configuration to output the best move calculated with an algorithm. $\quad$ Ex : minimax or random
- class Game : implementation of the whole game logic

***Project specificities :***
- should work for every board size (not only 3)
- class implementation 
- minimax with alpha beta pruning as AI algorithm
- AI algorithms and parameters comparison

***Warnings :***
- If AI is taking too much time to compute its move, please consider reducing the max_depth parameter (for minimax only)
- If you try to load a jupyter notebook cell while the program is waiting for your turn input, it will make the notebook "run forever/crash". If it happens, just close and restart the notebook. - If you want to stop the actual game early, enter 'STOP' in the input field.


# More details are given in the .ipynb file


