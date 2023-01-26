import numpy as np
import matplotlib.pyplot as plt

def k_armed_bandit(mean, size):
    return np.random.normal(mean, 1.0, size)

def Q_choose(Qlist, eps, n):
    p = np.random.rand()
    if n == 0:
        res = np.random.randint(0,10)
    elif p < eps:
        res = np.random.randint(0,10)
    else:
        res = np.argmax(Qlist)
    return res

def Q_update(Qlist, choose, value, n):
    Qlist[choose] += (value-Qlist[choose])/n ########3
    return Qlist

def Q_iter_in(eps):
    q_base = k_armed_bandit(0, 10)
    Qlist = np.zeros(10)
    reward = np.zeros(1000)
    n_select = np.zeros(10)    
    for i in range(1000):
        choose = Q_choose(Qlist, eps, i)
        n_select[choose] += 1
        value = np.random.normal(q_base[choose], 1, 1)#k_armed_bandit(q_base[choose], 1)
        Qlist = Q_update(Qlist, choose, value, n_select[choose])
        #reward[i]=value
        #reward[i]=Qlist[choose]  
        #reward[i] = q_base[choose]

        if i == 0:
            reward[i] = value
        else:
            reward[i] = reward[i-1] + (value-reward[i-1])/(i+1)

## if you want to plot the right choose chance             
#        if choose == np.argmax(q_base):
#            reward[i]=1
        
    return reward

def Q_iter(iter, eps):
    reward = np.zeros(1000)  
    for i in range (iter):
        reward += Q_iter_in(eps)
    return reward/iter

reward_1 = Q_iter(2000, 0) # eps = 0.0
reward_2 = Q_iter(2000, 0.01) # eps 0.01
reward_3 = Q_iter(2000, 0.1) # eps 0.1

plt.plot(np.linspace(1,1000,1000), reward_1, label = 'eps = 0.0')
plt.plot(np.linspace(1,1000,1000), reward_2, label = 'eps = 0.01')
plt.plot(np.linspace(1,1000,1000), reward_3, label = 'eps = 0.1')
plt.legend()
plt.show()
