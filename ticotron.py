import random
import datetime
import copy
# from HUERESTIC import hueristic
# from orig_heuristic import heuristic
ALPHA = -10000000000
BETA = 10000000000
HIGH_POS = [(0,0),(0,3),(3,0),(3,3)]
MID_POS = [(2,0),(2,3),(3,1),(3,2),(0,1),(0,2),(1,0),(1,3)]
LOW_POS = [(1,1),(1,2),(2,1),(2,2)]

class Team40:
	def __init__(self):
		self.dictn = {}
		self.timeLimit = datetime.timedelta(seconds = 15)
		self.cell_win = 100000

	def getOpp(self,flag):
		if flag=='o':
			return 'x'
		else:
			return 'o'
	
	def minimax(self,old_move, depth, max_depth, alpha, beta, isMax, p_board, my_flag,best_node,bonus_move):
		
		if datetime.datetime.utcnow() - self.timeLimit > self.begin:
			return (-1.23456,(-1,-1))
		
		opp_flag=self.getOpp(my_flag)
		
		terminal_state = p_board.find_terminal_state()
		if terminal_state[1] == 'WON' :
			if terminal_state[0] == my_flag :
				return (100000000,old_move)
			elif terminal_state[0] == opp_flag :
				return (-100000000,old_move)

		if depth==max_depth:

			utility = new_heuristic(p_board.block_status,p_board.board_status,my_flag) - new_heuristic(p_board.block_status,p_board.board_status,opp_flag)
			return (utility,old_move)
			

		else:
			children_list = p_board.find_valid_move_cells(old_move)
			random.shuffle(children_list)
			
			if len(children_list) == 0:
				utility = new_heuristic(p_board.block_status,p_board.board_status,my_flag) - new_heuristic(p_board.block_status,p_board.board_status,opp_flag)
				return (utility,old_move)

			for child in children_list:
				if isMax:
					p_board.update(old_move,child,my_flag)
				else:
					p_board.update(old_move,child,opp_flag)
				
				my_flag_won=False
				opp_flag_won=False
				
				p_block=p_board.block_status

				if p_block[child[0]/4][child[1]/4] == my_flag:
					my_flag_won=True
				
				elif p_block[child[0]/4][child[1]/4] == opp_flag:
					opp_flag_won=True
				
				if isMax and not my_flag_won:
					score = self.minimax(child,depth+1,max_depth,alpha,beta,False,p_board,my_flag,best_node,0)
					
					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] > alpha):
						best_node = child
						alpha = score[0]

				elif isMax and my_flag_won and bonus_move < 2:

					score = self.minimax(child,depth+1,max_depth,alpha,beta,True,p_board,my_flag,best_node,bonus_move+1)
					if datetime.datetime.utcnow() - self.timeLimit > self.begin:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] > alpha):
						alpha = score[0]
						best_node = child

				elif isMax and my_flag_won and not bonus_move < 2:

					score = self.minimax(child,depth+1,max_depth,alpha,beta,False,p_board,my_flag,best_node,0)
					if datetime.datetime.utcnow() - self.timeLimit > self.begin:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] > alpha):
						alpha = score[0]
						best_node = child
				elif not isMax and not opp_flag_won:

					score = self.minimax(child,depth+1,max_depth,alpha,beta,True,p_board,my_flag,best_node,0)

					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] < beta):
						beta = score[0]
						best_node = child
				elif not isMax and opp_flag_won and bonus_move < 2:

					score = self.minimax(child,depth+1,max_depth,alpha,beta,False,p_board,my_flag,best_node,bonus_move+1)
					if datetime.datetime.utcnow() - self.timeLimit > self.begin:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] < beta):
						beta = score[0]
						best_node = child

				elif not isMax and opp_flag_won and not bonus_move < 2:

					score = self.minimax(child,depth+1,max_depth,alpha,beta,True,p_board,my_flag,best_node,0)
					if datetime.datetime.utcnow() - self.timeLimit > self.begin:
						p_board.block_status[child[0]/4][child[1]/4] = '-'
						p_board.board_status[child[0]][child[1]] = '-'
						return (-1.23456,(-1,-1))
					
					if (score[0] < beta):
						beta = score[0]
						best_node = child
				p_board.block_status[child[0]/4][child[1]/4] = '-'
				p_board.board_status[child[0]][child[1]] = '-'
				
				if (alpha >= beta):
					break
			if isMax:
				return (alpha, best_node)
			else:
				return(beta, best_node)
	
	def move(self,board,old_move,my_flag) :
		temp_board = copy.deepcopy(board)
		self.begin = datetime.datetime.utcnow()

		maxDepth = 3
		valid_moves=board.find_valid_move_cells(old_move)
		random.shuffle(valid_moves)
		best_node = valid_moves[0]
		while datetime.datetime.utcnow() - self.begin < self.timeLimit:

			(g,g_node) = self.minimax(old_move,0,maxDepth,ALPHA,BETA,True,temp_board, my_flag,best_node,0)
			if g != -1.23456 :
				best_node = g_node
			maxDepth += 1
		print "My Move:  ", best_node
		return best_node

