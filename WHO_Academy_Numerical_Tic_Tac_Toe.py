import numpy as np

class Player:
    def __init__(self,name = 'Bob'):
        self.numbers = []  # list of available numbers to player
        self.name = name
    
    def set_numbers(self,numbers): # Not really sure that setters are useful in Python but anyway
        self.numbers = numbers
        
    def print_infos(self):  # Print info and available numbers list before playing a turn 
        print("Please, select a cell and a number. Answer format : column_letter row_number available_number ")
        print("Ex : 'A16' for column A, row 1 and number 6")
        print("Available numbers : ",self.numbers)
        
    def update_possibible_numbers(self,v):  # Update list - Once a number is used, it is removed from list
        self.numbers.remove(v)      
        
class Human_Player(Player):
    def get_move(self,board,mynumbers,opppnumbers):  # board and numbers aren't used here but are used for AI_Player.get_move 
        move = input()  
        return move
    

class Game:
    # Game initialization 
    def __init__(self, n=3, player0 = Human_Player(name = 'Bob'), player1 = Human_Player(name = 'John'), clear_output = True, verbose = True):  
        self.n = n 
        
        self.board = np.zeros((self.n,self.n),dtype = int)     # Create board of ize n x n
        self.win_limit = int(self.n*(self.n**2+1)/2)           # Define win limit. Ex: n = 3 => win_limit = 15
        
        self.player0 = player0                                 # Initialize players' lists
        self.player0.set_numbers(list(range(1,self.n**2+1,2))) # Player 0 gets odd numbers
        self.player1 = player1
        self.player1.set_numbers(list(range(2,self.n**2,2)))   # Player 1 gets even numbers 
        self.players = [self.player0,self.player1]
        
        self.turn = 0                                          # turn = 0 => player0's turn    turn = 1 => player1's turn
        self.state = 0                                         # Game state. 0 "continue" - 1 "Draw" - 2 "A player has won"
        
        self.winner = 'Draw'                                   # Winner is set if state = 2 - It is used for statistics 
        
        
        self.clear_output = clear_output                       # if set to True, it clears output at each game step
                                                               # if you want to debugg, set it to False
        self.verbose = verbose                                 # everything is visible only if verbose == true
                                                               # verbose = False is used for the statistical part
    
    # Function to print board 
    def print_board(self,):
        interligne = '  '+'|___'*self.n+"|"
        firstline = '  '+'____'*self.n+"_" 
        indexline = ' '+''.join(['   '+chr(x+65) for x in range(self.n)])  

        print(indexline)
        print(firstline)

        for ind,line in enumerate(self.board):
            s=str(ind+1)+" "
            for element in line:
                if element != 0:     
                    s = s +"| "+ str(element)+" "
                else:  
                    s= s +"|   "
            s = s+"|"
            print(s)
            print(interligne)        
    
    # Function to check if a move is correct, ie input only has 3 elements and all elements are valid
    def check_move(self,move):
        valid = True
        # check if len = 3 and row number is valid and column letter is valid 
        if len(move) != 3 or ord(move[0])<65 or ord(move[0])>=ord(chr(self.n+65)) or int(move[1])<1 or int(move[1])>self.n: 
            valid = False
        # check if board cell is free
        if  self.board[int(move[1])-1,ord(move[0])-65]!=0:
            valid = False
        # check if choosen numbers is available (not already used or not in list)
        if int(move[2]) not in self.players[self.turn].numbers:
            valid = False
        return valid
    
    # Convert 'A11' (Column_Letter Row_number choosen_number) format to 001 (row column value) format 
    def convert_move(self,move):
        r = int(move[1])-1
        c = ord(move[0])-65
        v = int(move[2])
        return (r,c,v)
    
    # update board and actual player's number list
    def process_move(self,r,c,v):
        self.board[r,c] = v
        self.players[self.turn].numbers.remove(v)
    
    # check if board state has changed after move represented by r,c,v - state = 0 : Continue, 1 : Draw and 2 : Victory
    def update_state(self,r,c,v):
        # Draw 
        if not np.any(self.board==0): #If no more free cell -> draw
            self.state = 1 

        # Horizontal win - sum line = 15 and no empty cell on line
        if sum(self.board[r,:])==self.win_limit and sum(self.board[r,:]==0)==0 : 
            self.state = 2

        # Vertical win - sum column = 15 and no empty cell on column
        if sum(self.board[:,c])==self.win_limit and sum(self.board[:,c]==0)==0 : 
            self.state = 2

        # Diagonals win - sum diag = 15 and no empty cell on diagonal
        # x==y => diag  
        if r==c:
            sum_diag = sum([self.board[i,i] for i in range(self.n)])
            empty_cell_diag = sum([self.board[i,i]==0 for i in range(self.n)])
            if sum_diag == self.win_limit and empty_cell_diag ==0:
                self.state = 2
        # x+y==n-1 => anti-diag - sum anti-diag = 15 and no empty cell on anti-diagonal
        elif r+c==self.n-1:
            sum_anti_diag = sum([self.board[self.n-i-1,i] for i in range(self.n)])
            empty_cell_anti_diag = sum([self.board[self.n-i-1,i]==0 for i in range(self.n)])
            if sum_anti_diag == self.win_limit and empty_cell_anti_diag ==0:
                self.state = 2
    
    def get_winner(self):
        return self.winner
    
    # game loop
    def play(self):
        #While state = "continue"
        while self.state == 0:
            #if self.clear_output: clear_output() # Jupyter Notebook function to clear output (for better visualization)
            
            # print player available numbers and actual board
            if self.verbose :
                self.players[self.turn].print_infos()
                self.print_board()
            
            # get player's move
            move = self.players[self.turn].get_move(self.board,self.players[self.turn].numbers,self.players[1-self.turn].numbers)
            
            # check if move is a valid one
            is_proper_move = self.check_move(move)
            
            # if not, ask again for a valid move
            if not is_proper_move:
                continue
            
            # else, convert move to row column value format 
            (r,c,v) = self.convert_move(move)
            
            # update game with move 
            self.process_move(r,c,v)
            
            # check if game state has changed 
            self.update_state(r,c,v)
            
            # if state has changed, handle end game
            if self.state == 1 :
                #if self.clear_output: clear_output()
                if self.verbose : 
                    self.print_board()
                    print("No more possible moves ! This is a draw")
                break 
            elif self.state == 2 : 
                #if self.clear_output: clear_output()
                if self.verbose :
                    self.print_board()
                    print("Victory ! Player : "+self.players[self.turn].name)
                self.winner = self.players[self.turn].name
                break
            
            #else, turn to other player
            self.turn = 1 - self.turn

