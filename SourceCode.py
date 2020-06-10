import random

#>>>>>>>>>>VARIABLES<<<<<<<<<<
N = 110 #gene
P = 50 #population
generations = 50 #Generations
Pm = 20# pop mutation (divided by 1000 to get percentage)
#ConL = 6 #Conditions
NumR = 10 #Number of rules
#Vars = 6 # Number of variables
DataSize = 200 # Data size
DataFile = "data4.txt"
VarSize= 9 # Size of variables in data sets 3 and 4, including space and decimal 

#If statements changing parameters based on which data file is selected 
if (DataFile == "data3.txt"):
    ConL = 6
else:
    ConL = 10
    
if (DataFile == "data3.txt"):
    Vars = 6
else:
    Vars = 10


    
#>>>>>>>>>>DATA TYPES<<<<<<<<<<
#Data type for individual 
class individual():
    def __init__(self):
        self.gene = [0 for _ in range(0,N)]
    fitness = 0    
population = [individual() for _ in range(0,P)]  
offspring = [individual() for _ in range(0,P)]
    
#Data type for rules
class rule():
    def __init__ (self):
        self.cond = [0]*ConL
        self.output = 0

#Data type for variables
class data():
    def __init__ (self):
        self.variables = [0]*Vars
        self.output = 0
        
#Reading Data File       
ReadData = [data() for i in range (DataSize)]

f = open (DataFile, "r")
for i in range(0,DataSize):
    for j in range (0, ConL):
        pointer = ""
        for k in range (0,VarSize):
            pointer += (f.read(1))
        ReadData[i].variables[j] = float(pointer)
    ReadData[i].output = int(f.read(2))
        
   # print (ReadData[i].variables,ReadData[i].output) 
  
#populate array with 0s, 1s & #s
for i in range(0,P):
    for j in range(0,N):
        if ((j+1)%(ConL+1)==0):
            population[i].gene[j] = random.randint(0,1)
        else:
            percentage = 0.33
            population[i].gene[j] = random.random()    
            if random.random() < percentage:
                population[i].gene[j] = '#'
   # print (population[i].gene)

# Original array population with 0s and 1s
#for i in range(0,P):
 #   for j in range(0,N):
  #      population[i].gene[j] = random.randint(0,1)
   # population[i].fitness = 0

#>>>>>>>>>>FUNCTIONS<<<<<<<<<<        
#>>>>>PARENT FUNCTION
def parentFunc():           
#Pick best parent
    for i in range(0,P):
        parent1a = random.randint(0,P-1)
        parent1b = random.randint(0,P-1)
        parent2a = random.randint(0,P-1)
        parent2b = random.randint(0,P-1)

        #parent 1
        if (population[parent1a].fitness >= population[parent1b].fitness):
            parent1 = parent1a
        else:
            parent1 = parent1b

        #parent 2
        if (population[parent2a].fitness >= population[parent2b].fitness):
            parent2 = parent2a  
        else:
            parent2 = parent2b

        #Crossover
        if (i % 2) == 0:
            C = random.randint(0,N) # crossover point
                    
            #offspring 1
            offspring[i].gene[0:C] = population[parent1].gene[0:C]
            offspring[i].gene[C:N] = population[parent2].gene[C:N]

            #offspring 2
            offspring[i+1].gene[0:C] = population[parent2].gene[0:C]
            offspring[i+1].gene[C:N] = population[parent1].gene[C:N]     

#>>>>>MUTATION FUNCTION
def mutationFunc():
    for i in range (0,P):
            for j in range (0,N):
                if ((j+1)%(ConL+1)==0):
                    population[i].gene[j] = random.randint(0,1)
                else:
                    Mutation_percentage = 0.33
                    if (random.randint(0,1000) <= Pm):
                        population[i].gene[j] = random.random()    
                    if random.random() < Mutation_percentage:
                        population[i].gene[j] = '#'

# Original mutation
#def mutationFunc():
 #   for i in range (0,P):
  #          for j in range (0,N):
   #             if (random.randint(0,1000) <= Pm):
    #                if (offspring[i].gene[j]):
     #                   offspring[i].gene[j] = 0
      #              else:
       #                 offspring[i].gene[j] = 1
                    
                
#>>>>>ORIGINAL FITNESS FUNCTION
#def fitFunc():
 #   for i in range(0,P):
  #      offspring[i].fitness = 0
   #     for j in range(0,N):
    #       if (offspring[i].gene[j] == 1):
     #          offspring[i].fitness = offspring[i].fitness + 1
     
      #>>>>>>>>>>>>>>>>>>>>MATCHING FUNCTION
def matching(DataVariables,RuleVariables):
    
    match_condition = 0
    match_all = 0
    
    for i in range(0,ConL):
        if (RuleVariables[i] == '#'):
            match_condition += 1
        elif(float(RuleVariables[i]) + 0.15 <= float(DataVariables[i])) | (float(RuleVariables[i]) - 0.15 >= float (DataVariables[i])):
            match_condition += 1 
    if (match_condition == ConL):
        match_all = 1
    return match_all

#>>>>>>>>>>>>>>>>>>>>NEW FITNESS FUNC 
def fitFunc (x):
    fitness = 0
    Rulebase = [rule() for _ in range(0,NumR)]
    k = 0   
    for i in range(0,NumR-1):
        for j in range(0,ConL):           
            Rulebase[i].cond[j] = population[x].gene[k]
            k += 1 
        Rulebase[i].output = population[x].gene[k]
        k += 1   
    for i in range (0,DataSize-1):
        for j in range (0,NumR-1):
            if (matching(ReadData[i].variables,Rulebase[j].cond) == 1):
                if (ReadData[i].output == Rulebase[j].output):
                    fitness += 1
                    #print ("Add fitness")
                break
    #print (fitness) 
    return fitness


        
#>>>>>>>>>>MAIN PROGRAM LOOP<<<<<<<<<<
for gen in range(0,generations):
    
    fittest = 0
    averagefitness = 0
    totalfitness = 0
    
    #PARENT
    parentFunc()
    
    #MUTATION
    mutationFunc()        

    #FITNESS
    for i in range (0,P):
        offspring[i].fitness = fitFunc(i)
        #print (offspring[i].fitness)
        #print (offspring[i].gene)
     
    #Make offspring   
    for i in range(0,P):
        population[i] = offspring[i]
    for i in range(0,P):
        totalfitness = totalfitness + offspring[i].fitness
        if (offspring[i].fitness >= fittest):
            fittest = offspring[i].fitness
        averagefitness = totalfitness/P

    print(averagefitness )
    
    



           
    
    
