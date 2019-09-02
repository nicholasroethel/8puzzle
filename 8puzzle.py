#This program generates 10,000 random instansces of the 8puzzle problem.
#It then attempts to solve each instance of the puzzle using
#Hil Climbing, Hill Climbing with Random Restarts and Simulated Annealing.
#At the end it prints and copares the results of successes
#To run this program type python3 q6-8puzzle.py into your console.
#Please not this program may take a few minutes to run
#By Nicholas Roethel, June 7 2019

import math,random,sys,gc,copy

class Puzzle: #class for the 8 puzzle probem, 0 represents the blank
    def __init__(self,startState):
        self.goalState=[[0,1,2],[3,4,5],[6,7,8]]
        self.startState=startState

def heuristic(curr, goal): #heuristc based on how many tiles are out of row, + how many are out of column
	
	score = 0

	#checks for row 1
	if((curr[0][0] != 0) & (curr[0][0] != 1) & (curr[0][0] != 2)):
		score += 1
	if((curr[0][1] != 0) & (curr[0][1] != 1) & (curr[0][1] != 2)):
		score += 1
	if((curr[0][2] != 0) & (curr[0][2] != 1) & (curr[0][2] != 2)):
		score += 1

	#checks for row 2
	if((curr[1][0] != 3) & (curr[1][0] != 4) & (curr[1][0] != 5)):
		score += 1
	if((curr[1][1] != 3) & (curr[1][1] != 4) & (curr[1][1] != 5)):
		score += 1
	if((curr[1][2] != 3) & (curr[1][2] != 4) & (curr[1][2] != 5)):
		score += 1

	#checks for row 3
	if((curr[2][0] != 6) & (curr[2][0] != 7) & (curr[2][0] != 8)):
		score += 1
	if((curr[2][1] != 6) & (curr[2][1] != 7) & (curr[2][1] != 8)):
		score += 1
	if((curr[2][2] != 6) & (curr[2][2] != 7) & (curr[2][2] != 8)):
		score += 1
		

	#checks for col 1
	if((curr[0][0] != 0) & (curr[0][0] != 3) & (curr[0][0] != 6)):
		score += 1
	if((curr[1][0] != 0) & (curr[1][0] != 3) & (curr[1][0] != 6)):
	 	score += 1
	if((curr[2][0] != 0) & (curr[1][0] != 3) & (curr[2][0] != 6)):
		score += 1

	#checks for col 2
	if((curr[0][1] != 1) & (curr[0][1] != 4) & (curr[0][1] != 7)):
		score += 1
	if((curr[1][1] != 1) & (curr[1][1] != 4) & (curr[1][1] != 7)):
		score += 1
	if((curr[2][1] != 1) & (curr[2][1] != 4) & (curr[2][1] != 7)):
		score += 1

	#checks for col 3
	if((curr[0][2] != 2) & (curr[0][2] != 5) & (curr[0][2] != 8)):		
		score += 1
	if((curr[1][2] != 2) & (curr[1][2] != 5) & (curr[1][2] != 8)):	
		score += 1
	if((curr[2][2] != 2) & (curr[2][2] != 5) & (curr[2][2] != 8)):	
		score += 1

	return score

def swapLeft(original,i,j): #swaps the blank tile left
	if(j==0):
		return original
	else:
		swapped = original[:]
		swapped[i][j], swapped[i][j-1] = original[i][j-1], original[i][j]
		return swapped

def swapRight(original,i,j): #swaps the blank tile right
	if(j==2):
		return original
	else:
		swapped = original[:]
		swapped[i][j], swapped[i][j+1] = original[i][j+1], original[i][j]
		return swapped

def swapUp(original,i,j): #swaps the blank tile up
	if(i==0):
		return original
	else:
		swapped = original[:]
		swapped[i][j], swapped[i-1][j] = original[i-1][j], original[i][j]
		return swapped

def swapDown(original,i,j): #swaps the blank tile down
	if(i==2):
		return original
	else:
		swapped = original[:]
		swapped[i][j], swapped[i+1][j] = original[i+1][j], original[i][j]
		return swapped

def findZero(curr): #finds the blank tile
	location = []
	i=0
	j=0

	if(curr[0][0] == 0):
		i = 0
		j = 0

	elif(curr[0][1] == 0):
		i = 0
		j = 1
	
	elif(curr[0][2] == 0):
		i = 0
		j = 2

	elif(curr[1][0] == 0):
		i = 1
		j = 0

	elif(curr[1][1] == 0):
		i = 1
		j = 1

	elif(curr[1][2] == 0):
		i = 1
		j = 2

	elif(curr[2][0] == 0):
		i = 2
		j = 0

	elif(curr[2][1] == 0):
		i = 2
		j = 1

	elif(curr[2][2] == 0):
		i = 2
		j = 2

	location.append(i)
	location.append(j)
	return location

def getBestNeighbour(curr,goal,i,j,min): #gets the best neighbour state

	move1 = curr[:]
	move2 = curr[:]
	move3 = curr[:]
	move4 = curr[:]

	next = None

	if(j>0):
		temp = curr[:]
		move1 = swapLeft(temp,i,j)
		tmp = heuristic(move1,goal)
		if tmp<min:
			min = tmp
			next = move1[:]

	if(j<2):
		temp = curr[:]
		move2 = swapRight(temp,i,j)
		tmp = heuristic(move2,goal)
		if tmp<min:
			min = tmp
			next = move2[:]

	if(i>0):
		temp = curr[:]
		move3 = swapUp(temp,i,j)
		tmp = heuristic(move3,goal)
		if tmp<min:
			min = tmp
			next = move3[:]

	if(i<2):
		temp = curr[:]
		move4 = swapDown(temp,i,j)
		tmp = heuristic(move4,goal)
		if tmp<min:
			min = tmp
			next = move4[:]

	return next