class AI_Player(Player):  
    # Initialization 
    def __init__(self,name,max_depth=9,algo='minimax',debugging = False, verbose = True):
        
        Player.__init__(self,name)                                       # inherits super class attributes 
        
        self.max_depth = max_depth                                       # set max_depth for minimax algo
        self.algo = algo                                                 # set algo used to compute best move 
         
        self.debugging = debugging                                       # if set to True, print debugging info
        self.verbose = verbose                                           # if set to True, print when AI is thinking
    
    # Name is pretty explicit - cell 'A11' -> 001
    def convert_rcv_to_input_format(self,r,c,v):
        return chr(65+c)+str(r+1)+str(v)
    
    # Check game state (Continue - 0 ,Draw - 1, Win - 2)
    def get_game_state(self,board):
        n = board.shape[0]
        win_limit = int(n*(n**2+1)/2)
        
        lines_sum = np.sum(board,axis = 1)
        nb_empty_cells_lines = np.sum(board==0,axis = 1)
        
        columns_sum = np.sum(board,axis = 0)
        nb_empty_cells_columns = np.sum(board==0,axis = 0)
        
        diag_sum = np.sum(np.diag(board))
        nb_empty_cells_diag = np.sum(np.diag(board==0))
        
        anti_diag_sum = np.sum(np.diag(np.fliplr(board)))
        nb_empty_cells_anti_diag = np.sum(np.diag(np.fliplr(board==0)))
        
        still_empty_cells = np.any(board==0)
        
        state = 0
        if not still_empty_cells: 
            state = 1
        for i in range(n):
            if lines_sum[i]==win_limit and nb_empty_cells_lines[i] == 0:
                state = 2
                break
            if columns_sum[i]==win_limit and nb_empty_cells_columns[i] == 0:
                state = 2
                break
        if diag_sum == win_limit and nb_empty_cells_diag ==0:
            state = 2
        if anti_diag_sum == win_limit and nb_empty_cells_anti_diag == 0 :
            state = 2
        return state 
    
    # Create hallucinated next board for minimax algo 
    def get_child(self,board,r,c,v):
        board_child = board.copy()
        board_child[r,c] = v
        return board_child
    
    # minimax algorithm with alpha-beta pruning 
    # Really good explanations and pseudo-code can be found here: https://www.youtube.com/watch?v=l-hh51ncgDI
    # Score explanation : score is 0 if Draw, -1 if lose and +1 if win 
    # We add + or - 'depth/max_depth' to this score to make it chose the "shortest" path leading to the best outcome
    def minimax(self,board,depth,alpha,beta,maximizingPlayer,mynumbers,oppnumbers): # recursive function
        n = board.shape[0]
        best_r = None; best_c = None; best_v = None
        
        # Leaf case
        state = self.get_game_state(board)
        if depth == 0 or state >0:
            return (state+depth/self.max_depth-1)*(1-maximizingPlayer)+(1-state-depth/self.max_depth)*maximizingPlayer,best_r,best_c,best_v
        
        # Else continue until Leaf
        if maximizingPlayer:
            maxEval = -10
            for r in range(n):
                for c in range(n):
                    if board[r,c] != 0: # if board cell isn't free, continue to next cell
                        continue
                    for v in mynumbers:
                        board_child = self.get_child(board,r,c,v)
                        mynumbers_c = mynumbers.copy(); mynumbers_c.remove(v)
                        score,_,_,_ = self.minimax(board_child,depth-1,alpha,beta,False,mynumbers_c,oppnumbers)
                        if score > maxEval:
                            best_r = r
                            best_c = c
                            best_v = v
                            maxEval = score
                        alpha = max(alpha,score)
                        if beta <= alpha:
                            return maxEval,best_r,best_c,best_v
                        if depth == self.max_depth and self.debugging: 
                            print(r,c,v,score,maxEval,alpha,beta)
            return maxEval,best_r,best_c,best_v
        else:
            minEval = 10
            for r in range(n):
                for c in range(n):
                    if board[r,c] != 0: # if board cell isn't free, continue to next cell
                        continue
                    for v in oppnumbers:
                        board_child = self.get_child(board,r,c,v)
                        oppnumbers_c = oppnumbers.copy(); oppnumbers_c.remove(v)
                        score,_,_,_ = self.minimax(board_child,depth-1,alpha,beta,True,mynumbers,oppnumbers_c)
                        if score < minEval:
                            best_r = r
                            best_c = c
                            best_v = v
                            minEval = score
                        beta = min(beta,score)
                        if beta <= alpha:
                            return minEval,best_r,best_c,best_v
            return minEval,best_r,best_c,best_v
        
    # AI using random moves    
    def get_random_move(self,board):
        valid_rows, valid_columns = np.where(board==0)
        random_ind = np.random.randint(low = 0, high = len(valid_rows))
        random_row = valid_rows[random_ind]
        random_column = valid_columns[random_ind]
        random_value = self.numbers[np.random.randint(low = 0,high = len(self.numbers))]
        return random_row,random_column,random_value
        
        
    # Get AI's best move using desired algorithm + convert to right format
    def get_move(self,board,mynumbers,oppnumbers):
        if self.verbose:
            print("AI player is thinking. Please wait a second.")
            print("If AI is taking too much time, please consider reducing the max_depth parameter")
        if self.algo == 'minimax':
            s,r,c,v = self.minimax(board,self.max_depth,-10000,10000,True,mynumbers,oppnumbers)
            # Security measure in case no optimal solution is found
            if r == None:
                r,c,v = self.get_random_move(board)
            move = self.convert_rcv_to_input_format(r,c,v)
        elif self.algo == 'random':
            r,c,v = self.get_random_move(board)
            move = self.convert_rcv_to_input_format(r,c,v)
        else:
            print("Algo not definied")
        return move    
            
            