def new_heuristic(win_board,board,myflag):
	oppflag='o'
	if myflag=='o':
		oppflag='x'
	win_board_heur=[
				[0,-2000,-10000,-50000,-250000],
				[2000,0,0,150000],
				[10000,0,0],
				[50000,-150000],
				[250000],
			]
	board_heur=[
				[0,-20,-100,-500,-2500],
				[20,0,0,1500],
				[100,0,0],
				[500,-1500],
				[2500],
			]
	heuristic_val=0
	for i in range(4):
		win_board_row_my=0
		win_board_row_opp=0
		win_board_row_draw=0
		win_board_col_my=0
		win_board_col_opp=0
		win_board_col_draw=0
		for j in range(4):
			if win_board[i][j]==myflag:
				win_board_row_my+=1
			elif win_board[i][j]==oppflag:
				win_board_row_opp+=1
			else:
				win_board_row_draw+=1
			if win_board[j][i]==myflag:
				win_board_col_my+=1
			elif win_board[j][i]==oppflag:
				win_board_col_opp+=1
			else:
				win_board_col_draw+=1
	
			if board[4*i+1][4*j+1]==myflag:
				heuristic_val+=3
			if board[4*i+1][4*j+1]==oppflag:
				heuristic_val-=3
			if board[4*i+1][4*j+2]==myflag:
				heuristic_val+=3
			if board[4*i+1][4*j+2]==oppflag:
				heuristic_val-=3
			if board[4*i+2][4*j+1]==myflag:
				heuristic_val+=3
			if board[4*i+2][4*j+1]==oppflag:
				heuristic_val-=3
			if board[4*i+2][4*j+2]==myflag:
				heuristic_val+=3
			if board[4*i+2][4*j+2]==oppflag:
				heuristic_val-=3

			if board[4*i+0][4*j+1]==myflag:
				heuristic_val+=2
			if board[4*i+0][4*j+1]==oppflag:
				heuristic_val-=2
			if board[4*i+0][4*j+2]==myflag:
				heuristic_val+=2
			if board[4*i+0][4*j+2]==oppflag:
				heuristic_val-=2
			if board[4*i+3][4*j+1]==myflag:
				heuristic_val+=2
			if board[4*i+3][4*j+1]==oppflag:
				heuristic_val-=2
			if board[4*i+3][4*j+2]==myflag:
				heuristic_val+=2
			if board[4*i+3][4*j+2]==oppflag:
				heuristic_val-=2

			if board[4*i+1][4*j+0]==myflag:
				heuristic_val+=2
			if board[4*i+1][4*j+0]==oppflag:
				heuristic_val-=2
			if board[4*i+2][4*j+0]==myflag:
				heuristic_val+=2
			if board[4*i+2][4*j+0]==oppflag:
				heuristic_val-=2
			if board[4*i+2][4*j+3]==myflag:
				heuristic_val+=2
			if board[4*i+2][4*j+3]==oppflag:
				heuristic_val-=2
			if board[4*i+2][4*j+1]==myflag:
				heuristic_val+=2
			if board[4*i+2][4*j+1]==oppflag:
				heuristic_val-=2

			if(win_board[i][j]==myflag):
				heuristic_val+=2500
			elif(win_board[i][j]==oppflag):
				heuristic_val-=2500
			elif(win_board[i][j]=='-'):
				for a in range(4):
					board_row_my=0
					board_row_opp=0
					board_col_my=0
					board_col_opp=0
					for b in range(4):
						if board[4*i+a][4*j+b]==myflag:
							board_row_my+=1
						elif board[4*i+a][4*j+b]==oppflag:
							board_row_opp+=1
						if board[4*i+b][4*j+a]==myflag:
							board_col_my+=1
						elif board[4*i+b][4*j+a]==oppflag:
							board_col_opp+=1
					heuristic_val+=board_heur[board_row_my][board_row_opp]
					heuristic_val+=board_heur[board_col_my][board_col_opp]
				for a in range(2):
					for b in range(2):
						board_doctor_my=0
						board_doctor_opp=0
						if(board[4*i+a+0][4*j+b+1]==myflag):
							board_doctor_my+=1
						elif(board[4*i+a+0][4*j+b+1]==oppflag):
							board_doctor_opp+=1
						if(board[4*i+a+1][4*j+b+0]==myflag):
							board_doctor_my+=1
						elif(board[4*i+a+1][4*j+b+0]==oppflag):
							board_doctor_opp+=1
						if(board[4*i+a+1][4*j+b+2]==myflag):
							board_doctor_my+=1
						elif(board[4*i+a+1][4*j+b+2]==oppflag):
							board_doctor_opp+=1
						if(board[4*i+a+2][4*j+b+0]==myflag):
							board_doctor_my+=1
						elif(board[4*i+a+2][4*j+b+0]==oppflag):
							board_doctor_opp+=1
						heuristic_val+=board_heur[board_doctor_my][board_doctor_opp]

		if win_board_row_draw==0:
			heuristic_val+=win_board_heur[win_board_row_my][win_board_row_opp]
		if win_board_col_draw==0:
			heuristic_val+=win_board_heur[win_board_col_my][win_board_col_opp]

	for i in range(2):
		for j in range(2):
			win_board_doctor_my=0
			win_board_doctor_opp=0
			win_board_doctor_draw=0

			if(win_board[i+0][j+1]==myflag):
				win_board_doctor_my+=1
			elif(win_board[i+0][j+1]==oppflag):
				win_board_doctor_opp+=1
			else:
				win_board_doctor_draw+=1

			if(win_board[i+1][j+0]==myflag):
				win_board_doctor_my+=1
			elif(win_board[i+1][j+0]==oppflag):
				win_board_doctor_opp+=1
			else:
				win_board_doctor_draw+=1

			if(win_board[i+1][j+2]==myflag):
				win_board_doctor_my+=1
			elif(win_board[i+1][j+2]==oppflag):
				win_board_doctor_opp+=1
			else:
				win_board_doctor_draw+=1

			if(win_board[i+2][j+1]==myflag):
				win_board_doctor_my+=1
			elif(win_board[i+2][j+1]==oppflag):
				win_board_doctor_opp+=1
			else:
				win_board_doctor_draw+=1
			
			if win_board_doctor_draw==0:
				heuristic_val+=win_board_heur[win_board_doctor_my][win_board_doctor_opp]		

	if win_board[1][1]==myflag:
		heuristic_val+=200
	if win_board[1][1]==oppflag:
		heuristic_val-=200
	if win_board[1][2]==myflag:
		heuristic_val+=200
	if win_board[1][2]==oppflag:
		heuristic_val-=200
	if win_board[2][1]==myflag:
		heuristic_val+=200
	if win_board[2][1]==oppflag:
		heuristic_val-=200
	if win_board[2][2]==myflag:
		heuristic_val+=200
	if win_board[2][2]==oppflag:
		heuristic_val-=200

	if win_board[0][1]==myflag:
		heuristic_val+=100
	if win_board[0][1]==oppflag:
		heuristic_val-=100
	if win_board[0][2]==myflag:
		heuristic_val+=100
	if win_board[0][2]==oppflag:
		heuristic_val-=100
	if win_board[3][1]==myflag:
		heuristic_val+=100
	if win_board[3][1]==oppflag:
		heuristic_val-=100
	if win_board[3][2]==myflag:
		heuristic_val+=100
	if win_board[3][2]==oppflag:
		heuristic_val-=100

	if win_board[1][0]==myflag:
		heuristic_val+=100
	if win_board[1][0]==oppflag:
		heuristic_val-=100
	if win_board[2][0]==myflag:
		heuristic_val+=100
	if win_board[2][0]==oppflag:
		heuristic_val-=100
	if win_board[2][3]==myflag:
		heuristic_val+=100
	if win_board[2][3]==oppflag:
		heuristic_val-=100
	if win_board[2][1]==myflag:
		heuristic_val+=100
	if win_board[2][1]==oppflag:
		heuristic_val-=100

	return heuristic_val
