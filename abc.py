import numpy as np
from random import uniform

#mock solution space
print("start memory allocation")
area = np.random.rand(2000,2000)
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
                v=abs(v)%max_
            elif v>(max_-1): #remove hardcode
                v=v%max_
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
        if self.cycles>self.cycleLimit:         
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
Runs = 1000
minimalRuns = 500
maximumRunsWithoutChange = 300
saveImgs = False
for i in range(swarmSize):
    Swarm.append(Bee(area))
    
#start
bestSolutions = []
from matplotlib import pyplot as plt
for i in range(Runs):

    nectarAmounts = []
    for b in Swarm:
        nectarAmounts.append(b.giveNectar())
    
    pltarea = area.copy()
    if saveImgs:
        print(i,50*"-")
        
        plt.figure()
        plt.title("Artificial Bee Colony\n"+"Swarm Size = "+str(swarmSize)+", Run = "+str(i))
        plt.imshow(pltarea)
        for n in nectarAmounts:
            plt.plot(n[0][0], n[0][1], "or")
        #plt.show()
        plt.savefig(str(i)+".png")
        plt.close()

    
    bestSolutions.append(sorted(nectarAmounts, key=lambda x: x[1], reverse=True)[0])
    #print(len(bestSolutions))
   
    
    if len(bestSolutions) > minimalRuns and round(np.average([x[1] for x in bestSolutions][-maximumRunsWithoutChange:]),5) == round(bestSolutions[-1][1],5):
        print("End condition satisfied at", len(bestSolutions))
        break
    for b in Swarm:
        b.dance()
        b.look(Swarm)
        b.updateCycles()
        if b.shouldScout():
            b.scoutArea()
    
    
print("Best possible solution", np.max(area))
print("Best Solution Found: ", bestSolutions[-1])
#print(bestSolutions.shape())
plt.figure()
plt.plot([x[1] for x in bestSolutions])
plt.show()


