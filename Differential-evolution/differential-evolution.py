'''
1. RANDOM GENERATION OF SOLUTION
2. FOR EACH VECTOR -> CHOOSE OTHER THREE
3. GENERATE A TRIAL VECTOR FROM VECTOR A
4. IF THE TRIAL VECTOR HAS BETTER FITNESS THAN THE PARENTAL VECTOR -> REPLACE TEH PARENT

Set Hyperparameters
NP = population size
CR = mutation/crossover propability
F  = differential weight

Initialize the population of solution vectors

For each number of 1 to num
    For each solution vector X in the NP
        Create an updated emptyvector X+1
            Choose three other vectors A,B,C different from each other and different from X
            For each index Xi in X
                Generate random value R from 0 to 1
                if R < CR
                    X+1i = ai + F*(bi-c1)
                if R > CR
                    X+1i = Xi
            If fitness value of X+1 >= fitness value of X
                replace X with X+1 in the population

                
Nutrient Allocation Problem

Suppose in a given meal,
a 500g meal should contain 
30% protein, 15% fat and 55% carbohydrates

Food options
    Chicken breast      = 23g protein   + 5g fat    + 5g carbohydrates
    Sweet potato        = 2g protein    + 0g fat    + 24g carbohydrates
    Brown rice          = 2.6g protein  + 1g fat    + 26g carbohydrates
    Egg                 = 13g protein   + 8.9g fat  + 1.5g carbohydrates
    Beans               = 9.5g protein  + 1.4g fat  + 29g carbohydrates

'''

import random
import matplotlib.pyplot as plt

CR = 0.5
F = 0.8

def combination():
    items = []
    for i in range(5):
        quant = random.randint(0,199) + random.random()
        items.append(quant)
    return(items)

def population(num):
    pop = []
    for i in range(num):
        pop.append(combination())
    return pop

def divergence(dish, show=False):
    carbs = dish[0]*0.05 + dish[1]*0.24 + dish[2]*0.26 + dish[3]*0.15 + dish[4]*0.29
    prots = dish[0]*0.23 + dish[1]*0.02 + dish[2]*0.026 + dish[3]*0.13 + dish[4]*0.095
    lips  = dish[0]*0.05 + dish[1]*0 + dish[2]*0.01 + dish[3]*0.089 + dish[4]*0.014

    total = carbs + prots + lips
    summ = sum(dish)

    porcCarbs = (carbs/total)*100
    porcProts = (prots/total)*100
    porcLips  = (lips/total)*100

    difCarb = abs(porcCarbs - 55)   # 55% of the final dish will be Carbs
    difProt = abs(porcProts - 30)   # 30% of the final dish will be Protein
    difLip  = abs(porcLips - 15)    # 15% of the final dish will be Lips

    if show:
        print(f'Carbs    : {porcCarbs}')
        print(f'Proteins : {porcProts}')
        print(f'Lipids   : {porcLips}')
        print(f'Total of grams : {summ}')
        print(dish)
    
    totalDif = difCarb + difProt + difLip
    if show:
        print(totalDif)

    return totalDif

def select3(parental, population):
    p2=[]
    three_vectors=[]
    for v in population:
        if parental != v :
            p2.append(v)
    for j in range(3):
        rand = random.choice(p2)
        three_vectors.append(rand)
        p2.remove(rand)
    return three_vectors

def mutation(parentalVector, three):
    count=0
    A = three[0]
    B = three[1]
    C = three[2]

    trial = []

    while count < len(parentalVector):
        R = random.random()
        if R < CR:
            X = A[count] + F*abs(B[count] - C[count])
            trial.append(X)
        else:
            trial.append(parentalVector[count])
        count+=1
    
    return trial

def bestVector(pop):
    scores=[]
    for i in pop:
        scores.append(divergence(i))
    indice = scores.index(min(scores))
    return pop[indice]


def regulateDish(dish):
    scale = 500/sum(dish)
    for i in range(len(dish)):
        dish[i] *= scale
    print(dish)
    print(f'Updated Total of grams : {sum(dish)}')

popGenOne = population(5)
bests = []


for i in range(150):
    for j in popGenOne:
        tri = select3(j, popGenOne)
        trial = mutation(j,tri)
        if divergence(trial) < divergence(j):
            popGenOne.remove(j)
            popGenOne.append(trial)
        bests.append(divergence(bestVector(popGenOne)))
        # print(f'Best Vector     : {bestVector(popGenOne)}')
        # print(f'Fitness value   : {divergence(bestVector(popGenOne))}')
        # print()

plt.plot(bests)
plt.xlabel('Iterations')
plt.ylabel('Fitness Value')
plt.title('Divergence Value')
# plt.show()

print()
divergence(bestVector(popGenOne), False)

print('Regulated dish amounts to be a total of 500g')
regulateDish(bestVector(popGenOne))
print()