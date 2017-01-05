###  File:    MKP.py
###  Purpose: to solve the MDMKP using Traditional Jaya or Modified Jaya
###  Author:  Zachary Kern
###
import random
# just a random seed that i created so that the random numbers are repeatable
random.seed(123456789)


from collections import Counter


###  Class:   Solution
###  Purpose: this is an object that i use its methods to hold a certain
###           solution to the MDMKP.
###  methods: dimensionalSolution : will fills attribute array with zero's up to size
###                                 number of times.( used to generate initial population)
###           demandSolution:       fills attribute array with 1's size number of times
###                                 (used for initial population)
###           printSolution:        used in testing(not used in program)
###           getLength:            gets the length of the solution, used in testing ( not used in program)
###           clearSolution:        clears all atribute arrays(thought i needed it but i ended up not using in program.
###           allZero:              sets the solution array of the class to all zeros.
###           
class Solution( object ):
    def __init__(self):
        self.dim = []
        self.dem = []
        self.sol = []
        self.sequence = []
        for i in range(0,100):
            self.sequence.append(i)
        self.sequence = random.sample(self.sequence,100)
        self.newSolution = []
        self.constraintsViolated = []
        self.obj = 0
        self.violation = 0
        self.feasible = 0 
	
    def dimensionalSolution(self, size):
        for i in range(0,size):
            self.dim.append(0)
    def demandSolution(self,size):
        for i in range(0,size):
            self.dem.append(1)
            
    def printSolution(self):
        print self.data

    def getLength(self):
        return len(self.data)
    def clearSolutionDim(self):
        self.dim = []
        self.sol = []
        self.dimensionalSolution(100)

    def allZero(self, size):
        for i in range(0,size):
            self.sol.append(0)
    

###  Class:   Problems
###  Purpose: This is used to do all of the operations in the metaheuristic to solve the MDMKP 
###
###  Methods:
###         getProblems :      this is where the txt file is read in and the problem is gotten and formatted into a usable manner.
###         solveProblem:      Where the problem type is set and the method solve problem is called.( only problem1 or case 1 is set because I only did work on 1 demand constraint)
###         readObj:           used in testing( not used in program)
###         printConstraints:  does what it sounds like (not used in program)
###         sumProduct:        this method is used to get things like the overal solution, it is used to check feasiblity and anything like that.
###                            it takes two arrays L1 and L2; L1_i * L2_i summed up accross whole array.
###         setConstraints:    this will take the data read in from txt file and map it into usable arrays.
###         solveSubProblem1:  This is where the entire metaheuristic is performed. for case 1: 1 demand constraint
###         checkDimFeasible:  This will check if only the dimensional constraints are feasible; used for half of the intial population.
###         checkDemFeasible:  This will check if only the demand constraints are feasible; used for half of the initial population.
###         checkFeasible:     This checks if the solution is feasible accross dimensional and demand constraints.
###         uniqueList:        Checks to make sure if the solution being put into inital is unique.
###         mergeSort:         Modified merge sort that sorts the solutions in decending order in respect to violation; tiebreakers go to highest objective value.
###         violatedContraints:Where the violation attribute is set. the ammount each constraint is violated by. if feasible violation will be 0.
###         JAYA:              This is where the JAYA code is.
###         ModifiedJAYA:      This is where the modified JAYA code is.


