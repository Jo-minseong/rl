import numpy as np
import matplotlib.pyplot as plt

def k_armed_bandit(mean, size):
    return np.random.normal(mean, 1.0, size)

def Q_update(Qlist, choose, value, n):
    Qlist[choose] += (value-Qlist[choose])/n ########
    return Qlist

def Q_ucb_choose(Qlist, n , n_select):
    c = 2
    Q_ucb = np.zeros(10)
    for i in range(10):
        Q_ucb[i] = Qlist[i] + c * np.sqrt(np.log(n)/n_select[i])        
    return np.argmax(Q_ucb)

def Q_iter_in(eps):
    q_base = k_armed_bandit(0, 10)
    Qlist = np.zeros(10)
    reward = np.zeros(1000)
    n_select = np.zeros(10)    
    for i in range(1000):
        choose = Q_ucb_choose(Qlist, i, n_select + 1e-7)
        n_select[choose] += 1
        value = np.random.normal(q_base[choose], 1, 1)
        Qlist = Q_update(Qlist, choose, value, n_select[choose])
        if i == 0:
            reward[i] = value
        else:
            reward[i] = reward[i-1] + (value-reward[i-1])/(i+1)

    return reward

def Q_iter(iter, eps):
    reward = np.zeros(1000)  
    for i in range (iter):
        reward += Q_iter_in(eps)
    return reward/iter

reward_1 = Q_iter(2000, 0) # eps = 0.0

plt.plot(np.linspace(1,1000,1000), reward_1, label = 'eps = 0.0')

plt.legend()
plt.show()
