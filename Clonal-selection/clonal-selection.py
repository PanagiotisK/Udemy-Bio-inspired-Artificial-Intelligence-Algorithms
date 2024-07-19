'''
Clonal selection algorithms are inspired by the vertebrate immune system

    Clonal selection algorithm
    Negative selection algorithm
    Algorithms based on immune cell networks
    Dendritic cell algorithms

Similar to Darwinian evolution.

Main application
    Classification
    Pattern detection
    Anomaly detection
    Information-Cyber security
    Optimization for mathematical functions

1. Generation of antibody population
2. Selection of antibodies with most affinity
3. Cloning the most promising antibodies
4. Hypermutation of antibodies according to affinity

Generation of antibody population
Set fitness function
For each i of 1 to num
    For each antibody
        Calculate fitness
    Select n-best antibodies
    For each j of 1 to n-best
        Perform cloning proportionally to affinity
        Perform hyper-mutation inversely proportional to affinity

DIGIT RECOGNITION ( pattern recognition )
    digit 8 drawn in a 11x11 matrix        

'''

import random
import numpy as np
import matplotlib.pyplot as plt


number = [  0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,1,1,1,1,1,0,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,0,1,1,1,1,1,0,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,1,0,0,0,0,0,1,0,0,
            0,0,0,1,1,1,1,1,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0] #antigen

def antibody():
    positions = []
    for i in range(121):
        positions.append(random.randint(0,1))
    return positions

def population(quant):
    population = []
    for i in range(quant):
        population.append(antibody())
    return population

def affinity(antibody,antigen):
    score = 0
    count = 0
    while count < len(antibody):
        if antibody[count] == antigen[count]:
            score += 1
        count += 1
    return score

def affin_antibodies(pop_antibodies):
    affin_antibodies = []
    for i in pop_antibodies:
        afin_antibody = []
        afin_antibody.append(affinity(i,number))
        afin_antibody.append(i)
        affin_antibodies.append(afin_antibody)
    return affin_antibodies

def selec(affinity,numberAB):
    sortted = sorted(affinity)
    reverse = sortted[::-1]
    bests = reverse[:numberAB]
    return bests

def cloning(cloning,bests):
    
    # bests [affinity, [gene]]
    # clones matrix will have the same design as bests. 
    # X amount of copies of bests[0]
    # Y amount of copies of bests[1] etc...
    # X,Y etc are calculated and saved in clonings variable

    clones = []
    affinities = [x[0] for x in bests]
    summ = sum(affinities)
    anti = [x[1] for x in bests]
    # amount of clones for each best element. the better its affinity the more clonings
    clonings = [round((c/summ)*cloning) for c in affinities]

    count = 0
    while count < len(clonings):
        for i in range(clonings[count]):
            double = []
            double.append(affinities[count])
            double.append(anti[count])
            clones.append(double)
        count += 1
    return clones

def hypermutation(clones,factor):
    hypermutated = []
    clones = [x[1] for x in clones]
    for i in clones:
        aff = affinity(i,number)
        hypRate = (1-(aff/121))*factor
        hyperm = []
        for j in i:
            rand = random.random()
            if rand <= hypRate:
                if j == 0:
                    hyperm.append(1)
                if j == 1:
                    hyperm.append(0)
            else:
                hyperm.append(j)
        hypermutated.append(hyperm)
    return hypermutated

#====   TEST 01 BEGIN   ====#

# pop = population(20)
# afin = affin_antibodies(pop)
# sel = selec(afin,5)
# for i in sel:
#     print(i)

# print()

# for i in afin:
#     print(i)

#====   TEST 01 END     ====#

#====   TEST 02 BEGIN   ====#

# pop = population(20)
# afin = affin_antibodies(pop)
# sel = selec(afin,3)
# cloned = cloning(17,sel)

# for i in cloned:
#   print(i[1])

# print()

# for i in afin:
#   print(i)

# print(len(cloned))

#====   TEST 02 END     ====#

pop = population(30)
firsts = []

for i in range(100):
    affins = affin_antibodies(pop)
    bests = selec(affins,4)
    clon = cloning(25,bests)
    hipermut = hypermutation(clon,0.1)
    nNews = len(pop) - len(hipermut)
    for i in range(nNews):
        hipermut.append(antibody())
    pop = hipermut
    print(pop[0])
    print(affinity(pop[0],number))
    firsts.append(affinity(pop[0],number))
    print()

    picture = pop[0]
    array_image = []
    init = 0
    end = 11
    while end < (len(picture)-1):
        array = picture[init:end]
        array_image.append(array)
        init += 11
        end += 11

    image = np.array(array_image)
    # Comment out to show the number pattern be created progressively
    # fig,ax = plt.subplots()
    # im = ax.imshow(image)
    # ax.set_title('Number')
    # fig.tight_layout()
    # plt.show()

plt.plot(firsts)
plt.title('Affinity (x/121)')
plt.show()