def getRandomNeighbour(curr,i,j): #get a random neighbour state

	next = []
	move1 = curr[:]
	move2 = curr[:]
	move3 = curr[:]
	move4 = curr[:]

	if(j>0):
		temp = curr[:]
		move1 = swapLeft(temp,i,j)

	if(j<2):
		temp = curr[:]
		move2 = swapRight(temp,i,j)

	if(i>0):
		temp = curr[:]
		move3 = swapUp(temp,i,j)

	if(i<2):
		temp = curr[:]
		move4 = swapDown(temp,i,j)

	rand = random.sample(range(0, 4), 1)

	if rand == 0:
		next = move1
	elif rand == 1:
		next = move2
	elif rand == 2:
		next = move3
	else:
		next = move4

	return next

def acceptanceProbability(oldScore, newScore, currProb): #probabilty function for acceptance
	if newScore>oldScore:
		return 5
	else:
		tmp = math.exp((newScore-oldScore)/currProb)
		#print(tmp)
		return tmp

def generateRandomStart(): #returns a random start
	rands = random.sample(range(0, 9), 9)

	rands1 = [] 
	rands2 = []
	rands3 = []
	rands2d = []

	rands1.append(rands[0])
	rands1.append(rands[1])
	rands1.append(rands[2])
	rands2.append(rands[3])
	rands2.append(rands[4])
	rands2.append(rands[5])
	rands3.append(rands[6])
	rands3.append(rands[7])
	rands3.append(rands[8])

	rands2d.append(rands1)
	rands2d.append(rands2)
	rands2d.append(rands3)

	return rands2d


def hillClimbing(curr, goal): #basic hill climbing

	min = heuristic(curr,goal) #evaluate state
	if(min == 0):
		return curr
	
	location = findZero(curr)
	i=location[-2]
	j=location[-1]
	
	next = getBestNeighbour(curr,goal,i,j,min) #get the next state

	if(next != None): #iterate
		hillClimbing(next, goal)

	return curr

def hillClimbingRR(curr, goal, best, count, sol,ans): #find better state

	min = heuristic(curr,goal)

	if(min<best):
		best = copy.copy(min)
		tmp = list(curr)
		sol = copy.deepcopy(tmp)


	if(best == 0):
		ans.append(sol)
		return ans

	location = findZero(curr)
	i=location[-2]
	j=location[-1]
	
	next = getBestNeighbour(curr,goal,i,j,min)

	if(next!=None):
		hillClimbingRR(next,goal,best,count,sol,ans)

	count+=1
	if((next == None) & (count<5)):
		next = getRandomNeighbour(curr,i,j)	
		hillClimbingRR(next,goal,best,count,sol,ans)

	ans.append(sol)
	return ans


def simulatedAnnealing(curr,goal): #simulated anneling 

	oldScore = heuristic(curr,goal)
	currProb = 1
	minProb = .1
	alpha = 0.5

	while currProb > minProb:
		x = 1
		while x <= 10:
			if(heuristic(curr,goal)==0):
				return goal
			location = findZero(curr)
			i=location[-2]
			j=location[-1]
			newOption = getRandomNeighbour(curr,i,j)
			newScore = heuristic(newOption,goal)
			acceptProb = acceptanceProbability(oldScore, newScore, currProb)
			rand = random.sample(range(0, 2), 1)
			if acceptProb>float(rand[0]):
				curr = copy.deepcopy(newOption)
				oldScore = copy.copy(newScore)
			x += 1
		currProb = currProb*alpha
	return curr

def main():

  gc.enable()
  sys.setrecursionlimit(100000)
  states = []
  x = 0
  hcSuccesses = 0
  hcrrSuccesses = 0
  saSuccesses = 0
  
  while x<10000:
  	sol = []
  	ans = []
  	ans.clear()
  	count = 0
  	hcrr = [[9,9,9],[9,9,9],[9,9,9]] #high start heuristic
  	states.append(generateRandomStart()) 
  	startState = states[x-1]
  	puzzle = Puzzle(startState)
  	goal = puzzle.goalState
  	hc = hillClimbing(puzzle.startState,puzzle.goalState) #hill climbing result
  	ans = hillClimbingRR(puzzle.startState,goal,20,count,sol,ans)
  	for element in ans:
  		if heuristic(element,goal)<heuristic(hcrr,goal):
  			hcrr = copy.deepcopy(element) #get the smallest value from hcrr
  	sa = simulatedAnnealing(puzzle.startState,puzzle.goalState)
  	if(heuristic(hc,puzzle.goalState)==0):
  		hcSuccesses+=1
  	if(heuristic(hcrr,puzzle.goalState)==0):
  		hcrrSuccesses+=1
  	if(heuristic(sa,puzzle.goalState)==0):
  	 	saSuccesses+=1
  	x+=1
  	
  print("Tries",x) #print results
  print("Hill Climbing Successes",hcSuccesses)
  print("Hill Climbing with Random Restart Successes",hcrrSuccesses)
  print("Simulated Annealing Successes",saSuccesses)


if __name__== "__main__":
  main()

