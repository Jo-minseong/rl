import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

class blackjack:

    def __init__(self):
        self.deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.hand_deck = {'A' : 0,
                          '2' : 0,
                          '3' : 0,
                          '4' : 0,
                          '5' : 0,
                          '6' : 0,
                          '7' : 0,
                          '8' : 0,
                          '9' : 0,
                          '10' : 0,
                          'J' : 0,
                          'Q' : 0,
                          'K' : 0}
        self.deck_count = 0
        self.init_count = np.random.randint(12,22)
        self.latest_pick = ''
        self.first_pick = ''
        self.player_done = 0 ############################################################
        self.dealer_done = 0

    def select(self):
        pick = str(np.random.choice(self.deck, replace = "True"))
        self.hand_deck[pick] += 1
        self.latest_pick = pick
        if self.first_pick == '':
            self.first_pick = self.latest_pick
        return pick

    def sum_without_ace(self):
        sum = (self.hand_deck['2'] * 2 +
               self.hand_deck['3'] * 3 +
               self.hand_deck['4'] * 4 +
               self.hand_deck['5'] * 5 +
               self.hand_deck['6'] * 6 +
               self.hand_deck['7'] * 7 +
               self.hand_deck['8'] * 8 +
               self.hand_deck['9'] * 9 +
               self.hand_deck['10'] * 10 +
               self.hand_deck['J'] * 10 +
               self.hand_deck['Q'] * 10 +
               self.hand_deck['K'] * 10)
        return sum
    
    def total_sum_player(self):
        sum = self.init_count + self.sum_without_ace()
        if sum <= 10:
            self.deck_count = sum + self.hand_deck['A'] * 11
        else:
            self.deck_count = sum + self.hand_deck['A'] * 1
        return self.deck_count
    
    def total_sum_dealer(self):
        sum = self.sum_without_ace()
        if sum <= 10:
            self.deck_count = sum + self.hand_deck['A'] * 11
        else:
            self.deck_count = sum + self.hand_deck['A'] * 1
        return self.deck_count
    
    def player_policy(self):
        if self.deck_count >= 20:
            self.player_done = 1
    
    def dealer_policy(self):
        if self.deck_count >= 17:
            self.dealer_done = 1

def generate_episode():
    
    player = blackjack()
    init_val = player.total_sum_player()
    
    dealer = blackjack()
    card = dealer.select()
    dealer.select()
    dealer.total_sum_dealer() # the card which dealer shown
    #dealer.total_sum_dealer()
    
    while True:
        
        player.player_policy()
        dealer.dealer_policy()
        if player.player_done == 0:
            player.select()
            player.total_sum_player()
        if dealer.dealer_done == 0:
            dealer.select()
            dealer.total_sum_dealer()
        if player.player_done == 1 and dealer.dealer_done == 1:
            break
    
    if player.deck_count >= 22:
        reward = -1
    elif dealer.deck_count >= 22:
        reward = 1
    elif player.deck_count >= dealer.deck_count:
        reward = 1
    else:
        reward = 0
    #print(reward)
    return card, init_val, reward

table = np.zeros((10, 10, 2))

for i in range(1000000):
    res = generate_episode()
    if res[0] == 'A':
        table[0, res[1]-12, 0] += res[2]
        table[0, res[1]-12, 1] += 1
    elif res[0] == 'J' or res[0] == 'Q' or res[0] == 'K':
        table[9, res[1]-12, 0] += res[2]
        table[9, res[1]-12, 1] += 1
    else:
        table[int(res[0])-1, res[1]-12, 0] += res[2]
        table[int(res[0])-1, res[1]-12, 1] += 1
        

res = table[:,:,0]/table[:,:,1]

X = np.arange(10)
Y = np.arange(10)
X, Y = np.meshgrid(X, Y)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_wireframe(X, Y, res[:,:])
plt.show()