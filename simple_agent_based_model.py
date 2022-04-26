import numpy as np
from math import ceil
from matplotlib import pyplot as plt

class abm:
    def __init__(self, nPop, inf0, TransmProb, meeting_ave):
        self.nPop = nPop                # population size
        self.inf0 = inf0                # number of infected agents at time 0
        self.TransmProb = TransmProb    # transmission probability
        self.meeting_ave = meeting_ave  # average number of meetings per day   
        self.time = 0                   # define time variable
        self.susc = []                  # define susceptible agents       
        self.exp = []                   # define exposed agents
        self.inf = []                   # define infected agents
        self.rec = []                   # define recovered agents
        self.asy = []                   # define asymptomatic agents
        self.sym = []                   # define symptomatic agents

    def start_inf(self, i):             # function to infect inf0 individuals at time 0
        self.states[i] = 2
        self.infectiousLen[i] = 0  
        self.infectiousTime[i] = ceil(np.random.lognormal(1.501524205, 0.07145896398))
 
    def infInit(self):                  # function to randomly select time 0 infected individuals
        infs = np.random.randint(0, self.nPop, self.inf0)
        for i in infs:
            self.start_inf(i)

    def create_pop(self):              # function to create population
        self.id = [i for i in range(self.nPop)]                 # define IDs
        self.states = [0 for i in range(self.nPop)]             # define states
        self.latencyTime = [-1 for i in range(self.nPop)]       # define times exposed
        self.infectiousTime = [-1 for i in range(self.nPop)]    # define times infectious
        self.latencyLen = [-1 for i in range(self.nPop)]        # define latency lengths
        self.infectiousLen = [-1 for i in range(self.nPop)]     # deifne infectious lengths
        self.mixersAvi = [ [x for x in range(self.nPop) if x != i] for i in range(self.nPop) ]      # define vectors of available agents 
        self.infInit()
                  

    def infected(self, i):             # function to infect agents at end of day and assign latency/infectious times
        self.states[i] = 1
        self.latencyTime[i] = ceil(np.random.lognormal(1.501524205, 0.07145896398))
        self.infectiousTime[i] = ceil(np.random.lognormal(2.064055712, 0.1754185243))
        self.latencyLen[i] = 0

    def iteration(self):            # function to simulate a day in the model
        new_inf = []                # define list of new infections on day
        for i in range(self.nPop):
            if self.states[i] == 2 and self.infectiousLen[i] == self.infectiousTime[i]:         # move agents at end of infectious period to recovered
                self.states[i] = 3
                self.infectiousLen[i] = -1
            if self.states[i] == 1 and self.latencyLen[i] == self.latencyTime[i]:               # move agents at end of latency period to infectious
                self.states[i] = 2
                self.infectiousLen[i] = 0
                self.latencyLen[i] = -1
            meeting_no = np.random.poisson(self.meeting_ave)             # determine number of meetings for agent   
            meetings = np.random.choice(self.mixersAvi[i], meeting_no)   # determine who agent meets
            for j in range(len(meetings)):                               # meetings occur
                if self.states[meetings[j]] == 2 and self.states[i] == 0:
                    outcome = np.random.rand()      # determines whether infection occurs
                    if outcome < self.TransmProb:
                        new_inf.append(i)
            if self.states[i] == 1:         # update latency length
                self.latencyLen[i] += 1
            elif self.states[i] == 2:       # update infectious length
                self.infectiousLen[i] += 1
        for k in new_inf:           # update infections
            self.infected(k)
        self.time += 1              # update time

    def summary(self):      # output summary data
        a = [self.states[x] for x in range(self.nPop) if self.states[x] == 0]
        b = [self.states[x] for x in range(self.nPop) if self.states[x] == 1]
        c = [self.states[x] for x in range(self.nPop) if self.states[x] == 2]
        d = [self.states[x] for x in range(self.nPop) if self.states[x] == 3]
        return [len(a), len(b), len(c), len(d)]

    def run(self, n):       # run model for n days
        for i in range(n):
            self.iteration()
            sum = self.summary()
            self.susc.append(sum[0])
            self.exp.append(sum[1])
            self.inf.append(sum[2])
            self.rec.append(sum[3])
            if i % 10 == 0:
                print(self.summary())

# initial parameters
nPop = 500
inf0 = 1
TransmProb = 0.016 
meeting_ave = 20

days = 100

model = abm(nPop, inf0, TransmProb, meeting_ave)
model.create_pop()
model.run(days)

times = [i for i in range(days)]

suscs = [sum(model.susc[i] for i in range(j, j+7))/7 for j in range(len(model.susc) - 7)]
exps = [sum(model.exp[i] for i in range(j, j+7))/7 for j in range(len(model.exp) - 7)]
infs = [sum(model.inf[i] for i in range(j, j+7))/7 for j in range(len(model.inf) - 7)]
recs = [sum(model.rec[i] for i in range(j, j+7))/7 for j in range(len(model.rec) - 7)]

times2 = [i +7 for i in range(days - 7)]

plt.plot(times, model.susc, linestyle='-', label="Susceptible")
plt.plot(times, model.exp, linestyle='-', label="Exposed")
plt.plot(times, model.inf, linestyle='-', label="Infected")
plt.plot(times, model.rec, linestyle='-', label="Recovered")
plt.legend(loc="upper left")

"""
#plt.plot(times2, suscs, linestyle='-', label="Susceptible")
#plt.plot(times2, exps, linestyle='-', label="Exposed")
#plt.plot(times2, infs, linestyle='-', label="Infected")
#plt.plot(times2, asymps, linestyle='-', label="Asymptomatic")
#plt.plot(times2, symps, linestyle='-', label="Symptomatic")
#plt.plot(times2, recs, linestyle='-', label="Recovered")

"""

plt.ylabel("Number of infections")
plt.xlabel("Time (days)")

plt.show()
