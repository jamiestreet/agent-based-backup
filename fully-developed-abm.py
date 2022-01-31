from workplaces import workplaces
import numpy as np
from math import ceil, cos, sin, pi
from matplotlib import pyplot as plt
from households import households
import time

class abmHouseholds:
    def __init__(self, nPop, inf0, ageDist, household_dist, workplace_dist, TransmProb, severities, meeting_ave, work_meeting_ave, social_distancing=-1, eff_SocialD=1, lockdown_date=-1, eff_Lockdown=1, isolation_date=-1, isolationLen=10, testing_date=-1, testProb = 1):
        self.nPop = nPop
        self.inf0 = inf0
        self.ageDist = ageDist
        self.household_dist = household_dist
        self.workplace_dist = workplace_dist
        self.TransmProbHouse = TransmProb
        self.TransmProb = TransmProb
        self.severities = severities
        self.meeting_ave = meeting_ave
        self.work_meeting_ave = work_meeting_ave
        self.time = 0
        self.susc = []
        self.exp = []
        self.inf = []
        self.rec = []
        self.asy = []
        self.sym = []
        self.all_meetings = []
        self.social_distancing = social_distancing
        self.eff_SocialD = eff_SocialD
        self.lockdown_date = lockdown_date
        self.eff_Lockdown = eff_Lockdown
        self.isolationRule = False
        self.isolation_date = isolation_date
        self.isolationLen = isolationLen
        self.testing_date = testing_date
        self.testProb = testProb
        self.testingOn = False
        self.infection_tracker = []

    def start_inf(self, i):
        self.states[i] = 2
        self.infectiousLen[i] = 0  
        sym = np.random.rand()
        if sym > self.severities[self.ageGroup[i]]:
            self.infectionType[i] = 1
            self.infectiousTime[i] = ceil(np.random.lognormal(1.501524205, 0.07145896398))
        else:
            self.infectionType[i] = 2
            self.infectiousTime[i] = ceil(np.random.lognormal(-0.1827236141, 0.7456993951) + np.random.lognormal(2.064055712, 0.1754185243))

    def infInit(self):
        infs = np.random.randint(0, self.nPop, self.inf0)
        for i in infs:
            self.start_inf(i)

    def setHouseholds(self):
        householdsN = households(self.household_dist, self.ages, self.id)
        self.households = householdsN.household_sort()
        self.household_no = [0 for i in range(self.nPop)]
        for i in range(len(self.households)):
            for j in self.households[i]:
                self.household_no[j] = i

    def setWorkplaces(self):
        workplacesN = workplaces(self.workplace_dist, self.ages, self.id)
        self.workplaces = workplacesN.workplace_sort()
        self.workplace_no = [0 for i in range(self.nPop)]
        for i in range(len(self.workplaces)):
            for j in self.workplaces[i]:
                self.workplace_no[j] = i

    def create_pop(self):
        self.id = [i for i in range(self.nPop)]
        age = [10*i for i in range(10)]
        ages1 = np.random.choice(age, self.nPop, p=self.ageDist)
        self.ages = [np.random.choice([ages1[i] + j for j in range(10)]) for i in range(self.nPop)]
        self.setHouseholds()
        self.setWorkplaces()
        self.ageGroup = [self.ages[i] // 10 for i in range(self.nPop)]
        self.states = [0 for i in range(self.nPop)]
        self.latencyTime = [-1 for i in range(self.nPop)]
        self.infectiousTime = [-1 for i in range(self.nPop)]
        self.preSympTime = [-1 for i in range(self.nPop)]
        self.infectionType = [-1 for i in range(self.nPop)]
        self.latencyLen = [-1 for i in range(self.nPop)]
        self.preSympLen = [-1 for i in range(self.nPop)]
        self.infectiousLen = [-1 for i in range(self.nPop)]
        self.mixersAvi = [ [x for x in range(self.nPop) if x != i] for i in range(self.nPop) ]
        self.isolating = [0 for i in range(self.nPop)]
        self.infInit()
                  

    def  infected(self, i):
        self.states[i] = 1
        self.latencyTime[i] = ceil(np.random.lognormal(1.501524205, 0.07145896398))
        sym = np.random.rand()
        if sym > self.severities[self.ageGroup[i]]:
            self.infectionType[i] = 1
            self.preSympTime[i] = 0
            self.infectiousTime[i] = ceil(np.random.lognormal(2.064055712, 0.1754185243))
        else:
            self.infectionType[i] = 2
            self.preSympTime[i] = ceil(np.random.lognormal(-0.1827236141, 0.7456993951))
            self.infectiousTime[i] = ceil(np.random.lognormal(2.064055712, 0.1754185243))
        self.latencyLen[i] = 0

    def iteration(self):
        new_inf = []
        new_iso = []
        if self.time == self.social_distancing:
            self.social_distance()
        if self.time == self.lockdown_date:
            self.lockdown()
        if self.time == self.isolation_date:
            self.isolation()
        if self.time == self.testing_date:
            self.testing()
        for i in range(self.nPop):
            if self.states[i] == 3 and self.infectiousLen[i] == self.infectiousTime[i]:
                self.states[i] = 4
                self.infectiousLen[i] = -1
            if self.isolating[i] == self.isolationLen:
                self.isolating[i] = 0
        for i in range(self.nPop):
            if self.states[i] == 2 and self.preSympLen[i] == self.preSympTime[i]:
                self.states[i] = 3
                self.preSympLen[i] = -1
                self.infectiousLen[i] = 0
                if self.isolationRule:
                    for q in self.households[self.household_no[i]]:
                        if q == i:
                            new_iso.append(q)
                        elif self.isolating[q] == 0:
                            new_iso.append(q)
        for i in range(self.nPop):
            if self.states[i] == 1 and self.latencyLen[i] == self.latencyTime[i]:
                if self.infectionType[i] == 2:
                    self.states[i] = 2
                    self.preSympLen[i] = 0
                    self.latencyLen[i] = -1
                else:
                    self.states[i] = 3
                    self.latencyLen[i] = -1
                    self.infectiousLen[i] = 0
            if self.isolating[i] == 0:
                if self.testingOn:
                    self.randTest(i)
                if self.isolating[i] == 0:
                    meeting_no = np.random.poisson(self.meeting_ave)
                    work_meeting_no = np.random.poisson(self.work_meeting_ave)
                    meetings1 = np.random.choice(self.mixersAvi[i], meeting_no)
                    meetings2 = np.append(meetings1, np.repeat(np.array([int(self.households[self.household_no[i]][k]) for k in range(len(self.households[self.household_no[i]])) if self.households[self.household_no[i]][k] != i ], dtype='int64'), 4))
                    meetings = np.append(meetings2, np.random.choice([self.workplaces[self.workplace_no[i]][k] for k in range(len(self.workplaces[self.workplace_no[i]])) if self.workplaces[self.workplace_no[i]][k] != i], work_meeting_no))
                    for j in range(len(meetings)):
                        self.all_meetings.append([i, meetings[j]])
                        if (self.states[meetings[j]] == 2 or self.states[meetings[j]] == 3) and self.states[i] == 0 and self.isolating[meetings[j]] == 0:
                            outcome = np.random.rand()
                            if self.household_no[i] == self.household_no[meetings[j]]:
                                if outcome < self.TransmProbHouse * self.infectionType[meetings[j]]:
                                    new_inf.append(i)
                                    self.infection_tracker.append([self.household_no[i], self.household_no[meetings[j]]])
                            else:
                                if outcome < self.TransmProb * self.infectionType[meetings[j]]:
                                    new_inf.append(i)
                                    self.infection_tracker.append([self.household_no[i], self.household_no[meetings[j]]])
            if self.states[i] == 1:
                self.latencyLen[i] += 1
            elif self.states[i] == 2:
                self.preSympLen[i] += 1
            elif self.states[i] == 3:
                self.infectiousLen[i] += 1
            if self.isolating[i] > 0:
                self.isolating[i] += 1
        for k in new_inf:
            self.infected(k)
        for l in new_iso:
            self.isolating[l] = 1
        self.time += 1                     

        
    def social_distance(self):
        self.TransmProb = self.TransmProb * self.eff_SocialD

    def lockdown(self):
        self.meeting_ave = self.meeting_ave * self.eff_Lockdown
        self.work_meeting_ave = 0

    def isolation(self):
        self.isolationRule = True

    def testing(self):
        self.testingOn = True
    
    def randTest(self, i):
        outcome = np.random.rand()
        if outcome < self.testProb:
            if self.states[i] == 3:
                self.isolating[i] = 1

    def summary(self):
        a = [self.states[x] for x in range(self.nPop) if self.states[x] == 0]
        b = [self.states[x] for x in range(self.nPop) if self.states[x] == 1]
        c = [self.states[x] for x in range(self.nPop) if self.states[x] == 2 or self.states[x] == 3]
        d = [self.states[x] for x in range(self.nPop) if self.states[x] == 4]
        e = [self.states[x] for x in range(self.nPop) if (self.states[x] == 2 or self.states[x] == 3) and self.infectionType[x] == 1]
        f = [self.states[x] for x in range(self.nPop) if (self.states[x] == 2 or self.states[x] == 3) and self.infectionType[x] == 2]
        return [len(a), len(b), len(c), len(d), len(e), len(f)]

    def run(self, n):
        for i in range(n):
            self.iteration()
            sum = self.summary()
            self.susc.append(sum[0])
            self.exp.append(sum[1])
            self.inf.append(sum[2])
            self.rec.append(sum[3])
            self.asy.append(sum[4])
            self.sym.append(sum[5])
            #if i % 10 == 0:
                #print(self.summary())
"""
nPop = 2000
inf0 = 1
ageDist = [0.11, 0.1, 0.12, 0.12, 0.12, 0.13, 0.1, 0.08, 0.04, 0.08]
household_dist = [0.15, 0.14, 0.03, 0.29, 0.1, 0.09, 0.02, 0.02, 0.02, 0.02, 0.02, 0.05, 0.02, 0.02, 0.01]
workplace_dist = [0.2, 0.4, 0.3, 0.1]
TransmProb = 0.016
severities = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.9]
meeting_ave = 8
work_meeting_ave = 9
social_distancing = -1
eff_SocialD = 0.18
lockdown_date = -1
eff_Lockdown = 0.1
isolation_date = 30
isolationLen = 14
testing_date = -1
testProb = 0.4

days = 100

model = abmHouseholds(nPop, inf0, ageDist, household_dist, workplace_dist, TransmProb, severities, meeting_ave, work_meeting_ave, social_distancing, eff_SocialD, lockdown_date, eff_Lockdown, isolation_date, isolationLen, testing_date, testProb)
start = time.time()
model.create_pop()
model.run(days)
end = time.time()
#print(model.summary())
print(end - start) 

times = [i for i in range(days)]

suscs = [sum(model.susc[i] for i in range(j, j+7))/7 for j in range(len(model.susc) - 7)]
exps = [sum(model.exp[i] for i in range(j, j+7))/7 for j in range(len(model.exp) - 7)]
infs = [sum(model.inf[i] for i in range(j, j+7))/7 for j in range(len(model.inf) - 7)]
recs = [sum(model.rec[i] for i in range(j, j+7))/7 for j in range(len(model.rec) - 7)]

times2 = [i for i in range(days - 7)]

#print(model.summary())
#same_household = [model.infection_tracker[i][0] for i in range(len(model.infection_tracker)) if model.infection_tracker[i][0] == model.infection_tracker[i][1] ]
#print(len(same_household) / len(model.infection_tracker))
#print(len(model.households))

#plt.plot(times, model.susc, linestyle='-', label="Susceptible")
#plt.plot(times, model.exp, linestyle='-', label="Exposed")
#plt.plot(times, model.inf, linestyle='-', label="Infected")
#plt.plot(times, model.asy, linestyle='-', label="Asymptomatic")
#plt.plot(times, model.sym, linestyle='-', label="Symptomatic")
#plt.plot(times, model.rec, linestyle='-', label="Recovered")

plt.plot(times2, suscs, linestyle='-', label="Susceptible")
plt.plot(times2, exps, linestyle='-', label="Exposed")
plt.plot(times2, infs, linestyle='-', label="Infected")
plt.plot(times2, recs, linestyle='-', label="Recovered")

plt.legend(loc="upper left")
plt.xlabel("time (days)")
plt.ylabel("proportion of population infected")

plt.show()
"""
