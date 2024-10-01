import random

#   EXAMPLE WITH 4 NODES
# ab = ['AB',['BC','BD'],8,1]
# ac = ['AC',['BC','BD'],14,1]
# ad = ['AD',[],22,1]
# bc = ['BC',['CD'],7,1]
# cb = ['CB',['BD'],9,1]
# bd = ['BD',[],8,1]
# cd = ['CD',[],10,1]
# edges = [ab,ac,ad,bc,cb,bd,cd]

#   EXAMPLE WITH 5 NODES
ab = ['AB',['BD','BE','BC'],5,1]
bc = ['BC',['CD','CE'],11,1]
ac = ['AC',['CB','CD','CE'],6,1]
cb = ['CB',['BD','BE'],11,1]
ae = ['AE',[],30,1]
cd = ['CD',['DE'],17,1]
bd = ['BD',['DC','DE'],6,1]
ce = ['CE',[],10,1]
be = ['BE',[],16,1]
de = ['DE',[],4,1]
dc = ['DC',['CE'],17,1]
edges = [ab,bc,ac,cb,ae,cd,bd,ce,be,de,dc]


def probabilities(adjucent_edges):
  distants = []
  pheromone = []
  for i in adjucent_edges:
    for j in edges:
      if j[0] == i:
        distants.append(j[2])
        pheromone.append(j[3])

  attractivities = []
  count = 0
  while count < len(adjucent_edges):
    atract = pheromone[count]*(1/(distants[count]))
    attractivities.append(atract)
    count += 1

  summ = sum(attractivities)
  probabilities = []
  for i in attractivities:
    prob = (i/summ)
    probabilities.append(prob)

  return probabilities


def chooseEdges(adjucent_edges):
  probab = probabilities(adjucent_edges)
  thresholds = []
  summ = 0
  for i in probab:
    summ += i
    thresholds.append(summ)
  r = random.random()
  count = 0
  for i in thresholds:
    if r > i:
      count += 1
  return adjucent_edges[count]


def ant():
  starters = [ab,ac,ae]
  path = []

  starter = chooseEdges(['AB','AC','AE'])
  path.append(starter)

  if 'E' in path[-1]:
    return path
  else:
    while True:
      for i in edges:
        if path[-1] == i[0]:
          adj = i[1]
          if len(adj)==0:
            break
          else:
            adj_random = chooseEdges(adj)
            path.append(adj_random)
      return path
      break


def length(ant):
  summ = 0
  for i in ant:
    for j in edges:
      if i == j[0]:
        summ += j[2]
  return summ

#Pheromone evaporation

def evaporation(evap):
  for i in edges:
    i[3] = i[3]*(1-evap)

#Pheromone Update

def update_pherom(ants):
  for i in ants:
    pherom = 1/(length(i))
    for j in i:
      for k in edges:
        if k[0] == j:
          k[3] = k[3] + pherom



#   TEST probabilities function
# print ( probabilities(['AB', 'AC', 'AD']) )

#   TEST chooseEdges function
# print( chooseEdges(['AB','AC','AD']) )

#   TEST ant function
# print( ant() )

#   TEST edges  weights
# for i in edges:
#   print(i)

#   TEST multiple ants , evaporated edges and print edges  weights
# ants= [['AB', 'BD'], ['AD']]
# update_pherom(ants)

# for i in edges:
#   print(i)


#Running the algorithm

for i in range(15):
  evaporation(0.3)
  ants = []
  for j in range(5):
    ants.append(ant())
  update_pherom(ants)


#   we can notice the more 'weighted' route - the more pheromone the better
for i in edges:
  print(i[0],i[3])

for k in ants:
  print(k)

