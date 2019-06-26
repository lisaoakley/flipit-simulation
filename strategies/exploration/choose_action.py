import numpy as np
import random
import math

def noise(sigma,row):
    row[1] += sigma* np.random.randn()
    return np.argmax(row)

def epsilon_greedy(epsilon,row,tick,decay_lambda):
    decay = epsilon * math.exp(-decay_lambda*tick)
    if random.random() < decay:
        return random.randint(0,1)
    return np.argmax(row)

def epsilon_greedy_visit_decay(epsilon,row,visits,decay_lambda,no_move_weight):
    decay = epsilon * math.exp(-decay_lambda*visits)
    if random.random() < decay:
        return 0 if random.random() < no_move_weight else 1
    return np.argmax(row)

def uniform_epsilon_greedy_visit_decay(epsilon,row,visits,decay_lambda):
    decay = epsilon * math.exp(-decay_lambda*visits)
    if random.random() < decay:
        return random.randint(0,1)
    return np.argmax(row)
