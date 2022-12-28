from random import randint, uniform
from copy import deepcopy

#Initialize mutation probability, crossover rate, and population size
mutationRate = 0.01
crossoverRate = 0.7
populationSize = 10

#92 solutions in total, counter starts at 0 so reaching 91 will result in 92 solutions
target = 91
#SolutionsCounter = 0
solutionSet = set()

#Board class to contain all methods related to the board
class Board:

    #Board constructor to generate random board and calculate fitness
    def __init__(self):
        self.board = [randint(0,7) for x in range(8)]
        self.weakness = self.numberOfAttacks()

    #Fitness function to determine the number of attacks possible by a given board, want to minimize this value
    #Returns number of times queens can attack eachother for a given board
    def numberOfAttacks(self):
        #initialize total number of attacks counter
        numberOfAttacks = 0
        i = 0

        #Loop through each index on the board
        while i <=6:
            currentPiece = self.board[i]
            
            j=i+1

            #Simulate attacks for all other columns on the board
            while j <=  7: 

                #Difference between two locations determines if attack is possible
                diagonal = j -i
                defender = self.board[j]

                #Increment attack counter if queen in same row
                if currentPiece == defender:
                    numberOfAttacks +=1
                #Increment attack coutner if queen can attack another piece diagonally upward
                if currentPiece == defender + diagonal:
                    numberOfAttacks +=1
                #Increment attack counter if queen can attack diagonally downward
                if currentPiece == defender - diagonal:
                    numberOfAttacks+=1
                j=j+1
            i=i+1

        return numberOfAttacks
    
    #Mutate a random gene within a given chromosome (board), and recalculate its fitness
    def chromosomeMutation(self):
        self.board[randint(0,7)] = randint(0,7)
        self.weakness = self.numberOfAttacks()


#Determine if mutation will occur or not based on mutation rate global variable
def toMutate():
    #Generate a random number between 0 and 1
    mutation = uniform(0,1)
    
    #Only mutate if probability is less than or equal to mutation rate
    if  mutation <= mutationRate:
        return True
    else:
        return False

#Cross genes from two parent chromosomes over
def crossover(mom, dad):

    #Create a pass by value copy of the two parents
    child1 = deepcopy(mom)
    child2 = deepcopy(dad)

    #Generate random value between 0 and 1 to determine if the genes will crossover
    crossover = uniform(0,1)

    #Only cross genes over if random value is less than global variable crossoverRate
    if  crossover <= crossoverRate:

        #Generate random location to split chromosome
        splitLocation = randint(1,6)
        
        #Split chromosome on location and swap to create new children
        temp = child1.board[splitLocation:]
        child1.board[splitLocation:] = child2.board[splitLocation:]
        child2.board[splitLocation:] = temp
    
    #Update weakness/fitness of children
    child1.weakness = child1.numberOfAttacks()
    child2.weakness = child2.numberOfAttacks()

    return child1, child2

#Determine if the algorithm is completed by checking if all 92 solutions have been found
def completed():
    if len(solutionSet) == target:
        return True
    else:
        return False

#Pick two parents to breed based on the initial population array using the roulette wheel method
def roulette(populationArray):

    #Add all fitness values together from the initial population array
    weaknessSum = sum(board.weakness for board in populationArray)

    #Calculate the ratio for each fitness value based on the sum of all the fitness values to generate the range for the wheel
    ratios = [board.weakness/weaknessSum for board in populationArray]
        
    wheel = []

    #Loop through population array and creates the roulette wheel
    for i in range(len(populationArray)):
        if i == 0:
            wheel.append(ratios[i])
        if i != 0:
            wheel.append(ratios[i] + ratios[i-1])

    #Generate the value that the parents spin on the wheel
    momProbability = uniform(0,1)
    dadProbability = uniform(0,1)

    #Initialize mom and dad with objects of the board class
    mom = Board()
    dad = Board()

    #Determine which value to choose as parents based on the ratios in the roulette wheel
    for i in reversed(range(len(wheel))):
        if momProbability ==1:
            mom = populationArray[len(populationArray)]
        if momProbability <= wheel[i]:
            mom = populationArray[i]
    
    for i in reversed(range(len(wheel))):
        if dadProbability ==1:
            dad = populationArray[len(populationArray)]
        if dadProbability <= wheel[i]:
            dad = populationArray[i]
 
    return mom, dad

#Check if a solution has been found 
def solutionChecker(arr):
    for board in arr:
        #If a perfect solution (board) has been found with no possible attacks in all directions
        if board.weakness == 0:

            #Ensure only unique solutions are found based on checking if the board is in the current solution set
            if tuple(board.board) not in solutionSet:
                print("solution",len(solutionSet), "found =", board.board)

            #Add board to solution set if unique board is found
            #By default set only keeps unique values
            solutionSet.add(tuple(board.board))

if __name__ == '__main__':

    #Generate new empty population array
    populationArray = []

    #Initialize generation count to 0
    generation = 0

    #Populate population array with 10 boards
    for i in range(populationSize):
        populationArray.append(Board())

    #Check if all solutions have been found
    complete = completed()
    
    #Loop while all solutions have not been found
    while not complete:

        generation += 1

        #Create new empty population array to hold new population for next generation
        newPopulation =[]
        
        #Loop through half the population and pick 2 parents, crossover, and mutate them
        for i in range(int(populationSize/2)):

            #Pick parents to breed by spinning the wheel
            mom, dad = roulette(populationArray)
    
            #Breed chosen parents and create two children
            child1, child2 = crossover(mom,dad)
            
            #Determine if mutation will occur and mutate children if so
            if toMutate():
                child1.chromosomeMutation()
            if toMutate():
                child2.chromosomeMutation()

            #Append mutated children to new population array
            newPopulation.append(child1)
            newPopulation.append(child2)
        
        #Check if there are any solutions in the new popylation
        solutionChecker(newPopulation)

        #Update the population array for the next loop based on the children generated
        populationArray = newPopulation

    #Print final solution set
    print(solutionSet)

        
            