class problems( object ):
    def __init__(self):
        self.total=0

    def getProblem( self, problemNumber ):
        file = open('beasleyMDMKP1.txt', 'r')
        textFiles = file.readlines()
        size = len(textFiles)/15
        self.problem = textFiles[(problemNumber*size):((problemNumber+1)*size)]
        
    def solveProblem(self, problemList):
        self.setConstraints(problemList)
        self.solveSubProblem1(self.subProb1OBJ,self.dimConstraint1,self.dimConstraint2,self.dimConstraint3,self.dimConstraint4,self.dimConstraint5,self.demConstraint1,self.dimRHS,self.demRHS)
        
    def readObj(self,size):
        for i in range(0,size):
            self.obj.append(i)
    def printConstraint(self):
        print self.obj

    def sumProduct(self,SolutionList,ConstraintList):
        self.total = 0
        for i in range(0,len(SolutionList)):
            self.total += SolutionList[i]*ConstraintList[i]
        return self.total

    def setConstraints(self, problemList):
        self.dimConstraint1 = map(int,problemList[1].split())
        self.dimConstraint2 = map(int,problemList[2].split())
        self.dimConstraint3 = map(int, problemList[3].split())
        self.dimConstraint4 = map(int, problemList[4].split())
        self.dimConstraint5 = map(int, problemList[5].split())
        self.dimRHS = map(int,problemList[6].split())
        self.demConstraint1 = map(int,problemList[7].split())
        self.demConstraint2 = map(int, problemList[8].split())
        self.demConstraint3 = map(int, problemList[9].split())
        self.demConstraint4 = map(int, problemList[10].split())
        self.demConstraint5 = map(int, problemList[11].split())
        self.demRHS = map(int, problemList[12].split())
        self.subProb1OBJ = map(int, problemList[13].split())
        self.subProb2OBJ = map(int, problemList[14].split())
        self.subProb3OBJ = map(int,problemList[15].split())
        self.subProb4OBJ = map(int,problemList[16].split())
        self.subProb5OBJ = map(int,problemList[17].split())
        self.subProb6OBJ = map(int,problemList[18].split())

    def solveSubProblem1(self,subProb1OBJ,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,demConstraint1,dimRHS,demRHS):
        self.populationList = []
        #for i in range(0,50):
        #100 initial solutions in dimensional respect
        for i in range(0,100):
            x = Solution()
            x.dimensionalSolution(100)
            for i in x.sequence:
                x.dim[i] = 1
                if (self.checkDimFeasible(x.dim,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS) != True ):
                    x.dim[i] = 0
            x.sol = x.dim
            self.populationList.append(x)
        #100 initial solutions in demand respect
        for i in range(0,100):
            x = Solution()
            x.demandSolution(100)
            for i in x.sequence:
                x.dem[i] = 0
                if (self.checkDemFeasible(x.dem,demConstraint1,demRHS) != True):
                    x.dem[i] = 1
            x.sol = x.dem
            #combine all the solutions,
            self.populationList.append(x)
        #Then sort all of the solutions and take the best 30.
        for i in self.populationList:
            if (self.checkFeasible(i,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ) == True):
                i.feasible = 1
            self.violatedConstraints(i,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ)
        print("first merge sort")
        self.mergeSort(self.populationList)
        #for i in self.populationList:
            #print i.obj
        self.uniqueList(self.populationList)
        print("Initial")
        for i in self.population30:
            print i.violation, "\t", i.obj, "\t", i.feasible, "\t", i.constraintsViolated
        print("")
        #600 iterations of JAYA or Modified JAYA
        for i in range(0,600):
            #for modified JAYA just uncoment line below and comment out JAYA and mergeSort.
            #self.ModifiedJAYA(self.population30,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ)
            self.JAYA(self.population30,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ)
            self.mergeSort(self.population30)
        for i in self.population30:
            print i.violation, "\t", i.obj, "\t", i.feasible, "\t", i.constraintsViolated
        

    def checkDimFeasible(self,SolutionDimList,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS):
        if (self.sumProduct( SolutionDimList,dimConstraint1) <= dimRHS[0]):
            if (self.sumProduct( SolutionDimList,dimConstraint2) <= dimRHS[1]):
                if (self.sumProduct( SolutionDimList,dimConstraint3) <= dimRHS[2]):
                    if (self.sumProduct( SolutionDimList,dimConstraint4) <= dimRHS[3]):
                        if (self.sumProduct( SolutionDimList,dimConstraint5) <= dimRHS[4]):
                            return True
        return False

    def checkDemFeasible(self,SolutionDemList, demConstraint1,demRHS):
        if (  self.sumProduct( SolutionDemList,demConstraint1) >= demRHS[0]):
            return True
        return False

        
    def checkFeasible(self,Solution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ):
        self.violation = 0
        self.constraintsViolated = [] 
        if (self.sumProduct( Solution.sol,dimConstraint1) <= dimRHS[0]):
            if (self.sumProduct( Solution.sol,dimConstraint2) <= dimRHS[1]):
                if (self.sumProduct( Solution.sol,dimConstraint3) <= dimRHS[2]):
                    if (self.sumProduct( Solution.sol,dimConstraint4) <= dimRHS[3]):
                        if (self.sumProduct( Solution.sol,dimConstraint5) <= dimRHS[4]):
                            if (  self.sumProduct( Solution.sol,demConstraint1) >= demRHS[0]):
                                return True   
        
        return False

    def uniqueList(self,populationList):
        self.population30 = []
        for x in populationList:
            if x not in self.population30:
                self.population30.append(x)
       
        #print len(self.population30)
        #self.mergeSort(self.population30)
        self.population30= self.population30[:30]
        
                                    
                                 

    def mergeSort(self,populationList):
        if len(populationList)>1:
            mid = len(populationList)//2
            lefthalf = populationList[:mid]
            righthalf = populationList[mid:]
            self.mergeSort(lefthalf)
            self.mergeSort(righthalf)

            i=0
            j=0
            k=0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i].violation < righthalf[j].violation:
                    populationList[k]=lefthalf[i]
                    i=i+1    
                elif lefthalf[i].violation == righthalf[j].violation:
                    if lefthalf[i].obj > righthalf[j].obj:
                        populationList[k]=lefthalf[i]
                        i=i+1
                    else:
                        populationList[k]=righthalf[j]
                        j=j+1

                else:
                    populationList[k]=righthalf[j]
                    j=j+1
                k=k+1

            while i < len(lefthalf):
                populationList[k]=lefthalf[i]
                i=i+1
                k=k+1

            while j < len(righthalf):
                populationList[k]=righthalf[j]
                j=j+1
                k=k+1

                
    
    def violatedConstraints(self,Solution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ):
        self.violation = 0
        self.constraintsViolated = []
        self.obj = 0
        if (self.sumProduct( Solution.sol,dimConstraint1) > dimRHS[0]):
            Solution.violation += ( self.sumProduct( Solution.sol,dimConstraint1) - dimRHS[0])
            Solution.constraintsViolated.append(1)    

        if (self.sumProduct( Solution.sol,dimConstraint2) > dimRHS[1]):
            Solution.violation += ( self.sumProduct( Solution.sol,dimConstraint2) - dimRHS[1])
            Solution.constraintsViolated.append(2)

        if (self.sumProduct( Solution.sol,dimConstraint3) > dimRHS[2]):
            Solution.violation += ( self.sumProduct( Solution.sol,dimConstraint3) - dimRHS[2])
            Solution.constraintsViolated.append(3)

        if (self.sumProduct( Solution.sol,dimConstraint4) > dimRHS[3]):
            Solution.violation += ( self.sumProduct( Solution.sol,dimConstraint4) - dimRHS[3])
            Solution.constraintsViolated.append(4)

            
        if (self.sumProduct( Solution.sol,dimConstraint5) > dimRHS[4]):
            Solution.violation += ( self.sumProduct( Solution.sol,dimConstraint5) - dimRHS[4])
            Solution.constraintsViolated.append(5)

            
        if (  self.sumProduct( Solution.sol,demConstraint1) < demRHS[0]):
            Solution.violation += (demRHS[0] - self.sumProduct( Solution.sol,demConstraint1))
            Solution.constraintsViolated.append(6)

        Solution.obj = self.sumProduct(Solution.sol,subProb1OBJ)                                                    

    def JAYA(self, populationList,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ):
        #assign best and worst solution for JAYA algorithm
        best= self.population30[0]
        worst = self.population30[29]
        
        #runs through entire population.
        for j in range(0,30):
            #create a new solution and start it off will all zeros.
            newSolution = Solution()
            newSolution.allZero(100)
            #the size for this case is 100. So this runs for each bit in the solution.
            for i in range(0,100):
                R1 = random.randint(0,1)
                R2 = random.randint(0,1)
                bitValue = (populationList[j].sol[i] + R1*(best.sol[i] - populationList[j].sol[i]) - R2*(worst.sol[i] - populationList[j].sol[i]))
                if bitValue<= 0 :
                    newSolution.sol[i] = 0
                else:
                    newSolution.sol[i] = 1
            
            if (self.checkFeasible(newSolution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ) == True):
                newSolution.feasible = 1
            self.violatedConstraints(newSolution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ)
            #print newSolution.violation, "\t", newSolution.obj, "\t", newSolution.feasible, "\t", newSolution.constraintsViolated

            #if the new solutions violation is better then current position insert it in the population at current position.
            #if they are tied the higher objective value gets put in the population
            if newSolution.violation < populationList[j].violation:
                self.population30[j] = newSolution
            elif newSolution.violation == populationList[j].violation:
                if newSolution.obj > populationList[j].obj:
                    self.population30[j] = newSolution

        
        
    def ModifiedJAYA(self, populationList,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ):
        #Same as JAYA however you collect all 30 generated solutions, attach them to the population, sort and take the best 30.
        best= self.population30[0]
        worst = self.population30[29]
        jayaList = []
        jayaList = list(populationList)
        
        for j in range(0,30):
            newSolution = Solution()
            newSolution.allZero(100)
            for i in range(0,100):
                R1 = random.randint(0,1)
                R2 = random.randint(0,1)
                bitValue = (populationList[j].sol[i] + R1*(best.sol[i] - populationList[j].sol[i]) - R2*(worst.sol[i] - populationList[j].sol[i]))
                if bitValue<= 0 :
                    newSolution.sol[i] = 0
                else:
                    newSolution.sol[i] = 1

            if (self.checkFeasible(newSolution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ) == True):
                newSolution.feasible = 1
            self.violatedConstraints(newSolution,dimConstraint1,dimConstraint2,dimConstraint3,dimConstraint4,dimConstraint5,dimRHS,demConstraint1,demRHS,subProb1OBJ)
            #print newSolution.violation, "\t", newSolution.obj, "\t", newSolution.feasible, "\t", newSolution.constraintsViolated
            if j > 0:
                jayaList.append(newSolution)
        self.mergeSort(jayaList)
        jayaList = jayaList[:30]
        self.population30 = list(jayaList)
        #for i in jayaList:
         #   print i.violation, "\t", i.obj, "\t", i.feasible, "\t", i.constraintsViolated
        #print("")   


#This is the main part of the program.

problem1 = problems()
problem1.getProblem(14)
problem1.solveProblem(problem1.problem)