if __name__ == '__main__':
    # Player vs Player 
    print("Starting player vs player game")
    player_vs_player_game = Game(3,player0 = Human_Player(name = 'Myself-1'),player1 = Human_Player(name = 'Myself-2'))
    player_vs_player_game.play()
    
    # Player vs minimax AI
    print("Starting player vs minimax AI game - First move might take up to 30sec if AI has even numbers")
    player_vs_minimax_game = Game(3,player0 = Human_Player(name = 'Myself'), player1 = AI_Player(name = 'AlexNvn minimax 1.0',max_depth=9,algo='minimax'))
    player_vs_minimax_game.play()
    
    # Player vs Random AI
    print("Starting player vs random AI game")
    player_vs_minimax_game = Game(3,player0 = Human_Player(name = 'Myself'), player1 = AI_Player(name = 'Random AI',algo='random'))
    player_vs_minimax_game.play()
    
    
    # AI vs AI games
    print("Starting  AI vs AI games - Might take approx. 30 min to complete totaly")
    parameters = [('random','random',None),('mini1','minimax',1),('mini4','minimax',4),('mini9','minimax',9)] 

    games = [Game(3,
                  player0=AI_Player(name=i[0],algo=i[1],max_depth=i[2],verbose=False),
                  player1 = AI_Player(name=j[0],algo=j[1],max_depth=j[2],verbose=False),
                  verbose=False) 
                  for i in parameters for j in parameters if i!=j]
    for game in games:
        game.play()
        print(game.player0.name+" VS "+game.player1.name+" - Winner is : "+game.winner)