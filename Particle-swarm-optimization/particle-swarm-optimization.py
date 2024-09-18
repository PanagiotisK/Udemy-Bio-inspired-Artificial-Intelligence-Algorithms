import random
import numpy as np
import matplotlib.pyplot as plt

w = 0.8
c1 = 0.5
c2 = 0.5

def particle():
    while True:
        particle = []
        pos1 = []
        pos2 = []
        for i in range(6):
            rand1 = random.randint(0,3) + random.random()
            rand2 = random.randint(0,3) + random.random()
            pos1.append(rand1)
            pos2.append(rand2)
        vel = [0,0,0,0,0,0]
        particle.append(pos1)
        particle.append(pos2)
        particle.append(vel)
        if sum(particle[0]) <= 13 and sum(particle[1]) <= 13:
            return particle
            break

def population(quant):
    particles = []
    for i in range(quant):
        particles.append(particle())
    return particles

def evaluate(particle, indice):
    class1 = [3,2,1,2,4,2.5]
    class2 = [1,4,0,2,4,1.4]
    class3 = [1.5,2.5,1,2,3.5,1.5]
    classes = [class1, class2, class3]

    if sum(particle[indice]) <= 13:
        _sum = 0
        for _class in classes:
            count = 0
            while count < len(particle[indice]):
                double = [particle[indice][count], _class[count]]
                minimum = min(double)
                _sum += minimum
                count += 1
        return _sum/39
    else:
        return 0.01
    
def personalbest(particle):
    values = []
    count = 0
    while count < 2:
        if count == 0:
            best = particle[0]
        elif count == 1:
            if evaluate(particle,count) > evaluate(particle,0):
                best = particle[1]
        count += 1
    return best


def evaluate_simple(particle):
    class1 = [3,2,1,2,4,2.5]
    class2 = [1,4,0,2,4,1.4]
    class3 = [1.5,2.5,1,2,3.5,1.5]
    classes = [class1, class2, class3]

    if sum(particle) <= 13:
        _sum = 0
        for _class in classes:
            count = 0
            while count < len(particle):
                double = [particle[count], _class[count]]
                minimum = min(double)
                _sum += minimum
                count += 1
        return _sum/39
    else:
        return 0.01

def globalbest(population_generated):
    pbests = []
    for i in population_generated:
        pbests.append(list(personalbest(i)))
    
    for indice in pbests:
        if pbests.index(indice) == 0:
            gbest = pbests[0]
        else:
            if evaluate_simple(indice) > evaluate_simple(gbest):
                gbest = indice
    
    return gbest

def new_velocity(particle, population):
    r1 = random.random()
    r2 = random.random()
    vel = particle[2]

    new_v = w*np.array(vel) + c1*r1*(np.array(personalbest(particle) - np.array(particle[1]))) + c2*r2*(np.array(globalbest(population) )- np.array(particle[1]))
    return new_v

def new_position(particle, population):
    new_vel = new_velocity(particle, population)
    new_pos = particle[1] + new_vel
    return new_pos

def new_particle(particle, population):
    new_p = [np.array(particle[0]), new_position(particle, population), new_velocity(particle, population)]
    return new_p

#   TEST personalbest function
# p = particle()
# print(p[0])
# print(p[1])
# print(evaluate(p,0))
# print(evaluate(p,1))
# print(personalbest(p))

#   TEST globalbest function
# pop = population(5)
# best = globalbest(pop)
# print(best)
# print(evaluate_simple(best))

trial_population = population(20)
graph = []

for i in range(100):
    best = globalbest(trial_population)
    new_trial_population = []
    for j in trial_population:
        new_part = new_particle(j,trial_population)
        new_trial_population.append(new_part)
    trial_population = new_trial_population
    graph.append(evaluate_simple(best))

    print(f'Best solution of the population : {best}')
    print(f'Fitness value of the solution   : {evaluate_simple(best)}')
    print(sum(best))
    print()

plt.plot(graph)
plt.title('Course use / Fitness value')
plt.show()