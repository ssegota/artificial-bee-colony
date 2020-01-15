import numpy as np
from random import uniform

#mock solution space
print("start memory allocation")
area = np.random.rand(500,500,500)
print("memory allocation done")



def roulleteWheel(swarm):
    max = sum([b.nectarAmount for b in swarm])
    pick = uniform(0,max)
    current = 0
    for b in swarm:
        current += b.nectarAmount
        if current > pick:
            return b


class Bee():
    cycles=0
    cycleLimit = 50
    beeType = None
    dimensions = None
    nectarAmount = 0
    position = []
    search_area = []
    
    
    history = []
    ExtraElitist=True
    
    def calculateNectarAmount(self, position=None):
        if position==None:
            position=self.position

        return self.search_area[tuple(position)]

    def __init__(self, search_area, beeType='employeed'):
        self.beeType = beeType
        number_of_dims = search_area.ndim
        self.dimensions = search_area.shape
        randomBeePosition = []
        #get radnom positions of a bee
        for d in self.dimensions:
            randomBeePosition.append(np.random.randint(d))
        self.position = list(randomBeePosition)
        self.search_area = search_area
        self.nectarAmount = self.calculateNectarAmount()
        
        
    def setType(self, beeType):
        self.beeType=beeType
    

    def updateCycles(self, reset=False):
        if reset:
            cycles=0
            return
        self.cycles+=1
    
    def look(self, population):
        b = roulleteWheel(population)
        if b.nectarAmount > self.nectarAmount:
            self.position = b.position
            self.nectarAmount = self.calculateNectarAmount()
        return
    
    def scoutArea(self):#, population):
        
        new_position = []
        phi = uniform(0,1)
        
        scoutedPosition = []
        for d in self.dimensions:
            scoutedPosition.append(int(phi*d))
        if (self.ExtraElitist) and (self.calculateNectarAmount()>self.nectarAmount):
            self.position = list(scoutedPosition)
            self.nectarAmount=self.calculateNectarAmount()
        return
    def dance(self):
        #generate new solution
        phi = uniform(-1,1)
        #select a random candidate
        randomCandidatePosition = []
        #get radnom positions of a bee
        for d in self.dimensions:
            randomCandidatePosition.append(np.random.randint(d))
            
        candidateSolution = []
        for p,d,max_ in zip(self.position, randomCandidatePosition,self.dimensions):
            v = int(p+phi*(p)*(p-d))
            if v<0:
                v=0
            elif v>(max_-1): #remove hardcode
                v=max_-1
            candidateSolution.append(v)
        #get nectar amount
        candidateNectarAmount = self.calculateNectarAmount(position=candidateSolution)
        #candidateNectarAmount = self.search_area[tuple(candidateSolution)]
        if candidateNectarAmount>self.nectarAmount:
            self.nectarAmount = candidateNectarAmount
            self.position = list(candidateSolution)
            
        self.history.append(self.nectarAmount)
        #print(self.position, self.nectarAmount)
        
    def shouldScout(self):
        #print(self.cycles)
        if self.cycles>200:         
            if np.average(self.history[-50:])==self.history[-1:]:
                #print("SCOUTS")
                return True
        return False
    
    def giveNectar(self):
        return (self.position, self.nectarAmount)
        
#initialize bees            
Swarm = []
swarmSize=5
best = []

for i in range(swarmSize):
    print(i)
    Swarm.append(Bee(area))
    
#start
bestSolutions = []
from matplotlib import pyplot as plt
for i in range(1000):

    nectarAmounts = []
    for b in Swarm:

        nectarAmounts.append(b.giveNectar())

    
    bestSolutions.append(sorted(nectarAmounts, key=lambda x: x[1], reverse=True)[0])
        
    for b in Swarm:
        b.dance()
        b.look(Swarm)
        b.updateCycles()
        if b.shouldScout():
            b.scoutArea()
        

#print(bestSolutions.shape())
plt.figure()
plt.plot([x[1] for x in bestSolutions])
plt.show()


