import time
import sys
import random
import math

def get_minutes(hour):
    t = time.strptime(hour, '%H:%M')
    minutes = t[3]*60 + t[4]
    return minutes

def print_schedule(schedule):
    flight_id = -1
    flight_price = 0
    total_price = 0
    for i in range(len(schedule) // 2):
        name = people[i][0]     # full name of airport
        fromLocation = people[i][1]   # abriviation name of airport
        flight_id += 1
        going = flights[(fromLocation, destination)][schedule[flight_id]]
        # print('First flight : ' + str(going)) # TypeError: can only concatenate str (not "tuple") to str
        total_price += going[2]
        flight_id += 1
        returning = flights[(destination, fromLocation)][schedule[flight_id]]
        total_price += returning[2]
        # print('Returning flight : ' + str(returning)) # TypeError: can only concatenate str (not "tuple") to str
        print('%10s%10s   %5s-%5s  U$%3s   %5s-%5s  U$%3s' % (name, fromLocation, going[0], going[1], going[2], returning[0], returning[1], returning[2]))
    print('\nTotal price %8s' % (total_price))


# for this use case we will create a fitness function regarding the wait time at the airport
def fitness_function(schedule):
    total_price = 0
    last_arrival = 0        # get_minutes('00:00')
    first_departure = 1439  # get_minutes('23:59')

    total_wait = 0

    flight_id = -1
    for i in range(len(schedule) // 2):
        fromLocation = people[i][1]
        flight_id += 1
        going = flights[(fromLocation, destination)][schedule[flight_id]]
        flight_id += 1
        returning = flights[(destination, fromLocation)][schedule[flight_id]]
        total_price += going[2]
        total_price += returning[2]

        if last_arrival < get_minutes(going[1]):
            last_arrival = get_minutes(going[1])
        if first_departure > get_minutes(returning[1]):
            first_departure = get_minutes(returning[1])
    
    flight_id = -1
    for i in range(len(schedule) // 2):
        fromLocation = people[i][1]
        flight_id += 1
        going = flights[(fromLocation, destination)][schedule[flight_id]]
        flight_id += 1
        returning = flights[(destination, fromLocation)][schedule[flight_id]]
        total_wait += last_arrival - get_minutes(going[1])
        total_wait += get_minutes(returning[0]) - first_departure
    
    # print(last_arrival)
    # print(first_departure)
    # print(total_price)
    # print('Total wait %9s' % (str(total_wait)))

    # print('\nTotal weight %7s\n' % str(total_price + total_wait))
    return(total_price + total_wait)

def mutation(domain, schedule, probability):
    # print('\n\nMUTATION')
    gene = random.randint(0,len(domain) - 1)
    # print('Gene randomly selected : ' + str(gene))
    mutant = schedule
    if random.random() < probability :
        if schedule[gene] != domain[gene][0] :
            mutant = schedule[0:gene] + [schedule[gene] - 1] + schedule[gene+1:]
        else:
            if schedule[gene] != domain[gene][1]:
                mutant = schedule[0:gene] + [schedule[gene] + 1] + schedule[gene+1:]
    # print(mutant)
    return mutant

def crossover(domain, individual1, individual2):
    # print('\n\nCROSSOVER')
    gene = random.randint(1,len(domain) - 2)
    # print(str(individual1[0:gene] + individual2[gene:]))
    return individual1[0:gene] + individual2[gene:]

'''
    for the genetic algorithm we can break the implementation into smaller parts

        1. Create initial population (individuals, chromosomes, genes)
        2. Evaluate population ( calculate the score or weight of each population group )
        3. Check the stopping criterion
            3.A. Select parents
            3.B. CrossOver
            3.C. Mutation
            3.D. Evaluate population
            3.E. Define surviving population
        4. List best individuals
'''
def genetic_algorithm(domain, fitness_function, population_size=100, elitism=0.2, number_of_generations=500, mutation_propability=0.05):

    number_elitism = int(elitism * population_size)

#   1. CREATE POPULATION
    population = []
    for i in range(population_size):
        individual = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        population.append(individual)
    # print(population)

    #============   2. EVALUATE POPULATION  ============#
    for i in range(number_of_generations):
        score = [(fitness_function(individual), individual) for individual in population]
        # print(score)
        score.sort()
        ordered_individuals = [individual for (score, individual) in score]
        # print(ordered_individuals)
        #============   3.A. SELECT PARENTS ============#
        population = ordered_individuals[0:number_elitism]
        #============   3.B. CROSSOVER      ============#
        while(len(population) < population_size):
            i1 = random.randint(0, number_elitism)
            i2 = random.randint(0, number_elitism)
            # print(i1, i2, ordered_individuals[i1], ordered_individuals[i2])
            new_individual_crossover = crossover(domain, ordered_individuals[i1] , ordered_individuals[i2])
            # print(new_individual_crossover)
            #============   3.C. MUTATION   ============#
            new_individual_mutation = mutation(domain, new_individual_crossover, mutation_propability)
            # print(new_individual_mutation)
            population.append(new_individual_mutation)

    return score[0][1]




people = [('Lisbon', 'LIS'),
          ('Madrid', 'MAD'),
          ('Paris', 'CDG'),
          ('Dublin', 'DUB'),
          ('Brussels', 'BRU'),
          ('London', 'LHR')]

destination = 'FCO' # Rome

flights= {}
for row in open('Genetic-algorithms/flights.txt'):
    fromLocation, toLocation, departure, arrival, price = row.split(',')
    flights.setdefault((fromLocation, toLocation), [])
    flights[(fromLocation, toLocation)].append((departure, arrival, int(price)))
    
# print(flights['FCO', 'LIS'])

# TEST


'''
in print_schedule we send an array , 
and every two elements re grouped in way
that shows the TO and FROM each city.
Now we have 6 cities (LIS, MAD, CDG, DUB, BRU, LHR), 
so in order to cover all flights,
we must have 12 elements in the array.

print_schedule([    LIS->FCO[i]  , FCO->LIS[i]  ,  
                    MAD->FCO[i]  , FCO->MAD[i]  ,  
                    CDG->FCO[i]  , FCO->CDG[i]  ,  
                    DUB->FCO[i]  , FCO->DUB[i]  ,
                    BRU->FCO[i]  , FCO->BRU[i]  ,
                    LHR->FCO[i]  , FCO->LHR[i] 
                ]) 

data preparation is needed in order to know the amount of each from-to combination ,
and now we have 10 flights per day between 2 cities, so the values (i) for each element is between 0-9
'''
# print_schedule([1,4, 3,1, 8,3, 6,3, 2,4, 5,3])
# fitness_function([1,4, 3,1, 8,3, 6,3, 2,4, 5,3])
# print_schedule([1,1, 1,1, 7,3])
# fitness_function([1,4, 3,2, 7,3])

domain = [(0,9)] * (len(people) * 2)

# TEST
# for _ in range(10): 
#     mutation(domain, [6, 7, 6, 7, 3, 9, 7, 7, 0, 7, 6, 7], 0.9)

# TEST
# s1 = [1,4 , 3,2 , 7,3 , 6,3 , 2,4 , 5,3]
# s2 = [0,1 , 2,5 , 8,9 , 2,3 , 5,1 , 0,6]
# for _ in range(10):
#     crossover(domain, s1, s2)

solution = genetic_algorithm(domain, fitness_function, 350, 0.2, 500, 0.95)
print('\n')
print('Best solution : ' + str(solution) + ' with score : ' + str(fitness_function(solution)))
print('\n')
print_schedule(solution)