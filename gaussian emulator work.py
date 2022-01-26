from numpy.core.fromnumeric import transpose
from math import exp, log, sin
from COVIDabmSympPeriod import abmHouseholds
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import minimize
import time

start = time.time()
tr_start = 2
tr_end = 7
n = 6
X = np.linspace(tr_start, tr_end, n)

nPop = 500
inf0 = 1
ageDist = [0.11, 0.1, 0.12, 0.12, 0.12, 0.13, 0.1, 0.08, 0.04, 0.08]
household_dist = [0.15, 0.14, 0.03, 0.29, 0.1, 0.09, 0.02, 0.02, 0.02, 0.02, 0.02, 0.05, 0.02, 0.02, 0.01]
workplace_dist = [0.2, 0.4, 0.3, 0.1]
TransmProb = 0.016
severities = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.9]
meeting_ave = 8
work_meeting_ave = 9
days = 42
eff_SocialD = 0.18
eff_Lockdown = 0.1
isolation_date = 30
isolationLen = 14
days = 100

s = 5

yp = np.empty(len(X))
for i in range(len(X)):
    rt = []
    for j in range(s):
        a = True
        while a is True:
            model = abmHouseholds(nPop, inf0, ageDist, household_dist, workplace_dist, TransmProb, severities, meeting_ave, work_meeting_ave, -1, eff_SocialD, X[i] * 10, eff_Lockdown, -1, isolationLen)
            model.create_pop()
            model.run(days)
            if model.summary()[0] / nPop < 0.96:
                a = False
        rt.append((model.rec[days -1]) / nPop)
    print(i)
    yp[i] = np.median(rt)

y = np.transpose(np.matrix(yp))

def dist(X, Y):
    n = len(X)
    m = len(Y)
    D = [ [ (X[i] - Y[j])**2 for j in range(m)] for i in range(n) ]
    return np.matrix(D)

D = dist(X, X)

eps = np.finfo(float).eps

def nlg1(theta, D, Y):
    n = len(Y)
    K = np.exp(D/theta)
    K = np.matrix(K, dtype='float64')
    Ki = np.linalg.inv(K)
    dotK = np.multiply(K, D/(theta**2))
    KiY = np.matmul(Ki, Y)

    ll = (n/2) * float(np.matmul(np.matmul(np.transpose(KiY), dotK), KiY)) / float(np.matmul(np.transpose(Y), KiY)) - (1/2) * float(np.trace(np.matmul(Ki, dotK)))
    #print(ll)
    return -ll    

def nlg2(g, D, Y, theta):
    n = len(Y)
    K = np.exp(D/theta)
    K = np.add(K, g * np.identity(len(D)))
    Ki = np.linalg.inv(K)
    KiY = np.matmul(Ki, Y)
    ll = (n/2) * float(np.matmul(np.transpose(KiY), KiY)) / float(np.matmul(np.transpose(Y), KiY)) - (1/2) * float(np.trace(Ki))
    return -ll

outg1 = minimize(nlg1, 1, args=(D, y))
theta = outg1.x[0]
print(theta)
outg2 = minimize(nlg2, 0.1 * np.var(y), args=(D, y, theta))
g = outg2.x[0]
print(g)

def expD(D, theta, g):
    n = len(D)
    m = len(D[0])
    if g != 0:
        return np.add(np.exp(-D/theta), g * np.identity(len(D)))
    else:
        return np.exp(-D/theta)

Sigma = expD(D, theta, g)

m = 100
XX = np.linspace(tr_start, tr_end, m)

DXX = dist(XX, XX)
SXX = expD(DXX, theta, g)

DX = dist(XX, X)
SX = expD(DX, theta, 0)
Si = np.linalg.inv(Sigma)
premup = np.matmul(SX, Si)

tau2hat = float(np.matmul(np.matmul(np.transpose(y), Si), y))/n
print(tau2hat)

mup = np.matrix(np.matmul(premup, y), dtype='float64')

Sigmap1 = np.matmul(premup, np.transpose(SX), dtype='float64')
Sigmap2 = np.subtract(SXX, Sigmap1, dtype='float64')
Sigmap = np.matrix(tau2hat * Sigmap2, dtype='float64')

a = expD(DXX, 1, 0)
for i in range(len(SXX)):
    a[i, i] += eps
b = np.matmul(np.matmul(SX, Si), np.transpose(SX))

Sigma_int = np.matrix(tau2hat * np.subtract(a, b), dtype='float64')

YY = np.random.multivariate_normal(np.squeeze(np.asarray(mup)), Sigmap, m)

q1 = [float(mup[i, 0]) + norm.ppf(0.05, 0, float(Sigmap[i, i])**0.5) for i in range(len(Sigmap))]
q2 = [float(mup[i, 0]) + norm.ppf(0.95, 0, float(Sigmap[i, i])**0.5) for i in range(len(Sigmap))]

end = time.time()

print(end -start)

for i in range(m):
    if i == 0:
        plt.plot(XX * 10, YY[i], color="gray", alpha=0.1, label="Samples")
    else:
        plt.plot(XX * 10, YY[i], color="gray", alpha=0.1)
plt.plot(XX * 10, mup, label="Emulator estimate")
plt.plot(XX * 10, q1, color='red', linestyle='dashed', label="95% CI")
plt.plot(XX * 10, q2, color='red', linestyle='dashed')
plt.scatter(X * 10, yp)

plt.xlabel("Date of implementation of lockdown")
plt.ylabel("Proportion of population recovered")

plt.legend(loc="upper left")

plt.show()