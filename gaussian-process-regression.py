from simple_agent_based_model import abm
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import minimize

tr_start = 1
tr_end = 3
n = 11
X = np.linspace(tr_start, tr_end, n)

nPop = 500
inf0 = 1
TransmProb = 0.016
meeting_ave = 20

days = 43

s = 5

yp = np.empty(len(X))
for i in range(len(X)):
    model = abm(nPop, inf0, X[i]/100, meeting_ave)
    model.create_pop()
    model.run(days)
    yp[i] = (model.inf[42]) / nPop

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
outg2 = minimize(nlg2, 0.1 * np.var(y), args=(D, y, theta))
g = outg2.x[0]

def expD(D, theta, g):
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

for i in range(m):
    if i == 0:
        plt.plot(XX/100, YY[i], color="gray", alpha=0.1, label="Samples")
    else:
        plt.plot(XX/100, YY[i], color="gray", alpha=0.1)
plt.plot(XX/100, mup, label="Emulator estimate")
plt.plot(XX/100, q1, color='red', linestyle='dashed', label="95% CI")
plt.plot(XX/100, q2, color='red', linestyle='dashed')
plt.scatter(X/100, yp)

plt.xlabel("Transmission probability")
plt.ylabel("Proportion of infected at time 42")

plt.legend(loc="upper left")

plt.show()